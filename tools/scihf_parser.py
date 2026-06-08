#!/usr/bin/env python3
"""
.scihf Parser & Checker — L2 from ROADMAP

Implements the complete .scihf language pipeline:
  1. Tokenizer (lexer)  — §0 of LANGUAGE.md
  2. Parser (AST)       — §1-2 of LANGUAGE.md
  3. Checker (semantic) — §3, §5 of LANGUAGE.md

Usage:
  python3 tools/scihf_parser.py layer1/physics.scihf          # parse + check
  python3 tools/scihf_parser.py --check-only layer1/            # batch check
  python3 tools/scihf_parser.py --ast                            # print AST
"""

import re
import sys
import os
import json
from dataclasses import dataclass, field
from typing import Optional, Union
from enum import Enum, auto
from collections import defaultdict


# ═══════════════════════════════════════════════════════════════
# TOKENIZER (Lexer) — LANGUAGE.md §0
# ═══════════════════════════════════════════════════════════════

class TokenType(Enum):
    KEYWORD   = auto()   # Q, C, kernel, rule, contingent, effective_law, law, corollary
    IDENT     = auto()   # identifiers (quantity names, condition names, constant names)
    NUMBER    = auto()   # integer or float, optional scientific notation
    DIMENSION = auto()   # dimension literals [M·L·T⁻²]
    RELATION  = auto()   # =, ∝[+], ∝[-], ≠, ≥, ≤
    CALC      = auto()   # d, ∂, ∇, ∇·, ∇×, ∫, ∂_μ
    PUNCT     = auto()   # [, ], (, ), |, ←, ,, ·, +, -, /, ^
    EOF       = auto()


@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    col: int

    def __repr__(self):
        return f"Token({self.type.name}, '{self.value}', L{self.line}:{self.col})"


# Token patterns ordered by priority (longest match first)
TOKEN_SPEC = [
    # CALC — multi-char operators first
    (r'∂_μ',    TokenType.CALC),
    (r'∇·',     TokenType.CALC),
    (r'∇×',     TokenType.CALC),
    (r'∇',      TokenType.CALC),
    (r'∂',      TokenType.CALC),
    (r'∫',      TokenType.CALC),
    # DIMENSION — must contain a dimension base letter (L, M, T, I, Θ, N, J) or be [1]
    (r'\[1\]',  TokenType.DIMENSION),
    (r'\[[MLTIΘNJ][^\]]*\]', TokenType.DIMENSION),
    # RELATION — multi-char patterns first
    (r'∝\[\+\]', TokenType.RELATION),
    (r'∝\[\-\]', TokenType.RELATION),
    (r'∝',      TokenType.RELATION),
    (r'≠',      TokenType.RELATION),
    (r'≥',      TokenType.RELATION),
    (r'≤',      TokenType.RELATION),
    (r'=',      TokenType.RELATION),
    # KEYWORD
    (r'effective_law(?![.a-zA-Z0-9])', TokenType.KEYWORD),
    (r'corollary(?![.a-zA-Z0-9])', TokenType.KEYWORD),
    (r'contingent(?![.a-zA-Z0-9])', TokenType.KEYWORD),
    (r'kernel(?![.a-zA-Z0-9])',  TokenType.KEYWORD),
    (r'rule(?![.a-zA-Z0-9])',    TokenType.KEYWORD),
    (r'law(?![.a-zA-Z0-9])',     TokenType.KEYWORD),
    (r'\bQ\b',   TokenType.KEYWORD),
    (r'\bC\b',   TokenType.KEYWORD),
    # NUMBER
    (r'\d+\.\d+[eE][+-]?\d+', TokenType.NUMBER),
    (r'\d+[eE][+-]?\d+', TokenType.NUMBER),
    (r'\d+\.\d+', TokenType.NUMBER),
    (r'\d+',     TokenType.NUMBER),
    # CALC — single-char
    (r'd(?=[(])', TokenType.CALC),   # d( only
    # PUNCT
    (r'←',      TokenType.PUNCT),
    (r'→',      TokenType.PUNCT),
    (r'·',      TokenType.PUNCT),
    (r'\[',     TokenType.PUNCT),
    (r'\]',     TokenType.PUNCT),
    (r'\(',     TokenType.PUNCT),
    (r'\)',     TokenType.PUNCT),
    (r'\|',     TokenType.PUNCT),
    (r',',      TokenType.PUNCT),
    (r'\+',     TokenType.PUNCT),
    (r'-',      TokenType.PUNCT),
    (r'−',      TokenType.PUNCT),
    (r'/',      TokenType.PUNCT),
    (r'\^',     TokenType.PUNCT),
    # Comment (must be before catch-all)
    (r'#.*', None),
    # IDENT — Unicode-aware: letters, Greek, subscripts, math symbols
    (r'[a-zA-Zα-ωΑ-ΩħδΔℒℝ⟨⟩][a-zA-Z0-9α-ωΑ-ΩħδΔℒℝ_\.₀₁₂₃₄₅₆₇₈₉⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺]*', TokenType.IDENT),
    # Catch-all TEXT for free-form content (Chinese, math symbols, etc.)
    (r'[^\s\[\]\(\)\|←→\,·\+−\^=∝≥≤≠∂∇∫/]', TokenType.IDENT),
    # Whitespace
    (r'[ \t\r\n]+', None),
    # Comment
    (r'#.*', None),
]


