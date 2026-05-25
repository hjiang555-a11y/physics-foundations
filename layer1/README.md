# Reference layer1

`reference/layer1` 是 Sci-hf 第一阶段的可机验内核区。它只把物理学最基本、当前 corpus 内不可再推导的原理或前提放入 `kernel` / `rule` 根；Noether、Euler-Lagrange、Newton/Maxwell/Schrödinger 等定理或有效定律必须从这些根节点推出。

`reference/rules.md` 是人读准则：R1-R6 是物理世界最底层的 6 条核心原则；每条包含描述、数学表达式与变量说明。Noether 定理和自旋-统计定理是 R2/R4 的数学推论，不列为独立规则。完整科学描述语言规则见 `../docs/scientific-description-language-rules.md`。

## 文件职责

| 文件 | 职责 |
|---|---|
| `frameworks.yaml` | `kernel.*` 根节点与 `rule.*` 结构性元规则。只保存不可由当前 corpus 内更深层可信前提推出的物理前提 / 构造规则。 |
| `contingent.yaml` | 我们宇宙中仍归为经验事实的内容，以及从 kernel/rule/contingent 推出的结构后果。 |
| `effective_laws.yaml` | 从 kernel / rule / law 推出的有效定律、数学定理化表达与过渡期 `cor.*` 推论。 |
| `derivations.yaml` | `premise[]` 到 `conclusion` 的推导步骤，必须与对应 `derived_from[]` 集合一致。 |
| `quantities_registry.yaml` | 物理量、常数、scope、scope alias 与 discontinuity 注册。 |
| `claims.yaml` | 面向 checker 的归一化声明表。 |
| `physics.scihf` | `.scihf` 最小语言样例语料。 |
| `LANGUAGE.md` | `.scihf` token、AST node、grammar、semantics 与 checker 约束。 |
| `SOURCE.md` | `←` / `derived_from` / `premise` 的 source graph 语义与 V1–V5。 |
| `EXTRACTION.md` | YAML / `.scihf` 到 token、node、edge 的确定性提取规则。 |

## Layer1 边界

- `kernel`：物理理论推导图根节点；不得有 `derived_from`。例如 `kernel.least_action`、`kernel.spacetime_dimensionality`。
- `rule`：结构性元规则；作为 foundational 依赖参与检查，但不是物理定理。
- `effective_law` / `law`：从 kernel/rule/law 推出的定理化表达或有效定律。`law.noether_theorem` 位于此层，不再是 kernel 根。
- `contingent`：我们宇宙的经验事实；派生 contingent 必须显式列出 `derived_from`。
- `quantity` / `condition`：量、常数、scope 条件与别名注册，不直接作为 V1–V5 source graph 的 law/kernel 节点。

## Token 描述

### YAML / source graph token

| Token | 来源字段 | 含义 |
|---|---|---|
| `id` | `id` / `conclusion` / `derived_from` / `premise` | 稳定引用标识，必须唯一可解析。 |
| `namespace` | `kernel.*` / `rule.*` / `law.*` / `cor.*` / `contingent.*` / `qty.*` / `cst.*` | 节点命名空间。 |
| `layer` | `layer` | 节点层：`kernel`、`rule`、`contingent`、`effective_law`、`law`、`corollary`、`quantity`、`condition`。 |
| `relation` | `relation` / `.scihf` assertion | 科学关系文本或语言断言。 |
| `quantity_ref` | `quantities[]` / `Q(...)` | 物理量或常数引用。 |
| `scope_ref` | `scope[]` / `C(...)` / `under[]` | 作用域或条件引用。 |
| `source_ref` | `derived_from[]` / `premise[]` / `←` | 逻辑前提引用，参与 source graph。 |
| `provenance` | `provenance` / `sources[]` | 文献或知识来源，不参与推导图。 |
| `derivation_step` | `steps[]` | 推导过程文本。 |

### `.scihf` lexical token

