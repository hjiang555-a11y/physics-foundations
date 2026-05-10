# Reference/layer1 确定性提取约定

`reference/layer1` 的提取目标是把内核区资料收束为可机验的节点、token 与关系约束。提取器不得依赖自然语言猜测；同一份 YAML / `.scihf` 输入必须产生同一组节点和边。

## 1. Token 列表

| Token | 来源字段 / 语法 | 含义 |
|---|---|---|
| `id` | `id` / `conclusion` / `derived_from` / `premise` | 稳定引用标识，必须唯一可解析 |
| `namespace` | `kernel.*` / `rule.*` / `law.*` / `cor.*` / `contingent.*` / `qty.*` / `cst.*` | 节点命名空间 |
| `layer` | `layer` | 节点层：`kernel`、`rule`、`contingent`、`effective_law`、`law`、`corollary`、`quantity`、`condition` |
| `relation` | `relation` / `.scihf` assertion | 人读科学关系文本或语言断言 |
| `quantity_ref` | `quantities[]` / `Q(...)` | 物理量引用 |
| `scope_ref` | `scope[]` / `C(...)` / `under[]` | 作用域或条件引用 |
| `source_ref` | `derived_from[]` / `premise[]` / `←` | 逻辑前提引用 |
| `provenance` | `provenance` / `sources[]` | 文献或知识来源，不参与推导图 |
| `derivation_step` | `steps[]` | 推导步骤文本 |

> 建设原则：未经实验证实的理论不是可信理论；未被当前 corpus 内更深层可信前提推论出的、但作为推导根使用的实证前提，应放入 `kernel`。`kernel.spacetime_dimensionality` 是三维空间与一维时间的基本前提 / 基本规则，不是后续公式推导出来的结论；因此 10/11 维弦/M 理论候选不能作为把它降出 kernel 的判据。
> `reference/rules.md` 的 R1–R6 是物理世界最底层的 6 条核心原则；完整科学描述语言规则见 `../../docs/scientific-description-language-rules.md`。
>
> 前提闭包原则：若定律或推导的具体公式形式依赖当前 corpus 不能推出的 3 个空间维与 1 个时间维（例如 `∇` / `curl` / `×` 的三维向量形式、`d^3r` / `d^4x` 积分、四维张量指标、`1/r²` 势或单一时间参数 `dt`），必须把 `kernel.spacetime_dimensionality` 显式列入 `derived_from` / `premise`。只有当该维度前提已由被引用的中间定律承载且当前推导步骤不再直接使用新的维度特定结构时，才可不重复列出。

## 2. Node 列表

| Node | 存储位置 | 主键 | 说明 |
|---|---|---|---|
| `QuantityNode` | `quantities_registry.yaml` / `claims.yaml` / `.scihf Q(...)` | `qty.*` / `cst.*` | 可被 assertion 引用的物理量与常数 |
| `ConditionNode` | `quantities_registry.yaml` / `claims.yaml` / `.scihf C(...)` | condition id | scope 可解析条件 |
| `KernelNode` | `frameworks.yaml:kernels[]` | `kernel.*` | 推导图根节点，不允许 `derived_from` |
| `RuleNode` | `frameworks.yaml:structural_rules[]` | `rule.*` | 结构性元规则，作为 foundational 依赖参与推导 |
| `ContingentNode` | `contingent.yaml:contingent_facts[]` | `contingent.*` | 我们宇宙的经验事实；派生 contingent 必须显式 `derived_from` |
| `EffectiveLawNode` | `effective_laws.yaml:effective_laws[]` | `law.*` / 过渡期 `cor.*` | 从 kernel / rule / law 推出的有效定律或过渡期推论 |
| `DerivationNode` | `derivations.yaml:derivations[]` | `deriv.*` | `premise[]` 到 `conclusion` 的 HOW 说明 |
| `DependencyNode` | `derivations.yaml:dependencies[]` | `(dependent, depends_on)` | 非 V1–V5 的补充依赖说明 |
| `ClaimNode` | `claims.yaml:claims[]` | claim id | 面向 checker 的归一化声明 |

## 3. 关系约束

1. `id` 在同一 node 集合中必须唯一。
2. `derived_from[]` 与 `premise[]` 内不得重复同一个 ID；重复前提视为内容漂移。
3. `provenance` / `sources[]` 只记录文献来源，不得替代 `derived_from` / `premise`。
4. `source_ref` 必须满足 `SOURCE.md` V1–V5：
   - V1 引用解析；
   - V2 无环；
   - V3 层次序；
   - V4 law / corollary 可达至少一个 kernel 根；
   - V5 若存在 Derivation，则 `set(premise) == set(derived_from)`。
5. contingent 派生内容应落到 `contingent.*` 节点；不能把 contingent 支撑项混入无对应 assertion 的 law derivation。
6. scope 比较前必须经过 `scope_aliases` 归一化。
7. 未经实验证实的理论可以记录为 `provenance` 或说明性背景，但不能作为 source graph 的判据节点；不能用不可验证或尚未验证的高维理论排除核心 kernel 前提。

## 4. 确定性提取顺序

1. 读取 `quantities_registry.yaml` 和 `claims.yaml`，建立 quantity / constant / condition 字典。
2. 读取 `frameworks.yaml`，提取 `KernelNode` 与 `RuleNode`；`kernel.spacetime_dimensionality` 属于基本前提 / 基本规则级的 kernel 根节点。
3. 读取 `contingent.yaml`，提取 `ContingentNode` 与其 `derived_from` 边。
4. 读取 `effective_laws.yaml`，提取 `EffectiveLawNode` 与其 `derived_from` 边。
5. 读取 `derivations.yaml:derivations[]`，按 `conclusion` 绑定 `DerivationNode`，执行 V5 集合一致性检查。
6. 读取 `derivations.yaml:dependencies[]`，只作为补充解释边，不参与 V1–V5 source graph verdict。
7. 生成报告时按 `id` 排序输出，集合比较时去重，存储文件中仍禁止重复项。

## 5. 当前存储边界

- `SOURCE.md` 定义 source/derivation 图语义。
- `LANGUAGE.md` 定义 `.scihf` 语言 token、AST node 与 checker 约束。
- `EXTRACTION.md` 定义 YAML / `.scihf` 到 node、token、edge 的确定性抽取约定。
- `docs/layer1-source-graph-review.md` 是自动化审查结果，不是手工维护的事实源。