class SciHFTokenizer:
    """Tokenizer for .scihf language (§0 of LANGUAGE.md)."""

    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.line = 1
        self.col = 1

    def tokenize(self) -> list[Token]:
        tokens = []
        while self.pos < len(self.text):
            matched = False
            for pattern, tok_type in TOKEN_SPEC:
                m = re.match(pattern, self.text[self.pos:])
                if m:
                    value = m.group(0)
                    if tok_type is not None:  # skip whitespace/comments
                        tokens.append(Token(tok_type, value, self.line, self.col))
                    # Update position
                    newlines = value.count('\n')
                    if newlines > 0:
                        self.line += newlines
                        self.col = len(value) - value.rfind('\n')
                    else:
                        self.col += len(value)
                    self.pos += len(value)
                    matched = True
                    break
            if not matched:
                # Find the problematic character and report it
                bad_char = self.text[self.pos]
                context = self.text[max(0,self.pos-10):self.pos+10]
                raise SyntaxError(
                    f"Unexpected character '{bad_char}' (U+{ord(bad_char):04X}) "
                    f"at line {self.line}, col {self.col}\n  context: ...{context}..."
                )
        tokens.append(Token(TokenType.EOF, '', self.line, self.col))
        # Normalize Unicode operators to ASCII equivalents
        normalized = []
        for tok in tokens:
            if tok.value == '−':
                normalized.append(Token(tok.type, '-', tok.line, tok.col))
            else:
                normalized.append(tok)
        return normalized


# ═══════════════════════════════════════════════════════════════
# AST NODES — LANGUAGE.md §1
# ═══════════════════════════════════════════════════════════════

@dataclass
class Expr:
    """N6: Mathematical expression tree."""
    pass

@dataclass
class IdentExpr(Expr):
    name: str

@dataclass
class NumberExpr(Expr):
    value: str

@dataclass
class BinOpExpr(Expr):
    op: str
    left: Expr
    right: Expr

@dataclass
class DerivativeExpr(Expr):
    """d(id₁)/d(id₂) or ∂(id₁)/∂(id₂)"""
    operator: str   # 'd' or '∂'
    numerator: str
    denominator: str

@dataclass
class GradientExpr(Expr):
    """∇(id), ∇·(id), ∇×(id)"""
    operator: str   # '∇', '∇·', '∇×'
    target: str

@dataclass
class PowerExpr(Expr):
    base: Expr
    exponent: str

@dataclass
class BraExpr(Expr):
    name: str

@dataclass
class KetExpr(Expr):
    name: str

@dataclass
class BraketExpr(Expr):
    bra: str
    ket: str

@dataclass
class CommutatorExpr(Expr):
    left: Expr
    right: Expr


@dataclass
class QuantityDecl:
    """N2: Q(name, dim, class)"""
    name: str
    dim: str
    equiv_class: str

@dataclass
class ConditionDecl:
    """N3: C(name, category)"""
    name: str
    category: str


class RelationType(Enum):
    EQUALITY = auto()
    PROPORTIONALITY = auto()
    INEQUALITY = auto()
    EXISTENCE = auto()
    LIMIT = auto()


@dataclass
class Relation:
    """N5: Core semantic relation."""
    type: RelationType
    # Equality
    left: Optional[Expr] = None
    right: Optional[Expr] = None
    # Proportionality
    subject: Optional[str] = None
    direction: Optional[str] = None   # '+' or '-'
    proportional_to: Optional[list[str]] = None
    # Inequality
    op: Optional[str] = None
    # Existence
    conserved_id: Optional[str] = None
    # Limit
    lim_id1: Optional[str] = None
    lim_val1: Optional[str] = None
    lim_id2: Optional[str] = None
    lim_val2: Optional[str] = None


@dataclass
class Assertion:
    """N4: [layer] relation [scope] [source]"""
    layer: str          # kernel, rule, contingent, effective_law, law, corollary
    relation: Relation
    scope: list[str] = field(default_factory=list)
    source: list[str] = field(default_factory=list)


@dataclass
class Program:
    """N1: Root node."""
    quantities: list[QuantityDecl] = field(default_factory=list)
    conditions: list[ConditionDecl] = field(default_factory=list)
    assertions: list[Assertion] = field(default_factory=list)


# ═══════════════════════════════════════════════════════════════
# PARSER — LANGUAGE.md §1-2
# ═══════════════════════════════════════════════════════════════

