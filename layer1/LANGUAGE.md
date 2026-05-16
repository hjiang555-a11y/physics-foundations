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
            ← law.pauli_exclusion, kernel.boltzmann_entropy
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

---

## 6. 物理描述方法 (Description Methodology)

本节是从 R1–R6 精炼和 32 条定理推导的迭代过程中提取的语言描述方法。
目标：任何物理陈述（规则、定理、推导）在写入 corpus 时必须满足以下结构规范。

### 6.1 规则描述范式 (Rule Description Template)

每条核心规则 (R1–R6) 的完整描述需包含以下 8 个组件：

| # | 组件 | 英文 | 内容要求 |
|---|------|------|---------|
| 1 | **陈述** | Statement | 一句话精确陈述规则内容，不含歧义符号或未定义术语 |
| 2 | **变量表** | Variables | 每个变量：符号 (symbol)、类型 (type)、量纲 (dim)、定义域 (domain)、物理含义 (meaning)。格式见 6.3 |
| 3 | **数学表达式** | Mathematical Expression | 精确的数学公式；所有符号必须已在变量表中定义；量纲自洽 |
| 4 | **成立条件** | Scope | 规则适用的物理条件（如 inertial_frame, quantum_regime）。使用 scope 标签 |
| 5 | **失效边界** | Boundary | 规则失效的条件（如 Planck 尺度）。明确标注边界值与机制 |
| 6 | **必要性** | Necessity | 表格形式：若移除或弱化该规则的任一部分，哪些已确认的物理现象将被推翻 |
| 7 | **充分性** | Sufficiency | 该规则 + 前序规则组合，可覆盖的物理现象域与可导出的定理集合 |
| 8 | **子组件映射** | Sub-component Mapping | 规则与 `frameworks.yaml` 中 kernel.* / rule.* 的对应关系 |

**必要性论证的格式**：

| 移除/弱化 | 后果 |
|-----------|------|
| 具体可量化的移除操作 | 可检验的物理后果（非泛泛而谈） |

**充分性论证的格式**：

```
R(N) + R(M)（+ 其他前提）提供：
- 可导出的现象 1
- 可导出的现象 2
```

### 6.2 定理推导范式 (Theorem Derivation Template)

每条从 R1–R6 推出的定理，其推导在 `rigorous_derivations.yaml` 中需包含以下组件：

| # | 字段 | 内容 |
|---|------|------|
| id | `deriv.<name>` | 唯一推导标识 |
| conclusion | `law.<name>` 或 `cor.<name>` | 推导得到的定理 ID |
| conclusion_statement | 数学表达式 | 定理的精确陈述 |
| premise | `[kernel.*, law.*, ...]` | 逻辑前提列表（必须可追溯至 R1–R6） |
| variables | 变量列表 | 每变量包含 symbol, type, dim, domain, meaning |
| steps | 步骤列表 | 每步包含: step 编号, description, expression, justification, condition [N] |
| result | 文本 | 推导结果总结 |
| necessity_conditions | 列表 | 每步中的 [N] 条件汇总 |
| sufficiency_conditions | 列表 | 从前提 ⇒ 结论的充分性声明 |
| reversible | true/false | 结论是否能反推前提 |
| reverse_note | 文本 | 不可逆时的说明 |
| validity_scope | 标签列表 | 定理成立的物理条件 |
| mathematical_link | 符号链 | 从前提 → 结论的符号压缩路径 |

**推导步骤的格式**（每步）：

```yaml
- step: N
  description: "做什么操作"
  expression: "数学表达式"
  justification: "为什么这一步合法（引用 R1–R6 或 prior theorem）"
  condition: "[N] 若移除该条件，此步断裂"
```

### 6.3 变量定义规范 (Variable Definition Convention)

每个物理变量必须包含全部 5 个字段，无一可省：

| 字段 | 含义 | 示例 |
|------|------|------|
| `symbol` | 数学符号（LaTeX 兼容） | `$S$`, `$\\psi(r)$`, `$g_{\\mu\\nu}$` |
| `type` | 数学类型 | `$\\mathbb{R}$`, `$\\mathbb{R}^3$`, `$\\mathcal{H}$ 上厄米算符`, `泛函`, `常数` |
| `dim` | 量纲（SI 7 维向量表示） | `[M·L²·T⁻¹]`, `[1]`（无量纲）, `[L⁻²]` |
| `domain` | 定义域 / 取值范围 | `$t \\in \\mathbb{R}$`, `$\\|\\psi\\rangle\\| = 1$`, `$v \\in [0, c)$` |
| `meaning` | 物理含义（30 字内） | 只用已定义的术语描述 |

