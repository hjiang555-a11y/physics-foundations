# sci-hf 科学描述语言规范

**目的**: 为一门科学推理提供无歧义的描述语言。每一段合法的语言字符串，恰好一种解析，恰好一个意义。

**Phase 7 最小实现边界**: 先覆盖 `physics.scihf` 已出现的声明形态，验证引用完整性、量纲一致性、source 层次序与 scope 可解析性；完整数学表达式 parser、全量微积分语义与跨文件增量编译列为后续范围。YAML / `.scihf` 的确定性提取顺序见 [`EXTRACTION.md`](EXTRACTION.md)，科学描述语言的充分必要规则见 [`../../docs/scientific-description-language-rules.md`](../../docs/scientific-description-language-rules.md)。

---

## 0. Token 规范（词法层）

Token 是词法分析器从源文本中切分出的最小有意义的语言单位。
一个 token 携带类型和字面值。

### 0.1 Token 类型（7 类）

| # | Token 类型 | 描述 | 示例 |
|---|-----------|------|------|
| T1 | **KEYWORD** | 声明导引符、层标记 | `Q`, `C`, `kernel`, `rule`, `contingent`, `effective_law`, `law`, `corollary` |
| T2 | **IDENT** | 标识符（量名、条件名、常量名），含希腊字母和Unicode下标 | `time`, `qty.force`, `ħ`, `Δs²`, `r₁`, `ψ` |
| T3 | **NUMBER** | 整数或浮点数，可选科学记数法 | `0`, `1`, `3.14`, `6.626e-34`, `299792458` |
| T4 | **DIMENSION** | 量纲字面量 | `[T]`, `[M·L·T⁻²]`, `[1]` |
| T5 | **RELATION** | 关系运算符 | `=`, `∝[+]`, `∝[-]`, `≠`, `≥`, `≤` |
| T6 | **CALC** | 微积分算子 | `d`, `∂`, `∇`, `∇·`, `∇×`, `∫`, `∂_μ` |
| T7 | **PUNCT** | 分隔符、结构符号 | `[`, `]`, `(`, `)`, `|`, `←`, `,`, `·`, `+`, `-`, `/`, `^` |

### 0.2 Token 识别规则

```
KEYWORD    ::= "Q" | "C" | "kernel" | "rule" | "contingent" | "effective_law" | "law" | "corollary"
IDENT      ::= [a-zα-ωħδΔ][a-zA-Z0-9α-ωΑ-ΩħδΔ_\.₀-₉]*
NUMBER     ::= digit+ ["." digit*] ["e" ["-"] digit+]
DIMENSION  ::= "[" dim-term { "·" dim-term } "]"
RELATION   ::= "=" | "∝[+]" | "∝[-]" | "≠" | "≥" | "≤"
CALC       ::= "d" | "∂" | "∇" | "∇·" | "∇×" | "∫" | "∂_μ"
PUNCT      ::= "[" | "]" | "(" | ")" | "|" | "←" | "," | "·" | "+" | "-" | "/" | "^"
```

注释: `#` 到行尾为注释，lexer 丢弃。空白（空格、换行、制表符）为分隔符，lexer 丢弃。

### 0.3 Token 流示例

```
源文本:  Q(time, [T], time)

Token 流:
  KEYWORD:"Q"  PUNCT:"("  IDENT:"time"  PUNCT:","  DIMENSION:"[T]"  PUNCT:","  IDENT:"time"  PUNCT:")"
```

---

## 1. Node 规范（语法层）

Node 是 parser 从 token 流中构建的抽象语法树（AST）节点。
每个 node 携带类型、子节点、以及类型检查所需的元数据。

### 1.1 Node 类型（8 类）

| # | Node 类型 | 对应 BNF 产生式 | 描述 |
|---|----------|----------------|------|
| N1 | **Program** | `program` | 根节点：声明列表 + 断言列表 |
| N2 | **QuantityDecl** | `quantity-decl` | 物理量声明：名称、量纲、等价类 |
| N3 | **ConditionDecl** | `condition-decl` | 作用域条件声明：名称、类别 |
| N4 | **Assertion** | `stmt` | 断言语句：层标记 + 关系 + 域 + 来源 |
| N5 | **Relation** | `assertion` | 核心语义关系（等式/比例/不等式/连续性/极限） |
| N6 | **Expr** | `expr` | 数学表达式树（算术、微积分、幂） |
| N7 | **Scope** | `scope` | 作用域约束：该断言在哪些条件下成立 |
| N8 | **Source** | `source` | 推导来源：该断言从哪些父声明推出 |