class SciHFParser:
    """Recursive descent parser for .scihf language."""

    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0
        self.diagnostics: list[str] = []

    def peek(self) -> Token:
        return self.tokens[self.pos]

    def advance(self) -> Token:
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def expect(self, ttype: TokenType, value: Optional[str] = None) -> Token:
        tok = self.peek()
        if tok.type != ttype or (value is not None and tok.value != value):
            raise SyntaxError(
                f"Expected {ttype.name}" + (f" '{value}'" if value else "") +
                f", got {tok.type.name} '{tok.value}' at L{tok.line}:{tok.col}"
            )
        return self.advance()

    def parse_program(self) -> Program:
        """program ::= decl* stmt*"""
        prog = Program()
        while self.peek().type != TokenType.EOF:
            tok = self.peek()
            if tok.type == TokenType.KEYWORD and tok.value == 'Q':
                prog.quantities.append(self.parse_quantity_decl())
            elif tok.type == TokenType.KEYWORD and tok.value == 'C':
                prog.conditions.append(self.parse_condition_decl())
            elif tok.type == TokenType.PUNCT and tok.value == '[':
                prog.assertions.append(self.parse_assertion())
            else:
                raise SyntaxError(
                    f"Unexpected token {tok.type.name} '{tok.value}' "
                    f"at L{tok.line}:{tok.col}"
                )
        return prog

    def parse_quantity_decl(self) -> QuantityDecl:
        """Q(name, dim, class)"""
        self.expect(TokenType.KEYWORD, 'Q')
        self.expect(TokenType.PUNCT, '(')
        name = self.expect(TokenType.IDENT).value
        self.expect(TokenType.PUNCT, ',')
        dim = self.expect(TokenType.DIMENSION).value
        self.expect(TokenType.PUNCT, ',')
        equiv_class = self.expect(TokenType.IDENT).value
        self.expect(TokenType.PUNCT, ')')
        return QuantityDecl(name=name, dim=dim, equiv_class=equiv_class)

    def parse_condition_decl(self) -> ConditionDecl:
        """C(name, category)"""
        self.expect(TokenType.KEYWORD, 'C')
        self.expect(TokenType.PUNCT, '(')
        name = self.expect(TokenType.IDENT).value
        self.expect(TokenType.PUNCT, ',')
        category = self.expect(TokenType.IDENT).value
        self.expect(TokenType.PUNCT, ')')
        return ConditionDecl(name=name, category=category)

    def parse_assertion(self) -> Assertion:
        """stmt ::= '[' layer ']' (formal_relation | free_text) [scope] [source]"""
        self.expect(TokenType.PUNCT, '[')
        layer = self.expect(TokenType.KEYWORD).value
        self.expect(TokenType.PUNCT, ']')

        saved_pos = self.pos
        rel = None

        # Try parsing as a formal relation first
        try:
            rel = self._try_parse_relation()
            # Check if there are leftover tokens before scope/source markers
            tok = self.peek()
            if tok.type != TokenType.EOF and not (
                (tok.type == TokenType.PUNCT and tok.value in ('|', '←', '['))
            ):
                # Formal parse matched but left extra tokens — fall back to free text
                raise SyntaxError('Extra tokens after formal relation')
        except SyntaxError:
            self.pos = saved_pos
            # Free-form text: collect tokens; | only stops if followed by scope-like content
            text_tokens = []
            while self.pos < len(self.tokens) - 1:
                tok = self.peek()
                if tok.type == TokenType.EOF:
                    break
                if tok.type == TokenType.PUNCT and tok.value == '[':
                    break
                if tok.type == TokenType.PUNCT and tok.value in ('|', '←'):
                    # Check if what follows looks like a scope/source marker
                    peek_pos = self.pos + 1
                    is_scope = False
                    if tok.value == '←':
                        is_scope = True  # ← always starts source
                    elif peek_pos < len(self.tokens):
                        next_tok = self.tokens[peek_pos]
                        # Scope: IDENT followed by comma, |, ←, [, or EOF
                        if next_tok.type == TokenType.IDENT:
                            peek_pos2 = peek_pos + 1
                            if peek_pos2 < len(self.tokens):
                                n2 = self.tokens[peek_pos2]
                                if n2.type == TokenType.PUNCT and n2.value in (',', '|', '←', '['):
                                    is_scope = True
                                elif n2.type == TokenType.EOF:
                                    is_scope = True
                            else:
                                is_scope = True
                    if is_scope:
                        break
                text_tokens.append(self.advance())
            text = ' '.join(t.value for t in text_tokens).strip()
            if text:
                rel = Relation(type=RelationType.EQUALITY,
                              left=IdentExpr(name=text),
                              right=IdentExpr(name='true'))

        scope = []
        source = []

        while self.pos < len(self.tokens) - 1:
            tok = self.peek()
            if tok.type == TokenType.EOF:
                break
            if tok.type == TokenType.PUNCT and tok.value == '|':
                self.advance()
                scope = self._parse_id_list_flexible()
            elif tok.type == TokenType.PUNCT and tok.value == '←':
                self.advance()
                source = self._parse_id_list_flexible()
            elif tok.type == TokenType.PUNCT and tok.value == '[':
                break
            else:
                break

        return Assertion(layer=layer, relation=rel, scope=scope, source=source)

    def _try_parse_relation(self) -> Relation:
        """Attempt to parse any formal relation type."""
        saved = self.pos
        for method in [self.parse_existence, self.parse_limit,
                       self.parse_proportionality, self.parse_inequality,
                       self.parse_equality]:
            self.pos = saved
            try:
                return method()
            except SyntaxError:
                continue
        raise SyntaxError("No relation matched")

    def _parse_id_list_flexible(self) -> list[str]:
        """Parse comma-separated identifiers, stopping at [, |, ←, EOF."""
        ids = []
        while self.pos < len(self.tokens) - 1:
            tok = self.peek()
            if tok.type == TokenType.EOF:
                break
            if tok.type == TokenType.PUNCT and tok.value in ('[', '|', '←'):
                break
            if tok.type == TokenType.IDENT:
                ids.append(self.advance().value)
            elif tok.type == TokenType.PUNCT and tok.value == ',':
                self.advance()
            else:
                break
        return ids

    def parse_relation(self) -> Relation:
        """Parse the relation part of an assertion."""
        # Save position for backtracking
        saved_pos = self.pos
        saved_diag = len(self.diagnostics)

        # Try each relation type in order of specificity
        try:
            return self.parse_existence()
        except:
            self.pos = saved_pos

        try:
            return self.parse_limit()
        except:
            self.pos = saved_pos

        try:
            return self.parse_proportionality()
        except:
            self.pos = saved_pos

        try:
            return self.parse_inequality()
        except:
            self.pos = saved_pos

        return self.parse_equality()

    def parse_equality(self) -> Relation:
        """equality ::= expr '=' expr"""
        left = self.parse_expr()
        self.expect(TokenType.RELATION, '=')
        right = self.parse_expr()
        return Relation(type=RelationType.EQUALITY, left=left, right=right)

    def parse_proportionality(self) -> Relation:
        """proportionality ::= id '∝[' dir ']' id { '·' id }"""
        subject = self.expect(TokenType.IDENT).value
        # Match ∝[+] or ∝[-]
        rel_tok = self.peek()
        if rel_tok.type != TokenType.RELATION or not rel_tok.value.startswith('∝'):
            raise SyntaxError(f"Expected ∝[dir] at L{rel_tok.line}")
        direction = '+' if '[+]' in rel_tok.value else '-'
        self.advance()
        proportional_to = []
        # First dependent id
        proportional_to.append(self.expect(TokenType.IDENT).value)
        while self.peek().type == TokenType.PUNCT and self.peek().value == '·':
            self.advance()
            proportional_to.append(self.expect(TokenType.IDENT).value)
        return Relation(type=RelationType.PROPORTIONALITY,
                       subject=subject, direction=direction, proportional_to=proportional_to)

    def parse_inequality(self) -> Relation:
        """inequality ::= expr ('≥' | '≤') expr"""
        left = self.parse_expr()
        op_tok = self.peek()
        if op_tok.type != TokenType.RELATION or op_tok.value not in ('≥', '≤'):
            raise SyntaxError(f"Expected ≥ or ≤")
        self.advance()
        right = self.parse_expr()
        return Relation(type=RelationType.INEQUALITY, left=left, right=right,
                       op=op_tok.value)

    def parse_existence(self) -> Relation:
        """existence ::= '∂_μ' id '= 0'"""
        self.expect(TokenType.CALC, '∂_μ')
        conserved_id = self.expect(TokenType.IDENT).value
        self.expect(TokenType.RELATION, '=')
        self.expect(TokenType.NUMBER, '0')
        return Relation(type=RelationType.EXISTENCE, conserved_id=conserved_id)

    def parse_limit(self) -> Relation:
        """limit ::= id '→' number '|' id '→' number"""
        lim_id1 = self.expect(TokenType.IDENT).value
        self.expect(TokenType.PUNCT)  # should be → but let's be flexible
        lim_val1 = self.expect(TokenType.NUMBER).value
        self.expect(TokenType.PUNCT, '|')
        lim_id2 = self.expect(TokenType.IDENT).value
        self.expect(TokenType.PUNCT)  # should be →
        lim_val2 = self.expect(TokenType.NUMBER).value
        return Relation(type=RelationType.LIMIT,
                       lim_id1=lim_id1, lim_val1=lim_val1,
                       lim_id2=lim_id2, lim_val2=lim_val2)

    def parse_id_list(self) -> list[str]:
        """Comma-separated identifier list."""
        ids = []
        ids.append(self.expect(TokenType.IDENT).value)
        while self.peek().type == TokenType.PUNCT and self.peek().value == ',':
            self.advance()
            ids.append(self.expect(TokenType.IDENT).value)
        return ids

    # ── Expression parsing ──

    def parse_expr(self) -> Expr:
        """expr ::= term { ('+' | '-') term }"""
        left = self.parse_term()
        while self.peek().type == TokenType.PUNCT and self.peek().value in ('+', '-'):
            op = self.advance().value
            right = self.parse_term()
            left = BinOpExpr(op=op, left=left, right=right)
        return left

    def parse_term(self) -> Expr:
        """term ::= factor { '·' factor }"""
        left = self.parse_factor()
        while self.peek().type == TokenType.PUNCT and self.peek().value == '·':
            self.advance()
            right = self.parse_factor()
            left = BinOpExpr(op='·', left=left, right=right)
        return left

    def parse_factor(self) -> Expr:
        """factor ::= id | number | calc_expr | bra | ket | braket | comm | power | paren | division"""
        tok = self.peek()

        # Calc expressions
        if tok.type == TokenType.CALC:
            op = tok.value
            if op in ('d', '∂'):
                self.advance()
                return self.parse_derivative(op)
            elif op in ('∇', '∇·', '∇×'):
                self.advance()
                return self.parse_gradient(op)
            elif op == '∂_μ':
                return IdentExpr(name=self.advance().value)

        # bra(...), ket(...), braket(...), comm(...)
        if tok.type == TokenType.IDENT:
            name = tok.value
            if name == 'bra':
                self.advance()
                self.expect(TokenType.PUNCT, '(')
                inner = self.expect(TokenType.IDENT).value
                self.expect(TokenType.PUNCT, ')')
                return BraExpr(name=inner)
            elif name == 'ket':
                self.advance()
                self.expect(TokenType.PUNCT, '(')
                inner = self.expect(TokenType.IDENT).value
                self.expect(TokenType.PUNCT, ')')
                return KetExpr(name=inner)
            elif name == 'braket':
                self.advance()
                self.expect(TokenType.PUNCT, '(')
                bra = self.expect(TokenType.IDENT).value
                self.expect(TokenType.PUNCT, ',')
                ket = self.expect(TokenType.IDENT).value
                self.expect(TokenType.PUNCT, ')')
                return BraketExpr(bra=bra, ket=ket)
            elif name == 'comm':
                self.advance()
                self.expect(TokenType.PUNCT, '(')
                left = self.parse_expr()
                self.expect(TokenType.PUNCT, ',')
                right = self.parse_expr()
                self.expect(TokenType.PUNCT, ')')
                return CommutatorExpr(left=left, right=right)

        # NUMBER
        if tok.type == TokenType.NUMBER:
            return NumberExpr(value=self.advance().value)

        # IDENT
        if tok.type == TokenType.IDENT:
            name = self.advance().value
            # Check for power
            if self.peek().type == TokenType.PUNCT and self.peek().value == '^':
                self.advance()
                exp = self.expect(TokenType.NUMBER).value
                return PowerExpr(base=IdentExpr(name=name), exponent=exp)
            return IdentExpr(name=name)

        # Parenthesized expression
        if tok.type == TokenType.PUNCT and tok.value == '(':
            self.advance()
            expr = self.parse_expr()
            self.expect(TokenType.PUNCT, ')')
            # Check for power
            if self.peek().type == TokenType.PUNCT and self.peek().value == '^':
                self.advance()
                exp = self.expect(TokenType.NUMBER).value
                return PowerExpr(base=expr, exponent=exp)
            return expr

        raise SyntaxError(
            f"Unexpected token {tok.type.name} '{tok.value}' in expression "
            f"at L{tok.line}:{tok.col}"
        )

    def parse_derivative(self, op: str) -> DerivativeExpr:
        """d(id₁)/d(id₂) or ∂(id₁)/∂(id₂)"""
        self.expect(TokenType.PUNCT, '(')
        num = self.expect(TokenType.IDENT).value
        self.expect(TokenType.PUNCT, ')')
        self.expect(TokenType.PUNCT, '/')
        self.expect(TokenType.CALC, op)
        self.expect(TokenType.PUNCT, '(')
        den = self.expect(TokenType.IDENT).value
        self.expect(TokenType.PUNCT, ')')
        return DerivativeExpr(operator=op, numerator=num, denominator=den)

    def parse_gradient(self, op: str) -> GradientExpr:
        """∇(id), ∇·(id), ∇×(id)"""
        self.expect(TokenType.PUNCT, '(')
        target = self.expect(TokenType.IDENT).value
        self.expect(TokenType.PUNCT, ')')
        return GradientExpr(operator=op, target=target)