| Token 类型 | 描述 | 示例 |
|---|---|---|
| `KEYWORD` | 声明导引符、层标记 | `Q`, `C`, `kernel`, `rule`, `law` |
| `IDENT` | 量名、条件名、常量名或稳定 ID | `qty.force`, `ψ`, `Δs²` |
| `NUMBER` | 数值字面量 | `0`, `3.14`, `6.626e-34` |
| `DIMENSION` | 量纲字面量 | `[T]`, `[M·L·T⁻²]`, `[1]` |
| `RELATION` | 关系运算符 | `=`, `∝[+]`, `≥`, `≤` |
| `CALC` | 微积分算子 | `d`, `∂`, `∇`, `∇·`, `∇×`, `∫`, `∂_μ` |
| `PUNCT` | 分隔符与结构符号 | `[`, `]`, `(`, `)`, `←`, `,`, `·` |

## Node 描述

| Node | 存储位置 | 主键 | 说明 |
|---|---|---|---|
| `QuantityNode` | `quantities_registry.yaml` / `claims.yaml` / `.scihf Q(...)` | `qty.*` / `cst.*` | 可被 assertion 引用的物理量与常数。 |
| `ConditionNode` | `quantities_registry.yaml` / `claims.yaml` / `.scihf C(...)` | condition id | scope 可解析条件。 |
| `KernelNode` | `frameworks.yaml:kernels[]` | `kernel.*` | 推导图根节点；不得声明 `derived_from`。 |
| `RuleNode` | `frameworks.yaml:structural_rules[]` | `rule.*` | 结构性元规则；可作为 foundational source。 |
| `ContingentNode` | `contingent.yaml:contingent_facts[]` | `contingent.*` | 经验事实；派生项必须声明 source。 |
| `EffectiveLawNode` | `effective_laws.yaml:effective_laws[]` | `law.*` / `cor.*` | 从 kernel / rule / law 推出的有效定律或过渡期推论。 |
| `DerivationNode` | `derivations.yaml:derivations[]` | `deriv.*` | `premise[]` 到 `conclusion` 的 HOW 说明。 |
| `DependencyNode` | `derivations.yaml:dependencies[]` | `(dependent, depends_on)` | 非 V1–V5 的补充依赖说明。 |
| `ClaimNode` | `claims.yaml:claims[]` | claim id | 面向 checker 的归一化声明。 |

`.scihf` AST node 另含 `Program`、`QuantityDecl`、`ConditionDecl`、`Assertion`、`Relation`、`Expr`、`Scope`、`Source`；详见 `LANGUAGE.md`。

## 关系描述

| 关系 | 存储 / 语法 | 语义 | 约束 |
|---|---|---|---|
| `declares_quantity` | `Q(...)`, `quantities_registry.yaml`, `claims.yaml` | 声明物理量或常数。 | 量纲与 class 必须可解析。 |
| `declares_condition` | `C(...)`, `conditions`, `scope_aliases` | 声明作用域条件或别名。 | scope 比较前必须归一化。 |
| `has_quantity` | `quantities[]`, `about[]` | assertion 涉及的量引用。 | 引用应解析到 `qty.*` / `cst.*`。 |
| `has_scope` | `scope[]`, `under[]`, `.scihf \| ...` | assertion 的适用条件。 | 条件必须注册或可通过 alias 解析。 |
| `derived_from` | YAML `derived_from[]` | WHAT：节点成立所需逻辑前提。 | V1–V4 强制检查；不得重复。 |
| `premise` | `derivations.yaml:premise[]` | HOW 的前提集合。 | 若存在 derivation，必须与 `derived_from[]` 集合一致（V5）。 |
| `source` | `.scihf ← ...` | `.scihf` 形式的逻辑前提边。 | 语义等同 `derived_from`。 |
| `provenance` | `provenance` / `sources[]` | 文献或知识来源。 | 不得替代逻辑前提。 |
| `concludes` | `derivation.conclusion` | 推导步骤得到的目标节点。 | 必须解析到已有 assertion。 |

## Atom 清单（source graph reviewable atoms）

自动审查图当前为 **59 nodes / 105 edges**，V1–V5 全部 PASS。下表是 `mvp.source_graph` 从 YAML 中提取的可审查原子；quantity/condition 原子另见 `quantities_registry.yaml` 与 `claims.yaml`。

