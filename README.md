# Reference corpus

`reference/` 是 Sci-hf 的科学知识参考区，用于把"可读物理资料"逐步收束为"可机验科学语言内核"。

当前已完成 **R1-R6 充分必要性三轮审计**（2026-05-16）：6 条核心原则 → 32 条有效定律，双文件推导覆盖（`derivations.yaml` + `rigorous_derivations.yaml`），所有推导链可追溯至 kernel 根节点，YAML 验证通过。

## 目录职责

| 路径 | 职责 |
|---|---|
| `rules.md` | 人读形式的 6 条核心物理原则 (R1-R6) |
| `quantities.md` | SI 基本量、导出量与量纲参考 |
| `corollaries.md` | 早期整理的推论关系 |
| `boundaries.md` | 物理边界与常数极限 |
| `ontologies.md` | 本体论参考 |
| `sources.md` | 文献来源标签表；不是推导图 |
| `behavioral-constraints.md` | 库建设行为约束（操作原则层） |
| `layer1/` | 第一阶段内核区科学语言验证资产 |

## `reference/layer1` 文件职责

| 文件 | 职责 |
|---|---|
| `layer1/README.md` | `layer1/` 的入口说明、文件职责、token/node/关系描述与 atom 清单 |
| `LANGUAGE.md` | `.scihf` 的 token、node、grammar、semantics 与 checker 约束 |
| `EXTRACTION.md` | 从 YAML / `.scihf` 到 node、token、edge 的确定性提取约定 |
| `SOURCE.md` | `←` / `derived_from` / `premise` 的逻辑前提图规范 |
| `physics.scihf` | `.scihf` 语言样例语料 |
| `frameworks.yaml` | 不可再推导的 kernel 前提与 structural meta-rules |
| `effective_laws.yaml` | 从 kernel / rule / law 推出的有效定律与定理化表达 |
| `derivations.yaml` | 有效定律的推导步骤与 premise |
| `quantities_registry.yaml` | 物理量、scope、scope alias 与 discontinuity 注册表 |
| `claims.yaml` | 面向 checker 的归一化声明表 |
| `fundamental.md` / `effective.md` / `dimensions.md` / `quantities.md` | 人读解释材料 |
| `contingent.yaml` | 我们这个宇宙的经验事实，不属于 kernel 根 |

## 建设原则

- `provenance` 表示文献或知识来源；`source` / `derived_from` / `premise` 表示逻辑前提。
- 内核区新增内容必须优先明确 ID、layer、scope、quantities 与 provenance。
- scope 比较前必须经过 `scope_aliases` 归一化。
- `reference/layer1` 的提取顺序、node/token 列表与去重规则以 `layer1/EXTRACTION.md` 为准。
- `rules.md` 的 R1-R6 是物理世界最底层的 6 条核心原则。R1 包含三个独立子原则（1a/1b 因果结构 + 1c 等效原理）；R6 包含两个独立公设（6a S=k·lnW + 6b 等概率先验）。32 条有效定律的推导链（含必要性/充分性标注）见 `layer1/rigorous_derivations.yaml`。
- Noether 定理和自旋-统计定理（Pauli 不相容原理）是 R2/R4 的数学推论，不列为独立规则；但后者在推导文件中为结构性大纲+深度声明。

## 自动化审查

运行：

```
python3 -m mvp.source_graph --layer1 reference/layer1 --output docs/layer1-source-graph-review.md
```

将对内核 / 规则 / 经验事实 / 有效定律 / 推导图执行 `SOURCE.md` V1–V5 检查，最新报告见 [`docs/layer1-source-graph-review.md`](../docs/layer1-source-graph-review.md)。