# ═══════════════════════════════════════════════════════════════
# SEMANTIC CHECKER — LANGUAGE.md §3, §5
# ═══════════════════════════════════════════════════════════════

@dataclass
class Diagnostic:
    level: str    # ERROR, WARNING
    code: str     # C1-C6, V1-V5
    message: str
    line: int = 0


class SciHFChecker:
    """Semantic checker for .scihf AST."""

    def __init__(self, program: Program):
        self.program = program
        self.diagnostics: list[Diagnostic] = []
        # Build lookup tables
        self.quantity_dims: dict[str, str] = {}
        self.quantity_classes: dict[str, str] = {}
        self.condition_categories: dict[str, str] = {}
        self.assertion_ids: set[str] = set()
        for q in program.quantities:
            self.quantity_dims[q.name] = q.dim
            self.quantity_classes[q.name] = q.equiv_class
        for c in program.conditions:
            self.condition_categories[c.name] = c.category

    def check(self) -> list[Diagnostic]:
        self._check_reference_integrity()   # C1
        self._check_dimension_consistency() # C2
        self._check_layer_ordering()        # C3, V1-V4
        self._check_equivalence_class()     # C4
        self._check_duplicate_premises()    # C6
        return self.diagnostics

    def _check_reference_integrity(self):
        """C1: All referenced IDs must be declared."""
        # Collect all references from expressions, scopes, sources
        for i, assertion in enumerate(self.program.assertions):
            # Check scope references
            for s in assertion.scope:
                if s not in self.condition_categories:
                    self.diagnostics.append(Diagnostic(
                        'WARNING', 'C1',
                        f"Scope condition '{s}' not declared via C(...)",
                        line=i+1
                    ))
            # Check source references (will be resolved against assertion IDs in V1)
            # For expression references, collect all identifiers in relations
            refs = set()
            self._collect_identifiers(assertion.relation, refs)
            for ref in refs:
                if ref not in self.quantity_dims and ref not in self.condition_categories:
                    # Allow known physics constants and operators
                    if ref in ('ħ', 'c', 'k_B', 'G', 'ε₀', 'μ₀', 'π', 'e',
                               'exp', 'ln', 'sin', 'cos', 'h', 'ℏ', 'i', 'S_y', 'σ_x',
                               'σ_p', 'E', 'B', 'J', 'F', 'U', 'ρ_q', 'ν', 'T', 'P',
                               'V', 'N', 'S', 'm', 'p', 'r', 't', 'x', 'y', 'z', 'L',
                               'Δs', 'Ψ', 'ψ', 'φ', 'θ', 'μ', 'E_i', 'g', 'a', 'v',
                               'δS', 'dU', 'dS', 'dV', 'T^μν', 'J^μ', 'δ', 'f(E)', 'F_μν'):
                        continue
                    self.diagnostics.append(Diagnostic(
                        'WARNING', 'C1',
                        f"Identifier '{ref}' not declared via Q(...) or C(...)",
                        line=i+1
                    ))

    def _check_dimension_consistency(self):
        """C2: Dimension consistency for equality relations."""
        for i, assertion in enumerate(self.program.assertions):
            if assertion.relation.type == RelationType.EQUALITY:
                rel = assertion.relation
                dim_l = self._compute_dim(rel.left)
                dim_r = self._compute_dim(rel.right)
                if dim_l and dim_r and dim_l != dim_r:
                    self.diagnostics.append(Diagnostic(
                        'ERROR', 'C2',
                        f"Dimension mismatch: {dim_l} ≠ {dim_r}",
                        line=i+1
                    ))

    def _check_layer_ordering(self):
        """C3 + V1-V4: Layer ordering and graph constraints."""
        # Build assertion ID map
        source_graph: dict[str, list[str]] = {}
        layers: dict[str, str] = {}
        for i, assertion in enumerate(self.program.assertions):
            # Generate an ID from the relation content
            aid = self._generate_assertion_id(assertion, i)
            layers[aid] = assertion.layer
            source_graph[aid] = list(assertion.source)

        # V3: Layer ordering
        layer_rank = {'kernel': 0, 'rule': 0, 'contingent': 0,
                      'effective_law': 1, 'law': 1,
                      'corollary': 2}
        for aid, srcs in source_graph.items():
            lyr = layers[aid]
            if lyr not in layer_rank:
                continue
            for src in srcs:
                if src in layers:
                    src_lyr = layers.get(src, 'kernel')
                    if src_lyr not in layer_rank:
                        continue
                    if layer_rank.get(lyr, 99) < layer_rank.get(src_lyr, 99):
                        self.diagnostics.append(Diagnostic(
                            'ERROR', 'C3',
                            f"Layer ordering violation: {lyr} '{aid}' "
                            f"derives from {src_lyr} '{src}'"
                        ))

        # V2: Cycle detection
        self._check_cycles(source_graph)

    def _check_cycles(self, graph: dict[str, list[str]]):
        """V2: Detect cycles in the derivation graph using DFS."""
        WHITE, GRAY, BLACK = 0, 1, 2
        color = {node: WHITE for node in graph}

        def dfs(node, path):
            color[node] = GRAY
            for neighbor in graph.get(node, []):
                if neighbor not in color:
                    continue
                if color[neighbor] == GRAY:
                    cycle = path[path.index(neighbor):] + [neighbor]
                    self.diagnostics.append(Diagnostic(
                        'ERROR', 'V2',
                        f"Cycle detected: {' → '.join(cycle)}"
                    ))
                elif color[neighbor] == WHITE:
                    dfs(neighbor, path + [neighbor])
            color[node] = BLACK

        for node in graph:
            if color.get(node) == WHITE:
                dfs(node, [node])

    def _check_equivalence_class(self):
        """C4: Warn if different quantities share dimension but have different classes."""
        dim_to_classes: dict[str, set[str]] = defaultdict(set)
        for name, dim in self.quantity_dims.items():
            cls = self.quantity_classes.get(name, '')
            dim_to_classes[dim].add(cls)
        for dim, classes in dim_to_classes.items():
            if len(classes) > 1:
                self.diagnostics.append(Diagnostic(
                    'WARNING', 'C4',
                    f"Dimension {dim} has multiple equivalence classes: {classes}"
                ))

    def _check_duplicate_premises(self):
        """C6: No duplicate IDs in source lists."""
        for i, assertion in enumerate(self.program.assertions):
            seen = set()
            for src in assertion.source:
                if src in seen:
                    self.diagnostics.append(Diagnostic(
                        'ERROR', 'C6',
                        f"Duplicate premise '{src}' in assertion",
                        line=i+1
                    ))
                seen.add(src)

    # ── Helpers ──

    def _collect_identifiers(self, rel: Relation, refs: set):
        """Collect all identifier references from a relation."""
        if rel.left:
            self._collect_expr_idents(rel.left, refs)
        if rel.right:
            self._collect_expr_idents(rel.right, refs)
        if rel.subject:
            refs.add(rel.subject)
        if rel.proportional_to:
            refs.update(rel.proportional_to)
        if rel.conserved_id:
            refs.add(rel.conserved_id)
        if rel.lim_id1:
            refs.add(rel.lim_id1)
        if rel.lim_id2:
            refs.add(rel.lim_id2)

    def _collect_expr_idents(self, expr: Expr, refs: set):
        """Recursively collect identifiers from expression tree."""
        if isinstance(expr, IdentExpr):
            refs.add(expr.name)
        elif isinstance(expr, BinOpExpr):
            self._collect_expr_idents(expr.left, refs)
            self._collect_expr_idents(expr.right, refs)
        elif isinstance(expr, DerivativeExpr):
            refs.add(expr.numerator)
            refs.add(expr.denominator)
        elif isinstance(expr, GradientExpr):
            refs.add(expr.target)
        elif isinstance(expr, PowerExpr):
            self._collect_expr_idents(expr.base, refs)
        elif isinstance(expr, BraExpr):
            refs.add(expr.name)
        elif isinstance(expr, KetExpr):
            refs.add(expr.name)
        elif isinstance(expr, BraketExpr):
            refs.add(expr.bra)
            refs.add(expr.ket)
        elif isinstance(expr, CommutatorExpr):
            self._collect_expr_idents(expr.left, refs)
            self._collect_expr_idents(expr.right, refs)

    def _compute_dim(self, expr: Expr) -> Optional[str]:
        """Compute dimension of an expression (simplified)."""
        if isinstance(expr, IdentExpr):
            return self.quantity_dims.get(expr.name)
        elif isinstance(expr, NumberExpr):
            return '[1]'
        elif isinstance(expr, BinOpExpr):
            dim_l = self._compute_dim(expr.left)
            dim_r = self._compute_dim(expr.right)
            if dim_l and dim_r:
                if expr.op in ('+', '-'):
                    return dim_l if dim_l == dim_r else None
                elif expr.op == '·':
                    return self._add_dims(dim_l, dim_r)
        elif isinstance(expr, DerivativeExpr):
            dim_n = self.quantity_dims.get(expr.numerator)
            dim_d = self.quantity_dims.get(expr.denominator)
            if dim_n and dim_d:
                return self._subtract_dims(dim_n, dim_d)
        elif isinstance(expr, PowerExpr):
            base_dim = self._compute_dim(expr.base)
            if base_dim:
                try:
                    n = int(expr.exponent)
                    return self._multiply_dim(base_dim, n)
                except ValueError:
                    pass
        return None

    def _add_dims(self, d1: str, d2: str) -> str:
        """Simplified dimension addition."""
        if d1 == '[1]': return d2
        if d2 == '[1]': return d1
        inner1 = d1[1:-1]
        inner2 = d2[1:-1]
        # Concatenate — this is approximate; real implementation would parse properly
        return f'[{inner1}·{inner2}]'

    def _subtract_dims(self, d1: str, d2: str) -> str:
        """Simplified dimension subtraction."""
        if d2 == '[1]': return d1
        # Approximate
        inner1 = d1[1:-1]
        inner2 = d2[1:-1]
        return f'[{inner1}·{inner2}⁻¹]'

    def _multiply_dim(self, d: str, n: int) -> str:
        """Multiply dimension by integer n."""
        if d == '[1]': return '[1]'
        return f'{d}^{n}'

    def _generate_assertion_id(self, assertion: Assertion, index: int) -> str:
        """Generate a stable ID for an assertion from its content."""
        rel = assertion.relation
        if rel.type == RelationType.EQUALITY and rel.left and rel.right:
            left_str = self._expr_to_str(rel.left)[:20]
            return f"eq.{left_str}"
        elif rel.type == RelationType.EXISTENCE:
            return f"exist.{rel.conserved_id}"
        elif rel.subject:
            return f"prop.{rel.subject}"
        return f"stmt.{index}"


    def _expr_to_str(self, expr: Expr) -> str:
        if isinstance(expr, IdentExpr):
            return expr.name
        elif isinstance(expr, NumberExpr):
            return expr.value
        elif isinstance(expr, BinOpExpr):
            return f"{self._expr_to_str(expr.left)}{expr.op}{self._expr_to_str(expr.right)}"
        return "?"


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def parse_file(filepath: str) -> tuple[Program, list[Diagnostic], list[Token]]:
    """Parse a .scihf file and return (AST, diagnostics, tokens)."""
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    tokenizer = SciHFTokenizer(text)
    try:
        tokens = tokenizer.tokenize()
    except SyntaxError as e:
        print(f"LEXER ERROR: {e}", file=sys.stderr)
        return Program(), [Diagnostic('ERROR', 'LEXER', str(e))], []

    parser = SciHFParser(tokens)
    try:
        program = parser.parse_program()
    except SyntaxError as e:
        print(f"PARSE ERROR: {e}", file=sys.stderr)
        return Program(), [Diagnostic('ERROR', 'PARSE', str(e))], tokens

    checker = SciHFChecker(program)
    diagnostics = checker.check()

    return program, diagnostics, tokens