### 1.2 Node 层次结构

```
Program  (N1)
  ├── QuantityDecl  (N2) × N     — Q(name, dim, class)
  ├── ConditionDecl (N3) × N     — C(name, category)
  └── Assertion     (N4) × N
        ├── layer:   KEYWORD     — "kernel"|"rule"|"contingent"|"effective_law"|"law"|"corollary"
        ├── Relation (N5)        — 核心语义
        │     ├── Equality       — Expr = Expr
        │     ├── Proportionality — IDENT ∝[dir] IDENT {· IDENT}
        │     ├── Inequality     — Expr (≥|≤) Expr
        │     ├── Existence      — ∂_μ IDENT = 0
        │     └── Limit          — IDENT → NUMBER | IDENT → NUMBER
        ├── Scope   (N7)?        — | cond₁, cond₂, ...
        └── Source  (N8)?        — ← parent₁, parent₂, ...
```

### 1.3 Relation 子类型（N5 的 5 种变体）

| 子类型 | 语法 | 语义 | 示例 |
|--------|------|------|------|
| **Equality** | `expr₁ = expr₂` | 数值相等 | `F = m·d(v)/d(t)` |
| **Proportionality** | `id ∝[dir] id · id` | 单调依赖 | `S_y ∝[+] T` |
| **Inequality** | `expr₁ (≥\|≤) expr₂` | 上下界约束 | `σ_x·σ_p ≥ ħ/2` |
| **Existence** | `∂_μ id = 0` | 连续性/守恒 | `∂_μ J^μ = 0` |
| **Limit** | `id₁ → n₁ \| id₂ → n₂` | 极限行为 | `S → 0 \| T → 0` |

---

## 2. 语法 Grammar（BNF）

```
program         ::= decl* stmt*                           ;; → Program(N1)

;; ── 声明: N2, N3 ──
decl            ::= quantity-decl | condition-decl

quantity-decl   ::= "Q" "(" id "," dim "," class ")"     ;; → QuantityDecl(N2)
condition-decl  ::= "C" "(" id "," category ")"           ;; → ConditionDecl(N3)

dim             ::= "[" dim-term { "·" dim-term } "]"
dim-term        ::= dim-symbol ["^" exponent]
dim-symbol      ::= "L" | "M" | "T" | "I" | "Θ" | "N" | "J" | "1"
exponent        ::= ["-"] digit+
category        ::= id
class           ::= id

;; ── 断言: N4 ──
stmt            ::= "[" layer "]" assertion [scope] [source]  ;; → Assertion(N4)

layer           ::= "kernel" | "rule" | "contingent" | "effective_law" | "law" | "corollary"

;; ── 关系: N5 ──
assertion       ::= equality                                ;; → Equality
                  | proportionality                        ;; → Proportionality
                  | inequality                             ;; → Inequality
                  | existence                              ;; → Existence
                  | limit                                  ;; → Limit

equality        ::= expr "=" expr                           ;; → Equality(N5a)
proportionality ::= id "∝[" dir "]" id { "·" id }+          ;; → Proportionality(N5b)
inequality      ::= expr ("≥" | "≤") expr                   ;; → Inequality(N5c)
existence       ::= "∂_μ" id "= 0"                          ;; → Existence(N5d)
limit           ::= id "→" number "|" id "→" number         ;; → Limit(N5e)

;; ── 表达式: N6 ──
expr            ::= term { ("+" | "-") term }               ;; → Expr(N6)
term            ::= factor { "·" factor }
factor          ::= id
                  | number
                  | "d(" id ")/d(" id ")"
                  | "∂(" id ")/∂(" id ")"
                  | "∇·(" id ")"
                  | "∇×(" id ")"
                  | "∇(" id ")"
                  | "ket(" id ")"                           ;; 量子态右矢 |ψ⟩
                  | "bra(" id ")"                           ;; 量子态左矢 ⟨ψ|
                  | "braket(" id "," id ")"                 ;; 内积 ⟨φ|ψ⟩
                  | "comm(" expr "," expr ")"               ;; 对易子 [A,B]
                  | id "^" exponent
                  | id "/" id
                  | "(" expr ")"
                  | number "/" "(" expr ")"

;; ── 修饰: N7, N8 ──
scope           ::= "|" id { "," id }                       ;; → Scope(N7)
source          ::= "←" id { "," id }                       ;; → Source(N8)
dir             ::= "+" | "-"
id              ::= [a-zα-ωħδΔ][a-zA-Z0-9α-ωΑ-ΩħδΔ_\.₀-₉]*
number          ::= digit+ ["." digit*] ["e" ["-"] digit+]
digit           ::= "0".."9"
```