**类型体系**（用于 `type` 字段）：

| 类型 | 记法 | 说明 |
|------|------|------|
| 实数 | $\mathbb{R}$ | 单个实数值 |
| 实数向量 | $\mathbb{R}^D$ | D 维向量 |
| 复数 | $\mathbb{C}$ | 单个复数值 |
| 自然数 | $\mathbb{N}$ | 非负整数 |
| 正整数 | $\mathbb{N}^+$ | 正整数 |
| 矩阵 | $\mathbb{R}^{m \times n}$ | 实数矩阵 |
| Hilbert 空间向量 | $\mathcal{H}$ 中向量 | 量子态 |
| Hilbert 空间算符 | $\mathcal{H}$ 上厄米算符 | 可观测量 |
| 泛函 | 泛函 $\mathbb{R} \to \mathbb{R}$ | 作用量等 |
| 函数 | 定义域 $\to$ 值域 | 如 $\mathbb{R}^3 \to \mathbb{R}$ |
| 常数 | 常数 | 物理常数（非变量） |

### 6.4 充分必要性标注语言 (Necessity/Sufficiency Annotation)

在推导步骤中，使用以下标记语言：

| 标记 | 含义 | 语法 |
|------|------|------|
| `[N]` | **Necessary** — 此条件若不成立，推导在该步骤断裂，结论不可达 | `condition: "[N] 说明"` |
| `[S]` | **Sufficient** — 给定这些条件，结论必然成立 | 在 `sufficiency_conditions` 列表中 |
| `reversible: true` | **双向等价** — 结论 ⇔ 前提（可互推） | Boolean |
| `reversible: false` | **单向** — 前提 ⇒ 结论，但结论 ⇏ 前提 | Boolean + `reverse_note` 说明 |

**必要性检查清单**（submit 前逐条通过）：
1. 每一步的 `condition: [N]` 是否确实不可移除？
2. 是否存在隐式假设（如可微性、连续性、遍历性）未标注 [N]？
3. 所有 [N] 条件是否可追溯至 R1–R6 或已证定理？

**充分性检查清单**：
1. `sufficiency_conditions` 中的前提集是否涵盖了推导的所有步骤？
2. 是否存在"gap"——某步未在前提中声明但推导中使用了？
3. 放宽任一前提是否必然导致反例？

### 6.5 语言完备性迭代协议 (Completeness Iteration Protocol)

R1–R6 与全部定理的完整性通过以下迭代达成：

```
Round N:
  1. 从当前 R1–R6 出发，尝试推导全部定理
  2. 对每条定理，逐步检查：
     a. 每步的 justification 是否可追溯至 R1–R6 或 prior theorem？
     b. 每步中引用的变量是否已在 R1–R6 或本定理中定义？
     c. 是否存在隐式假设（如 Lagrangian 的具体形式、单位制）未声明？
  3. 若发现缺口 → 回到 R1–R6 补充或明确标注为 contingent
  4. 若全部可推且无新增缺口 → 迭代收敛，结束
  5. 否则 → Round N+1

停止条件: 连续两轮无变动，或修复数降至 0
```

**实践经验**（9 轮迭代数据）：
- 第 1–3 轮：结构性问题（缺失字段、缺失推导、单位矛盾）——每轮 10–15 个修复
- 第 4–5 轮：逻辑精度问题（scope 矛盾、错误失效条目、哲学诠释）——每轮 5–11 个修复
- 第 6–7 轮：数学符号错误（度规升降、Levi-Civita、单位混合）——每轮 1–4 个修复
- 第 8–9 轮：表述一致性（常数溯源、等价声明）——每轮 2 个修复
- 收敛模式：发现数随迭代轮次递减，深度增加（从结构 → 逻辑 → 数学 → 表述）

### 6.6 语言分层 (Language Layer Architecture)

```
Layer 0: Token (词法)        — KEYWORD, IDENT, NUMBER, DIMENSION, RELATION, CALC, PUNCT
Layer 1: Node (语法)         — Program, QuantityDecl, ConditionDecl, Assertion, ...
Layer 2: Constraint (语义)   — 引用完整、量纲一致、层次序、无环、根可达
Layer 3: Description (描述)  — 规则描述范式 (6.1), 推导范式 (6.2), 变量规范 (6.3)
Layer 4: Verification (验证) — V1–V5 source graph, 必要/充分性自动检查, 量纲代数
```

Layer 0–2 由 `.scihf` 语法和 checker 实现。
Layer 3–4 由 `rules.md`（人读）和 `rigorous_derivations.yaml`（机验）共同实现。
两个文件通过 `id` 引用互操作：rules.md 的 R1–R6 对应 frameworks.yaml 的 `kernel.*`；rigorous_derivations.yaml 的 `premise` 引用 kernel/law ids。