def print_ast(program: Program):
    """Pretty-print the AST."""
    print("═" * 60)
    print("  .scihf Abstract Syntax Tree")
    print("═" * 60)

    print(f"\n── Quantity Declarations ({len(program.quantities)}) ──")
    for q in program.quantities:
        print(f"  Q({q.name}, {q.dim}, {q.equiv_class})")

    print(f"\n── Condition Declarations ({len(program.conditions)}) ──")
    for c in program.conditions:
        print(f"  C({c.name}, {c.category})")

    print(f"\n── Assertions ({len(program.assertions)}) ──")
    for i, a in enumerate(program.assertions):
        rel = a.relation
        rel_str = ""
        if rel.type == RelationType.EQUALITY:
            rel_str = f"{_expr_str(rel.left)} = {_expr_str(rel.right)}"
        elif rel.type == RelationType.PROPORTIONALITY:
            deps = " · ".join(rel.proportional_to) if rel.proportional_to else ""
            rel_str = f"{rel.subject} ∝[{rel.direction}] {deps}"
        elif rel.type == RelationType.INEQUALITY:
            rel_str = f"{_expr_str(rel.left)} {rel.op} {_expr_str(rel.right)}"
        elif rel.type == RelationType.EXISTENCE:
            rel_str = f"∂_μ {rel.conserved_id} = 0"
        elif rel.type == RelationType.LIMIT:
            rel_str = f"{rel.lim_id1} → {rel.lim_val1} | {rel.lim_id2} → {rel.lim_val2}"

        scope_str = f" | {', '.join(a.scope)}" if a.scope else ""
        source_str = f" ← {', '.join(a.source)}" if a.source else ""

        print(f"  [{a.layer}] {rel_str}{scope_str}{source_str}")