---

## 3. 语义 Semantics

### 3.1 Node 间的语义关系

| 关系 | 涉及 Node | 约束 |
|------|----------|------|
| **声明绑定** | Expr 中的 IDENT → QuantityDecl / ConditionDecl | 所有引用的 id 必须在 Program 的 decl 列表中声明 |
| **量纲一致性** | Equality(N5a) 的左右 Expr | `dim(expr_left) = dim(expr_right)` |
| **层次序** | Assertion(N4) 的 Source → 另一 Assertion | kernel 的 source 为空；law 的 source 指向 kernel 或 law；corollary 的 source 指向 law 或 corollary |
| **等价类分离** | Expr 中的两个 IDENT → 各自的 QuantityDecl | 若量纲相同但 class 不同 → 警告 ACCIDENTAL_COLLISION |
| **域继承** | Assertion 的 Scope 向下传播 | 子推导继承父推导的所有 scope 条件，除非显式覆盖 |

说明：`rule` 与 `effective_law` 是 YAML 存储层使用的稳定 layer；`.scihf` 示例可继续使用较短的 `[law]` 作为人读形式。提取器按 `EXTRACTION.md` 将二者映射到同一 source graph 约束集合。

### 3.2 量纲代数

```
dim(NUMBER)         = [1]                 (纯数，无量纲)
dim(IDENT)          = dim(Q的 dim 字段)    (从 QuantityDecl 查找)
dim(expr₁ + expr₂)  = dim(expr₁)          (要求 dim(expr₁) = dim(expr₂))
dim(expr₁ - expr₂)  = dim(expr₁)          (要求 dim(expr₁) = dim(expr₂))
dim(expr₁ · expr₂)  = dim(expr₁) + dim(expr₂)
dim(expr₁ / expr₂)  = dim(expr₁) - dim(expr₂)
dim(expr^N)         = dim(expr) × N
dim(d(id₁)/d(id₂))  = dim(id₁) - dim(id₂)
dim(∂(id₁)/∂(id₂))  = dim(id₁) - dim(id₂)
dim(∇(id))          = dim(id) - [L]
dim(∇·(id))         = dim(id) - [L]
dim(∇×(id))         = dim(id) - [L]
dim(∫ expr d(id))   = dim(expr) + dim(id)
```

### 3.3 断言语义

| 断言类型 | 含义 |
|----------|------|
| `expr₁ = expr₂` | 在所有满足 scope 的条件下，两表达式数值相等 |
| `A ∝[+] B · C` | A 随 B 和 C 严格单调递增；∂A/∂B > 0, ∂A/∂C > 0 |
| `A ∝[-] B` | A 随 B 严格单调递减；∂A/∂B < 0 |
| `expr₁ ≥ expr₂` | 下界约束（如不确定性原理） |
| `∂_μ J = 0` | 连续性方程 — J 的四维散度处处为零 |
| `A → n₁ \| B → n₂` | 当 B 趋近于 n₂ 时，A 趋近于 n₁ |

---

## 4. 示例 Examples

