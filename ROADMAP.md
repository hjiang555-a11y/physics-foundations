# Physics Foundations — 路线图

> 最后更新：2026-05-16 | 当前版本：R1-R6 充分必要性审计完成（Round 12）

---

## 当前状态

### 已完成

| 里程碑 | 状态 |
|--------|:----:|
| R1-R6 核心原则（6 条，含独立子公设） | ✅ |
| 32 条有效定律的双文件推导覆盖（derivations.yaml + rigorous_derivations.yaml） | ✅ |
| 136 条显式必要性条件 [N] 标注 | ✅ |
| 四轮充分必要性审计（kernel 层清理、L-form 来源、½mv² 对称性论证、热力学极限桥接、变量合并、Pauli 推导草图） | ✅ |
| V1-V5 自动化推导验证器（`validate_derivations.py`，147 nodes, 39 derivations, ALL PASS） | ✅ |
| 全局文档对齐（32→30 引用修复、README 更新、迭代记录至 Round 12） | ✅ |

### 运行验证

```bash
cd physics-foundations
python3 validate_derivations.py layer1/
```

预期输出：`VERDICT: PASS — Errors: 0, Warnings: 0`

---

## 后续方向

### 短期（巩固 — 预期 1-3 天）

#### S1. `derivations.yaml` 必要性条件补全
当前简版 `derivations.yaml` 的 32 条推导大部分只有 3-5 行大纲步骤，缺少 `necessity_conditions` 和 `sufficiency_conditions` 块。应逐条对照 `rigorous_derivations.yaml` 补充，使两个文件均达到完备标注。
- **文件**：`layer1/derivations.yaml`
- **工作量**：~2-3 小时

#### S2. 依赖图可视化
基于现有的 V1-V5 验证器，输出 DOT 格式依赖图，按层着色（kernel=红, law=蓝, corollary=绿, contingent=灰），便于审阅推导链完整性。
- **文件**：新增 `tools/visualize_graph.py`
- **工作量**：~1 小时

#### S3. CI 集成
将 `validate_derivations.py` 加入 GitHub Actions，每次 push 自动运行 V1-V5 检查，拒绝引入断链的 PR。
- **文件**：新增 `.github/workflows/validate.yml`
- **工作量**：~30 分钟

---

### 中期（扩展推导深度 — 预期 1-2 周）

#### M1. 自旋-统计定理的完整逻辑链
当前 `deriv.pauli_exclusion` 是结构性大纲 + caveat。可参考 Streater & Wightman / Weinberg Vol.I Ch.5，扩展为 12-15 步的详细推导大纲，明确标注哪些步骤已在本项目框架内证明、哪些依赖外部定理（CPT、Wightman 公理）。
- **文件**：`layer1/rigorous_derivations.yaml` (deriv.pauli_exclusion)
- **参考**：Streater & Wightman §4.4; Weinberg §5.7

#### M2. Einstein 场方程的 Lovelock 唯一性展开
当前推导中 `deriv.einstein_field_equations` 引用 Lovelock 定理但未展开。应添加一个补充推导，在推导步骤中展开 Lovelock 定理的 4D 条件下的唯一性论证：为什么 EH 作用量（R + Λ）是唯一产生二阶场方程的选择。
- **文件**：`layer1/rigorous_derivations.yaml`
- **参考**：Lovelock, J. Math. Phys. 12, 498 (1971)

#### M3. 标准模型有效场论推导链
当前 `contingent.yaml` 声明了 SM 规范群和费米子内容但未构建推导链。可添加从 `contingent.sm_gauge_group + contingent.sm_fermion_content` 出发的有效场论推导：
- 跑动耦合常数与渐近自由（QCD）
- Higgs 机制与 W/Z 质量生成
- CKM 矩阵的物理必要性
- **文件**：`layer1/contingent.yaml` + 新增 `deriv.sm_*` 条目

#### M4. Nernst 不可达性原理
热力学第三定律有强弱两种形式。当前 `law.third_law_thermo` 仅覆盖弱形式（S→0 as T→0）。Nernst 原始表述——"无法通过有限步骤达到绝对零度"——是一个独立的更强推论，可作为 `cor.nernst_unattainability` 新增。
- **文件**：`layer1/effective_laws.yaml` + 推导文件

---

### 长期（体系化 — 预期 1-3 月）

#### L1. 多维物理对比附录
R1-R6 体系的一个核心力量在于"若某条原则不同，物理世界会怎样"的反事实推理。可撰写一个系统附录，展示若 R1 中 D≠3、Lorentz→Euclidean、c→∞，或 R4 中 [x̂,p̂]=0，哪些定律会如何退化。这本身是对 R1-R6 必要性论证的最强佐证。
- **文件**：新增 `appendix/counterfactual-physics.md`
- **参考**：Ehrenfest (1917); Tangherlini (1963); Barrow & Tipler

#### L2. `.scihf` 语言完整实现
当前 `LANGUAGE.md` 定义了 `.scihf` 的 token/node/grammar 规范，`physics.scihf` 是样例语料。下一步是实现一个完整的 parser + checker：
1. 词法分析器（tokenizer）
2. 语法分析器（parser，生成 AST）
3. 语义检查器（checker，执行 LANGUAGE.md 中定义的一致性约束）
- **文件**：新增 `tools/scihf_parser.py`
- **参考**：`layer1/LANGUAGE.md`, `layer1/EXTRACTION.md`

#### L3. 实验验证数据库对接
物理定律的最终判据是实验。可构建一个 `experiments.yaml`，记录每条有效定律对应的关键实验（如 Michelson-Morley → Lorentz 不变性, Eötvös → 等效原理, Davisson-Germer → de Broglie 波长），并关联实验精度与定律的确证度。
- **文件**：新增 `layer1/experiments.yaml`

---

## 优先顺序建议

```
Week 1:  S1 (必要性补全) → S2 (可视化) → S3 (CI)
Week 2:  M1 (自旋-统计) → M4 (Nernst)
Week 3:  M2 (Lovelock) → M3 (SM 推导链)
Month 2: L1 (多维对比) → L2 (scihf parser)
Month 3: L3 (实验数据库)
```

---

## 贡献原则

- **最小变更**：每项修改仅触及必要文件，不改动无关结构
- **可追溯**：所有推导步骤均显式标注前提（[N]）和充分性（[S]）
- **可机验**：修改后必须通过 `validate_derivations.py` V1-V5 全部检查
- **先诊断后行动**：任何新定律或推导，先确认其 kernel 依赖关系，再实施