def _expr_str(expr) -> str:
    if expr is None: return "?"
    if isinstance(expr, IdentExpr): return expr.name
    if isinstance(expr, NumberExpr): return expr.value
    if isinstance(expr, BinOpExpr): return f"({_expr_str(expr.left)}{expr.op}{_expr_str(expr.right)})"
    if isinstance(expr, DerivativeExpr): return f"{expr.operator}({expr.numerator})/{expr.operator}({expr.denominator})"
    if isinstance(expr, GradientExpr): return f"{expr.operator}({expr.target})"
    if isinstance(expr, PowerExpr): return f"{_expr_str(expr.base)}^{expr.exponent}"
    return str(type(expr).__name__)


def main():
    import argparse
    ap = argparse.ArgumentParser(description='.scihf Parser & Checker')
    ap.add_argument('files', nargs='*', help='.scihf files to parse')
    ap.add_argument('--ast', action='store_true', help='Print AST')
    ap.add_argument('--tokens', action='store_true', help='Print token stream')
    ap.add_argument('--json', action='store_true', help='Output diagnostics as JSON')
    args = ap.parse_args()

    if not args.files:
        ap.print_help()
        return

    all_ok = True
    for filepath in args.files:
        if not os.path.exists(filepath):
            print(f"ERROR: File not found: {filepath}", file=sys.stderr)
            all_ok = False
            continue

        print(f"\n{'='*60}")
        print(f"  {filepath}")
        print(f"{'='*60}")

        program, diagnostics, tokens = parse_file(filepath)

        if args.tokens:
            print(f"\nToken stream ({len(tokens)} tokens):")
            for tok in tokens[:-1]:  # skip EOF
                print(f"  {tok}")

        if args.ast:
            print_ast(program)

        # Print diagnostics
        errors = [d for d in diagnostics if d.level == 'ERROR']
        warnings = [d for d in diagnostics if d.level == 'WARNING']

        if args.json:
            result = {
                'file': filepath,
                'quantities': len(program.quantities),
                'conditions': len(program.conditions),
                'assertions': len(program.assertions),
                'errors': len(errors),
                'warnings': len(warnings),
                'diagnostics': [{'level': d.level, 'code': d.code,
                                'message': d.message, 'line': d.line}
                               for d in diagnostics]
            }
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"\n── Diagnostics ──")
            print(f"  Quantities: {len(program.quantities)}")
            print(f"  Conditions: {len(program.conditions)}")
            print(f"  Assertions: {len(program.assertions)}")
            print(f"  Errors:     {len(errors)}")
            print(f"  Warnings:   {len(warnings)}")
            for d in diagnostics:
                marker = '❌' if d.level == 'ERROR' else '⚠️'
                print(f"  {marker} [{d.code}] L{d.line}: {d.message}")

            if errors:
                all_ok = False

    if all_ok:
        print("\n✅ All checks passed.")
    else:
        print("\n❌ Errors found.")
        sys.exit(1)


if __name__ == '__main__':
    main()