```
# ── 向量声明: Q() → QuantityDecl(N2), C() → ConditionDecl(N3) ──

Q(time, [T], time)
Q(length, [L], geometric_length)
Q(mass, [M], inertial_mass)
Q(force, [M·L·T⁻²], force)
Q(momentum, [M·L·T⁻¹], momentum)
Q(energy, [M·L²·T⁻²], energy)
Q(entropy, [M·L²·T⁻²·Θ⁻¹], entropy)
Q(temperature, [Θ], thermodynamic_temperature)
Q(electric_charge, [T·I], electric_charge)
Q(electric_field, [M·L·T⁻³·I⁻¹], electric_field)
Q(magnetic_field, [M·T⁻²·I⁻¹], magnetic_flux_density)
Q(current_density, [L⁻²·I], current_density)
Q(action, [M·L²·T⁻¹], action)
Q(spin, [1], quantum_spin)

C(inertial_frame, reference_frame)
C(thermal_equilibrium, physical_regime)
C(isolated_system, system_boundary)
C(classical_limit, quantum_classical_boundary)
C(quantum_regime, quantum_classical_boundary)
C(conservative_force, force_type)

# ── Assertion(N4): [layer] Relation(N5) [Scope(N7)] [Source(N8)] ──

[kernel] δS = 0            ;; Equality(N5a), layer=kernel, source=empty

[law] F = d(p)/d(t)        ;; Equality(N5a), layer=law
      | inertial_frame, classical_limit     ;; Scope(N7)
      ← kernel.least_action, law.euler_lagrange  ;; Source(N8)

[law] ∇·(E) = ρ_q / ε₀     ;; Equality(N5a) with calc operators

[law] ∇·(B) = 0            ;; Equality(N5a)

[law] ∇×(E) = -∂(B)/∂(t)   ;; Equality(N5a) with calc and derivative

[law] ∇×(B) = μ₀·J + μ₀·ε₀·∂(E)/∂(t)

[law] E = h·ν              ;; Equality(N5a) — Planck-Einstein relation

[law] σ_x·σ_p ≥ ħ/2        ;; Inequality(N5c) — uncertainty

[law] dU = T·dS - P·dV | thermal_equilibrium
      ← law.noether_theorem, kernel.boltzmann_entropy

[law] S → 0 | T → 0        ;; Limit(N5e) — third law

[law] E = m·c^2             ;; Equality(N5a) — mass-energy

[law] ∂_μ T^μν = 0 | isolated_system    ;; Existence(N5d)

[law] ∂_μ J = 0             ;; Existence(N5d) — charge conservation

[law] S ∝[+] T | thermal_equilibrium     ;; Proportionality(N5b)
[law] S ∝[-] L | thermal_equilibrium

[corollary] T^2 ∝[+] r^3    ;; Proportionality(N5b), layer=corollary
            ← law.newton_second, law.newton_gravitation

[corollary] f(E) = 1 / (exp((E - μ) / (k_B·T)) + 1)
            ← kernel.pauli_exclusion, kernel.boltzmann_entropy
```

---

## 5. 一致性约束

Parser 在构建 AST 后强制以下约束（实现为 checker pass）。

### 5.1 基本约束

| # | 约束 | 检查方式 |
|---|------|---------|
| C1 | **引用完整性** | 遍历所有 Expr(N6) 和 Scope(N7) / Source(N8) 中的 IDENT，验证其在 Program(N1) 的 decl 列表中声明 |
| C2 | **量纲一致性** | 对每个 Equality(N5a)，计算左右 Expr 的 dim，验证相等 |
| C3 | **层次序** | 遍历 Assertion(N4) 的 Source(N8)：kernel 的 source 为空；law 的 source 只含 kernel 或 law id；corollary 的 source 只含 law 或 corollary id |
| C4 | **等价类分离** | 遍历 Expr 中的 IDENT 对：若 dim 相同但 class 不同，发出 ACCIDENTAL_COLLISION 警告 |
| C5 | **域一致性** | 若 parent Scope 声明了某条件但 child 未声明，child 继承该条件 |
| C6 | **重复前提禁止** | 同一 `derived_from` / `premise` / `←` 列表内不得重复同一 ID |

### 5.2 Source 推导图约束

Source 节点 (N8, `←`) 在知识库中构建**推导有向图**。除 C3 的层次序外，checker 还需强制执行以下图论约束。完整规范见 [`SOURCE.md`](SOURCE.md)。

| # | 约束 | 含义 | 失败后果 |
|---|------|------|---------|
| V1 | **引用解析** | 所有 `←` 后的 ID 必须指向存在的 Assertion | 拒绝加载 |
| V2 | **无环性** | 推导图中不存在环路（无循环论证） | 拒绝加载 |
| V3 | **层次序** | 同 C3，形式化为图论约束 | 拒绝加载 |
| V4 | **根可达性** | 每条 law/corollary 存在到达 kernel 的路径 | 拒绝加载 |
| V5 | **Source-Derivation 一致性** | 若存在 Derivation 条目，premise 集必须与 source 集一致 | 警告 |