| Atom ID | Layer | Source file | Logical sources |
|---|---|---|---|
| `contingent.gw_polarizations` | `contingent` | `contingent.yaml` | `kernel.spacetime_dimensionality`, `kernel.general_covariance` |
| `contingent.huygens_principle` | `contingent` | `contingent.yaml` | `kernel.spacetime_dimensionality` |
| `contingent.inverse_square_law` | `contingent` | `contingent.yaml` | `kernel.spacetime_dimensionality`, `rule.dimensional_consistency` |
| `contingent.minkowski_signature` | `contingent` | `contingent.yaml` | `kernel.spacetime_dimensionality`, `kernel.lorentz_invariance` |
| `contingent.sm_fermion_content` | `contingent` | `contingent.yaml` | — |
| `contingent.sm_free_parameters` | `contingent` | `contingent.yaml` | — |
| `contingent.sm_gauge_group` | `contingent` | `contingent.yaml` | — |
| `contingent.sm_higgs_sector` | `contingent` | `contingent.yaml` | — |
| `contingent.so3_rotation_group` | `contingent` | `contingent.yaml` | `kernel.spacetime_dimensionality` |
| `contingent.stable_kepler_orbits` | `contingent` | `contingent.yaml` | `kernel.spacetime_dimensionality` |
| `contingent.volume_dimension` | `contingent` | `contingent.yaml` | `kernel.spacetime_dimensionality`, `rule.dimensional_consistency` |
| `cor.bose_einstein` | `effective_law` | `effective_laws.yaml` | `kernel.superposition_principle`, `kernel.boltzmann_entropy` |
| `cor.fermi_dirac` | `effective_law` | `effective_laws.yaml` | `law.pauli_exclusion`, `kernel.boltzmann_entropy` |
| `cor.kepler_third` | `effective_law` | `effective_laws.yaml` | `law.newton_second`, `law.newton_gravitation`, `kernel.spacetime_dimensionality` |
| `kernel.boltzmann_entropy` | `kernel` | `frameworks.yaml` | — |
| `kernel.born_rule` | `kernel` | `frameworks.yaml` | — |
| `kernel.canonical_commutation` | `kernel` | `frameworks.yaml` | — |
| `kernel.equivalence_principle` | `kernel` | `frameworks.yaml` | — |
| `kernel.gauge_interactions` | `kernel` | `frameworks.yaml` | — |
| `kernel.general_covariance` | `kernel` | `frameworks.yaml` | — |
| `kernel.least_action` | `kernel` | `frameworks.yaml` | — |
| `kernel.lorentz_invariance` | `kernel` | `frameworks.yaml` | — |
| `kernel.operator_observable` | `kernel` | `frameworks.yaml` | — |
| `kernel.spacetime_dimensionality` | `kernel` | `frameworks.yaml` | — |
| `kernel.superposition_principle` | `kernel` | `frameworks.yaml` | — |
| `kernel.unitary_evolution` | `kernel` | `frameworks.yaml` | — |
| `law.ampere_maxwell` | `effective_law` | `effective_laws.yaml` | `kernel.gauge_interactions`, `kernel.least_action`, `kernel.lorentz_invariance`, `kernel.spacetime_dimensionality` |
| `law.angular_momentum_conservation` | `effective_law` | `effective_laws.yaml` | `law.noether_theorem`, `kernel.spacetime_dimensionality` |
| `law.charge_conservation` | `effective_law` | `effective_laws.yaml` | `law.noether_theorem`, `kernel.gauge_interactions`, `kernel.spacetime_dimensionality` |
| `law.de_broglie_wavelength` | `effective_law` | `effective_laws.yaml` | `law.energy_frequency` |
| `law.einstein_field` | `effective_law` | `effective_laws.yaml` | `kernel.equivalence_principle`, `kernel.general_covariance`, `kernel.least_action`, `kernel.spacetime_dimensionality` |
| `law.em_wave_equation` | `effective_law` | `effective_laws.yaml` | `law.gauss_electric`, `law.gauss_magnetic`, `law.faraday_induction`, `law.ampere_maxwell`, `kernel.spacetime_dimensionality` |
| `law.energy_conservation` | `effective_law` | `effective_laws.yaml` | `law.noether_theorem`, `kernel.spacetime_dimensionality` |
| `law.energy_frequency` | `effective_law` | `effective_laws.yaml` | `kernel.canonical_commutation`, `kernel.least_action`, `kernel.spacetime_dimensionality`, `kernel.unitary_evolution`, `kernel.gauge_interactions` |
| `law.euler_lagrange` | `effective_law` | `effective_laws.yaml` | `kernel.least_action`, `kernel.spacetime_dimensionality` |
| `law.faraday_induction` | `effective_law` | `effective_laws.yaml` | `kernel.gauge_interactions`, `kernel.spacetime_dimensionality` |
| `law.first_law_thermo` | `effective_law` | `effective_laws.yaml` | `law.energy_conservation`, `kernel.boltzmann_entropy`, `kernel.spacetime_dimensionality` |
| `law.gauss_electric` | `effective_law` | `effective_laws.yaml` | `kernel.gauge_interactions`, `kernel.least_action`, `kernel.lorentz_invariance`, `kernel.spacetime_dimensionality` |
| `law.gauss_magnetic` | `effective_law` | `effective_laws.yaml` | `kernel.gauge_interactions`, `kernel.spacetime_dimensionality` |
| `law.ideal_gas` | `effective_law` | `effective_laws.yaml` | `law.first_law_thermo`, `kernel.boltzmann_entropy`, `kernel.spacetime_dimensionality` |
| `law.lorentz_force` | `effective_law` | `effective_laws.yaml` | `kernel.gauge_interactions`, `kernel.spacetime_dimensionality` |
| `law.lorentz_transform` | `effective_law` | `effective_laws.yaml` | `kernel.lorentz_invariance`, `kernel.spacetime_dimensionality` |
| `law.mass_energy` | `effective_law` | `effective_laws.yaml` | `kernel.lorentz_invariance`, `kernel.spacetime_dimensionality` |
| `law.momentum_conservation` | `effective_law` | `effective_laws.yaml` | `law.noether_theorem`, `kernel.spacetime_dimensionality` |
| `law.newton_first` | `effective_law` | `effective_laws.yaml` | `kernel.least_action`, `kernel.spacetime_dimensionality` |
| `law.newton_gravitation` | `effective_law` | `effective_laws.yaml` | `kernel.equivalence_principle`, `kernel.general_covariance`, `kernel.spacetime_dimensionality` |
| `law.newton_second` | `effective_law` | `effective_laws.yaml` | `kernel.least_action`, `law.euler_lagrange`, `kernel.spacetime_dimensionality` |
| `law.newton_third` | `effective_law` | `effective_laws.yaml` | `law.noether_theorem`, `kernel.spacetime_dimensionality` |
| `law.noether_theorem` | `effective_law` | `effective_laws.yaml` | `kernel.least_action`, `kernel.spacetime_dimensionality` |
| `law.pauli_exclusion` | `effective_law` | `effective_laws.yaml` | `kernel.lorentz_invariance`, `kernel.superposition_principle`, `kernel.unitary_evolution` |
| `law.schroedinger_equation` | `effective_law` | `effective_laws.yaml` | `kernel.unitary_evolution`, `kernel.canonical_commutation`, `kernel.operator_observable`, `kernel.spacetime_dimensionality` |
| `law.second_law_thermo` | `effective_law` | `effective_laws.yaml` | `kernel.boltzmann_entropy`, `kernel.equal_prior_probability`, `kernel.spacetime_dimensionality` |
| `law.third_law_thermo` | `effective_law` | `effective_laws.yaml` | `kernel.boltzmann_entropy`, `kernel.superposition_principle` |
| `law.uncertainty_principle` | `effective_law` | `effective_laws.yaml` | `kernel.canonical_commutation`, `kernel.born_rule`, `kernel.operator_observable`, `kernel.spacetime_dimensionality` |
| `law.zeroth_law` | `effective_law` | `effective_laws.yaml` | `kernel.boltzmann_entropy` |
| `rule.conservation_continuity` | `rule` | `frameworks.yaml` | — |
| `rule.dimensional_consistency` | `rule` | `frameworks.yaml` | — |
| `rule.empirical_verification_boundary` | `rule` | `frameworks.yaml` | — |

## 提取与审查

确定性提取以 `EXTRACTION.md` 为准：先加载 quantity/condition，再加载 kernel/rule、contingent、effective law、derivation，并以 source graph V1–V5 检查引用解析、无环、层次序、根可达性与 source-derivation 一致性。

```bash
python3 -m mvp.source_graph --layer1 reference/layer1 --output docs/layer1-source-graph-review.md
```