### 6.7 迭代实践中发现的补充规则 (Practical Rules from Iteration)

以下规则在 9 轮迭代中作为反复出现的错误模式被识别，追加为语言描述方法的一部分。

#### R-A. 单位一致性 (Unit Consistency)

**规则**: 同一数学表达式中的所有项必须使用相同的单位制。混合自然单位 ($\hbar=c=1$) 与 SI 单位 ($\mu_0$, $\varepsilon_0$) 在同一 Lagrangian 中是被禁止的。

**违反示例**: $\mathcal{L} = \bar{\psi}(i\gamma^\mu D_\mu - m)\psi - \frac{1}{4\mu_0}F^2$ —— Dirac 部分用自然单位，规范部分用 SI。

**合规**: 明确标注单位制选择，或提供恢复完整单位的转换规则。

#### R-B. 度规符号一致性 (Metric Signature Consistency)

**规则**: 度规符号约定 $(+,-,-,-)$ 或 $(-,+,+,+)$ 必须在文件开头声明一次，并在所有指标升降操作中一致应用。

**关键陷阱**: 在 $(+,-,-,-)$ 下，空间指标的升降引入负号。当涉及反对称张量时，两个负号可能抵消：
$$F^{i0} = g^{ii}g^{00}F_{i0} = (-1)(1)F_{i0} = -F_{i0} = -(-F_{0i}) = F_{0i}$$
推导中常见的错误是直接写 $F^{i0} = -F_{0i}$ 而忽略了 $F_{i0} = -F_{0i}$ 的抵消。

#### R-C. 等價表述声明 (Equivalence Declaration)

**规则**: 当同一个物理事实存在多个等价的数学表述时，必须：
1. 明确声明等价性
2. 给出等价性证明（符号推导链）
3. 选择一个作为主要表述，其余作为等价变体

**示例**: R1.1 中"最大传播速度"与"Lorentz 因果结构"的等价性——它们通过 $ds^2 = c^2dt^2 - |d\mathbf{r}|^2$ 连接，类空 $\iff |d\mathbf{r}|/dt > c$。

#### R-D. 常数溯源 (Constant Provenance)

**规则**: 每个物理常数在 corpus 中首次出现时，必须声明其定义来源——来自哪个规则（如 $c \in$ R1, $\hbar \in$ R4, $k_B \in$ R6）、哪个推导（如 $G$ 由 Einstein 场方程的 Newton 极限引入），还是实验测量（如 $\alpha$ 精细结构常数）。

#### R-E. Contingent vs. Necessary 分类

**规则**: 规则陈述中的每条声明必须标注其逻辑地位：
- **逻辑必然**：从规则本身或前序规则可推出
- **Contingent 事实**：本宇宙的实验观测值，不由 R1-R6 决定（如 $D=3$、规范群选择、标准模型参数）

在变量表中，contingent 事实的 `domain` 字段应标注"本宇宙 contingent 事实"。

### 6.8 完整描述语言检查清单 (Complete Description Language Checklist)

提交前逐条通过：

**规则层 (R1-R6)**:
- [ ] 8 组件全部存在（陈述、变量表、数学表达式、Scope、Boundary、必要性、充分性、子组件映射）
- [ ] 变量表：5 字段完整（symbol/type/dim/domain/meaning）
- [ ] 单位制一致（同一表达式不混合单位制）
- [ ] 度规符号约定已声明且一致应用
- [ ] Scope 不自称"普遍适用"（必须在 Planck 尺度以上）
- [ ] Boundary 中使用的常数已交叉引用定义来源
- [ ] 必要性表格：每个条目具体可量化
- [ ] Contingent/Necessary 分类正确

**推导层 (rigorous_derivations.yaml)**:
- [ ] 13 字段全部存在
- [ ] 每步有 justification（引用 R1-R6 或 prior theorem）
- [ ] 每步中关键条件标注 [N]
- [ ] 所有变量在 derivation 的 variables 段或引用规则中定义
- [ ] 指标升降操作已验证（度规符号 + 反对称性）
- [ ] 最终结果与已知物理定律符号一致

**跨文件一致性**:
- [ ] premise 引用的 ID 在 frameworks.yaml 或 effective_laws.yaml 中存在
- [ ] conclusion 引用的 ID 在 effective_laws.yaml 中存在
- [ ] 推导图中无环
- [ ] 所有 kernel.* ID 在 rules.md 中有对应描述
- [ ] constants 溯源完整（见 R-D）
