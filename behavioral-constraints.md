# 行为约束（库建设原则）

> 本文件记录 Sci-hf 库建设过程中必须遵守的**行为约束**。
> 这些约束不是物理前提，也不是数学结构规则，而是我们建立这个库时约定的操作原则。
> 任何向 `reference/layer1` 的 kernel / rule / contingent 资产写入，都必须满足这些约束。

---

## B1. 实验验证边界约束

**ID**: `rule.empirical_verification_boundary`
（在 `reference/layer1/frameworks.yaml` 及 `claims.yaml` 的结构化资产中，层级字段标注为 `layer: rule`；但在本文件的概念分层中，该约束属于**行为约束**层，与数学结构规则的 `rule.dimensional_consistency` 等区分。）

**约束陈述**: 未经实验证实的理论不能作为 kernel 放置判据，不能用来覆盖或降级已有实验支撑的 kernel 前提。

**详细说明**:
- 未经实验证实的理论框架可记录在 `reference/layer1` 的 `contingent` 或注释中，作为背景信息保留。
- 但它不能以"更深层理论"的名义将已验证的 kernel（如 `kernel.spacetime_dimensionality`：3+1 时空维度）从 kernel 层移除或替换。
- 例如：额外维度理论（弦论景观、Kaluza-Klein 等）尚无直接实验证实，不能凭此将 `kernel.spacetime_dimensionality` 降级或替换为更抽象的维度中性版本。

**适用范围**: 所有向 `reference/layer1` 写入 kernel / rule 的操作；所有修改 `reference/rules.md` 核心原则的操作。

**来源**: Sci-hf 库建设原则；`reference/layer1/frameworks.yaml` §structural_rules

---

## 本文件与其他规则文件的关系

| 文件 | 内容 |
|------|------|
| `reference/behavioral-constraints.md`（本文件）| 库建设行为约束（操作原则层） |
| `reference/rules.md` R1–R6 | 6 条核心物理原则（原则层） |
| `reference/boundaries.md` §失效边界与例外情况 | 原则失效边界与例外（边界层） |
| `docs/scientific-description-language-rules.md` | 语言规则与充分必要性检查 |
