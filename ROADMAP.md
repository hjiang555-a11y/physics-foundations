# Physics Foundations — 路线图

> 最后更新：2026-05-26 | 当前版本：Round 13 — M1-M4 中期建设完成，150 nodes / 43 derivations，完整性·自洽性·充分必要性证明通过

---

## 当前状态

### 已完成

| 里程碑 | 状态 |
|--------|:----:|
| R1-R6 核心原则（6 条，含独立子公设） | ✅ |
| 43 条推导的双文件覆盖（derivations.yaml + rigorous_derivations.yaml） | ✅ |
| 150+ 条显式必要性条件 [N] 标注 | ✅ |
| 七轮充分必要性审计（kernel 层清理、L-form 来源、½mv² 对称性论证、热力学极限桥接、变量合并、Pauli 推导草图、完整性元验证） | ✅ |
| V1-V5 自动化推导验证器（`validate_derivations.py`，150 nodes, 43 derivations, ALL PASS） | ✅ |
| 全局文档对齐（32→30 引用修复、README 更新、迭代记录至 Round 13） | ✅ |
| S1: derivations.yaml 必要性条件补全（39→43 条推导含 necessity_conditions + sufficiency_conditions） | ✅ |
| S2: 依赖图 DOT 可视化（`tools/visualize_graph.py`，63 nodes / 119 edges，按层着色） | ✅ |
| S3: GitHub Actions CI 集成（`.github/workflows/validate.yml`） | ✅ |
| **M1: 自旋-统计定理完整逻辑链（13 步推导，external_theorem / in_project 标注）** | ✅ |
| **M2: Einstein 场方程的 Lovelock 唯一性展开（10 步，Euler 密度 + Gauss-Bonnet + Ostrogradsky）** | ✅ |
| **M3: 标准模型有效场论推导链（渐近自由 + Higgs 机制 + CKM 矩阵，共 20 步）** | ✅ |
| **M4: Nernst 不可达性原理（7 步，第三定律强形式）** | ✅ |
| **元验证：完整性·自洽性·充分必要性证明（`tools/meta_validate.py` + `layer1/PROOF.md`）** | ✅ |
| **语言单位定义（9 种论证单位：K, R, L, C, X, D, [N], [S], ↔）** | ✅ |

### 运行验证

```bash
cd physics-foundations
python3 validate_derivations.py layer1/
```

预期输出：`VERDICT: PASS — Errors: 0, Warnings: 0`

### 依赖图生成

```bash
python3 tools/visualize_graph.py layer1/
dot -Tpng physics_foundations_graph.dot -o graph.png
```

---

## 后续方向

### ~~短期（巩固 — 预期 1-3 天）~~ ✅ 已完成

#### S1. `derivations.yaml` 必要性条件补全 ✅
当前简版 `derivations.yaml` 的 39 条推导已全部补全 `necessity_conditions` 和 `sufficiency_conditions` 块（32 条对照 `rigorous_derivations.yaml`，7 条 contingent 手动撰写）。
- **文件**：`layer1/derivations.yaml`

#### S2. 依赖图可视化 ✅
输出 DOT 格式依赖图，按层着色（kernel=红, law=蓝, corollary=绿, contingent=灰），59 节点 / 105 边，与 README atom 清单一致。
- **文件**：`tools/visualize_graph.py`

#### S3. CI 集成 ✅
GitHub Actions workflow，push/PR 时自动运行 V1-V5 检查。
- **文件**：`.github/workflows/validate.yml`

---

### 中期（扩展推导深度 — 预期 1-2 周） ~~✅ 已完成~~

#### M1. 自旋-统计定理的完整逻辑链 ✅
扩展 `deriv.pauli_exclusion` 至 13 步推导，明确标注 external_theorem（Lorentz 表示论、簇分解、CPT 定理、系数函数）vs. in_project（Hilbert 空间、微因果性、波函数反对称性、Pauli 不相容）。Cross-ref: M3 (SM 费米子), cor.fermi_dirac, M4 (Nernst 基态简并)。
- **文件**：`layer1/rigorous_derivations.yaml`, `layer1/derivations.yaml`

#### M2. Einstein 场方程的 Lovelock 唯一性展开 ✅
扩展 `deriv.einstein_field_equations` 至 10 步，展示 Lovelock 定理的 Euler 密度序列 (L₀=Λ, L₁=R, L₂=Gauss-Bonnet)、Chern-Gauss-Bonnet 的拓扑性质 (L₂ 在 4D 中为拓扑不变量)、Ostrogradsky 鬼场排除 R² 等高阶项。Cross-ref: M1 (D=4 双重印证), M3 (唯一性方法论平行)。
- **文件**：`layer1/rigorous_derivations.yaml`, `layer1/derivations.yaml`

#### M3. 标准模型有效场论推导链 ✅
三条新推导：`deriv.asymptotic_freedom` (6 步, SU(3) β-函数), `deriv.higgs_mechanism` (7 步, SSB→W/Z 质量), `deriv.ckm_necessity` (7 步, Yukawa→CKM→CP 破坏)。新增 3 条 corollary: `cor.asymptotic_freedom`, `cor.higgs_mechanism`, `cor.ckm_matrix`。
- **文件**：`layer1/rigorous_derivations.yaml`, `layer1/derivations.yaml`, `layer1/effective_laws.yaml`

#### M4. Nernst 不可达性原理 ✅
新增 `cor.nernst_unattainability` + `deriv.nernst_unattainability` (7 步: 弱形式→热容标度→步数发散→强形式)。Cross-ref: M1 (自旋-统计→基态简并度→残余熵)。
- **文件**：`layer1/effective_laws.yaml`, `layer1/rigorous_derivations.yaml`, `layer1/derivations.yaml`

#### 全局对齐 ✅
- 补充 7 条 contingent 推导至 `rigorous_derivations.yaml`（inv_sq, so3, vol, minkowski, gw, kepler, huygens）
- 修复 `rigorous_derivations.yaml` 中 `deriv.lorentz_transformation` 的重复 premise
- 39→39 紧凑/严格推导完全对齐（ID、conclusion、premise 一致性）

#### 元验证 ✅
- `tools/meta_validate.py`: 完整性 100% (43/43), 必要性验证 (R1-R6 各影响 ≥1 定律), 自洽性验证 (0 cycles), 最小性验证 (0 kernel→kernel 依赖)
- `layer1/PROOF.md`: 完整的形式化证明文档（语言单位定义、完整性矩阵、必要性矩阵、自洽性证明、交叉印证网）

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
