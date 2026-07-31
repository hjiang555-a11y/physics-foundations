# R1-R6 充分必要性修复计划

## TL;DR

> **Quick Summary**: 修复物理学知识库中 R1-R6 核心原则的充分必要性缺陷——降级 3 个幽灵 kernel 节点、补充 3 条定理的缺失前提、清理 2 处冗余表述、修复 mvp 验证模块。
> 
> **Deliverables**:
> - `layer1/claims.yaml` — 幽灵 kernel 节点降级 + 引用更新
> - `layer1/rigorous_derivations.yaml` — 推导前提修正
> - `layer1/effective_laws.yaml` — 缺失 derived_from 补充
> - `rules.md` — R1.8 表修正 + 冗余清理
> - `layer1/physics.scihf` — .scihf 示例同步
> - `layer1/LANGUAGE.md` — 语言规范示例同步
> - `mvp/` 软链接 — 使 source_graph 可本地运行
> 
> **Estimated Effort**: Medium
> **Parallel Execution**: YES — 3 waves
> **Critical Path**: mvp 修复 → claims.yaml 降级 → 传播到其他文件 → source_graph 验证

---

## Context

### Original Request
用户要求严格检查 R1-R6 的充分必要性，方法是推导所有 30 条定理是否包含隐性条件未列出，以及 R1-R6 是否有多余表述。分析完成后，用户选择了"创建修复计划"（选项 2），并补充要求加入 mvp 模块修复。

### Interview Summary
**Key Discussions**:
- **检查方法**: 逐一追溯 30 条定理推导至 R1-R6，标定缺失前提和冗余表述
- **验证策略**: 逻辑一致性审查（Recommended），不开发新的自动化测试
- **mvp 修复**: 用户要求将 mvp 模块修复纳入计划，确保 source_graph checker 可本地运行

**Metis Review Findings**:
- **幽灵节点真实位置**: `kernel.pauli_exclusion`、`kernel.light_speed_invariance`、`kernel.second_law` 不在 frameworks.yaml 中——它们在 `claims.yaml`（line 656-715）被声明为 `_from: []` kernel 节点，并被 6 个其他文件引用
- **范围扩大**: 原计划 4 文件 → 实际需 ~7 文件 + mvp 修复
- **Edge cases**: derivations.yaml vs rigorous_derivations.yaml 可能不同步；physics.scihf 改 ID 可能影响 .scihf parser

### Research Findings
- **mvp 模块位置**: `/home/room115/Sci-hf/mvp/source_graph.py`（不在 physics-foundations 本地）
- **当前 source_graph 状态**: 59 nodes / 89 edges, V1-V5 ALL PASS（但 atom 表包含幽灵节点，可能使用了过时数据）
- **frameworks.yaml 真实 kernel 节点**: 13 个（不包含 pauli_exclusion, light_speed_invariance, second_law）

---

## Work Objectives

### Core Objective
修复 physics-foundations 知识库中 R1-R6 推导链的充分必要性缺陷，消除幽灵 kernel 节点，补充缺失前提，清理冗余表述，并恢复 mvp 验证模块可用性。

### Concrete Deliverables
- `layer1/claims.yaml`: 3 个幽灵 kernel 节点正确降级为 `law.*` 或删除
- `layer1/rigorous_derivations.yaml`: premise 引用从 `kernel.*` 修正为正确 ID
- `layer1/effective_laws.yaml`: `law.third_law_thermo` 补充缺失的 derived_from
- `rules.md`: R1.8 子组件表修正、R6 冗余清理、定理清单前提列修正
- `layer1/physics.scihf` + `LANGUAGE.md`: 示例 ID 同步
- `mvp` 软链接: 使 `python3 -m mvp.source_graph` 在 physics-foundations 内可运行

### Definition of Done
- [ ] `python3 -m mvp.source_graph --layer1 reference/layer1 --output docs/layer1-source-graph-review.md` → V1–V5 ALL PASS
- [ ] 无 `kernel.pauli_exclusion`、`kernel.light_speed_invariance`、`kernel.second_law` 残留在 YAML 的 derived_from/premise 字段
- [ ] `law.third_law_thermo` 的 derived_from 包含各必需 kernel 组件
- [ ] `law.lorentz_transform` 的 premise 不引用已合并的 `kernel.light_speed_invariance`
- [ ] `cor.fermi_dirac` 的前提链可追溯至 R1-R6（通过 `law.pauli_exclusion`）

### Must Have
- 所有 source graph V1-V5 PASS
- 幽灵 kernel 节点从 YAML 逻辑链中消失
- 缺失前提被正确补充
- R1-R6 表述无逻辑冗余

### Must NOT Have (Guardrails)
- **MUST NOT** 删除 `kernel.light_speed_invariance` 而不提供迁移路径（rules.md R1.8 表需保留为注释/alias）
- **MUST NOT** 修改 frameworks.yaml 中真实的 13 个 kernel 节点
- **MUST NOT** 在此轮修复中节点化 Lovelock 定理或重新分类 de Broglie
- **MUST NOT** 改动 `kernel.equal_prior_probability` 的层属（留待后续讨论）
- **MUST NOT** 修改 quantities_registry.yaml 或 contingent.yaml

---

## Verification Strategy

> **ZERO HUMAN INTERVENTION** — ALL verification is agent-executed.

### Test Decision
- **Infrastructure exists**: YES (mvp.source_graph via Sci-hf)
- **Automated tests**: Tests-after (source_graph checker 作为事后验证)
- **Framework**: Python mvp.source_graph V1-V5 checker + grep cross-reference

### QA Policy
Every task includes agent-executed QA scenarios.
- **Backend/CLI**: Bash (curl/grep/diff) for file content verification
- **Source graph**: `python3 -m mvp.source_graph` for V1-V5 validation
- **Evidence**: `.sisyphus/evidence/task-{N}-{scenario-slug}.txt`

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Start Immediately — mvp 修复 + baseline):
├── Task 1: mvp 模块链接 + source_graph 可运行化 [quick]
├── Task 2: 运行预修复 baseline source_graph 审查 [quick]
└── Task 3: 生成幽灵节点引用完整清单 [quick]

Wave 2 (After Wave 1 — 核心修复, MAX PARALLEL):
├── Task 4: 修复 claims.yaml — 降级 3 个幽灵 kernel 节点 [deep]
├── Task 5: 修复 rigorous_derivations.yaml — 修正 premise 引用 [deep]
├── Task 6: 修复 effective_laws.yaml — 补充缺失 derived_from [quick]
└── Task 7: 修复 rules.md — 清理表和引用 [quick]

Wave 3 (After Wave 2 — 传播):
├── Task 8: 修复 physics.scihf — 同步 .scihf 示例 [quick]
└── Task 9: 修复 LANGUAGE.md — 同步语法示例 [quick]

Wave 4 (After Wave 3 — 验证):
├── Task 10: 运行 post-fix source_graph 审查 [quick]
├── Task 11: 跨文件引用一致性审计 [deep]
└── Task 12: 重新生成 README.md atom 表 [quick]

Wave FINAL (After ALL tasks):
├── Task F1: Plan Compliance Audit (oracle)
├── Task F2: Code Quality Review (unspecified-high)
├── Task F3: Real Manual QA (unspecified-high)
└── Task F4: Scope Fidelity Check (deep)
```

**Critical Path**: Task 1 → Task 2 → Task 4 → Task 8 → Task 10 → Task 11 → F1-F4
**Parallel Speedup**: Waves 2 and 4 allow 4 and 3 tasks in parallel respectively
**Max Concurrent**: 4 (Wave 2)

---

## TODOs

### Wave 1: mvp 修复 + Baseline

- [ ] 1. **mvp 模块链接 + source_graph 可运行化**

  **What to do**:
  - 在 `/home/room115/physics-foundations/` 下创建指向 `/home/room115/Sci-hf/mvp/` 的软链接 `mvp`
  - 确保 `python3 -m mvp.source_graph --help` 正常输出
  - 安装依赖：`python3 -m pip install -r /home/room115/Sci-hf/requirements-dev.txt`（仅在缺少 pyyaml 时）

  **Must NOT do**:
  - 不要复制 mvp 目录（软链接即可）
  - 不要修改 mvp 源代码

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 创建软链接 + 验证命令可用，单一简单操作
  - **Skills**: []
  - **Skills Evaluated but Omitted**: None — no domain-specific skills needed

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 1 (sequential prerequisite for Task 2)
  - **Blocks**: Task 2, Task 3
  - **Blocked By**: None

  **References**:
  - `/home/room115/Sci-hf/mvp/source_graph.py:1-30` — source_graph 模块入口，确认它可以独立运行
  - `/home/room115/Sci-hf/requirements-dev.txt` — 依赖清单（需要 pyyaml）

  **Acceptance Criteria**:
  - [ ] `ls -la /home/room115/physics-foundations/mvp` 显示为指向 Sci-hf/mvp 的软链接
  - [ ] `python3 -m mvp.source_graph --help` 正常执行（working directory: physics-foundations）

  **QA Scenarios**:

  ```
  Scenario: mvp 模块可运行
    Tool: Bash
    Preconditions: Sci-hf/mvp 目录存在且含 __init__.py
    Steps:
      1. cd /home/room115/physics-foundations && ln -sf /home/room115/Sci-hf/mvp mvp
      2. cd /home/room115/physics-foundations && python3 -m mvp.source_graph --help
      3. 确认输出包含 "V1", "V2", "layer1" 等关键字
    Expected Result: 命令正常执行，输出帮助信息或参数说明
    Failure Indicators: ModuleNotFoundError, 或 --help 无输出
    Evidence: .sisyphus/evidence/task-1-mvp-link.txt
  ```

  **Commit**: YES (groups with Task 2)
  - Message: `fix: restore mvp module symlink for source_graph verification`
  - Files: `mvp`

- [ ] 2. **运行预修复 baseline source_graph 审查**

  **What to do**:
  - 运行 `python3 -m mvp.source_graph --layer1 reference/layer1 --output /tmp/pre-fix-review.md`
  - 保存输出为 baseline 证据
  - 记录当前 V1-V5 状态、node/edge 计数

  **Must NOT do**:
  - 不要在运行前做任何文件修改

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 执行一条命令并记录结果
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 1 (depends on Task 1)
  - **Blocks**: Task 3, Task 10 (post-fix 对比)
  - **Blocked By**: Task 1

  **References**:
  - `layer1/SOURCE.md` — V1-V5 规范定义
  - `docs/layer1-source-graph-review.md` — 最近一次审查报告

  **Acceptance Criteria**:
  - [ ] `/tmp/pre-fix-review.md` 文件已生成
  - [ ] 输出中包含 nodes/edges 计数和 V1-V5 逐条结果

  **QA Scenarios**:

  ```
  Scenario: baseline source_graph 审查可运行
    Tool: Bash
    Preconditions: Task 1 完成（mvp 可用）
    Steps:
      1. cd /home/room115/physics-foundations && python3 -m mvp.source_graph --layer1 reference/layer1 --output /tmp/pre-fix-review.md
      2. grep "V1:" /tmp/pre-fix-review.md; grep "V2:" /tmp/pre-fix-review.md; grep "V3:" /tmp/pre-fix-review.md; grep "V4:" /tmp/pre-fix-review.md; grep "V5:" /tmp/pre-fix-review.md
      3. grep "Nodes:" /tmp/pre-fix-review.md; grep "Edges:" /tmp/pre-fix-review.md
    Expected Result: V1-V5 结果全部可见，node/edge 计数与当前 README 一致（59/89）
    Evidence: .sisyphus/evidence/task-2-baseline.txt
  ```

  **Commit**: YES (groups with Task 1)
  - Message: `fix: restore mvp module symlink for source_graph verification`
  - Files: `mvp`

- [ ] 3. **生成幽灵节点引用完整清单**

  **What to do**:
  - 在 layer1/ 全域搜索 `kernel.pauli_exclusion`、`kernel.light_speed_invariance`、`kernel.second_law` 的所有引用
  - 区分三类引用：(a) derived_from/premise 逻辑前置引用，(b) 文档注释/表格，(c) .scihf 示例
  - 输出完整引用矩阵（文件:行号:用途）

  **Must NOT do**:
  - 不要在此任务中修改任何文件（仅侦察）

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 搜索 + 分类记录，无修改操作
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with nothing — 纯侦察)
  - **Parallel Group**: Wave 1 (可在 Task 1 完成后与 Task 2 并行)
  - **Blocks**: Task 4（claims.yaml 修复需要完整引用清单）
  - **Blocked By**: Task 1（mvp 不是必须的，但确保目录结构正确）

  **References**:
  - `layer1/claims.yaml:656-715` — 幽灵 kernel 节点声明处（预期位置）
  - `layer1/rigorous_derivations.yaml` — deriv.fermi_dirac 引用 kernel.pauli_exclusion
  - `layer1/effective_laws.yaml` — law.zeroth_law derived_from 等
  - `layer1/physics.scihf` — .scihf 语法示例
  - `layer1/LANGUAGE.md` — 语言规范
  - `layer1/README.md` — atom 表

  **Acceptance Criteria**:
  - [ ] 三个幽灵节点各自的完整引用位置清单（每节点 ≥2 个引用文件）
  - [ ] 分类标注：逻辑引用 vs 文档引用 vs 示例引用

  **QA Scenarios**:

  ```
  Scenario: 幽灵节点引用全覆盖搜索
    Tool: Bash (grep)
    Preconditions: 工作目录为 physics-foundations
    Steps:
      1. grep -rn "kernel\.pauli_exclusion" layer1/ --include="*.yaml" --include="*.md" --include="*.scihf"
      2. grep -rn "kernel\.light_speed_invariance" layer1/ --include="*.yaml" --include="*.md" --include="*.scihf"
      3. grep -rn "kernel\.second_law" layer1/ --include="*.yaml" --include="*.md" --include="*.scihf"
      4. 将结果分类标注为 output
    Expected Result: 每个幽灵节点至少找到 2 个引用文件，最多 ~7 个文件
    Evidence: .sisyphus/evidence/task-3-ghost-refs.txt
  ```

  **Commit**: NO（纯侦察任务）

---

### Wave 2: 核心修复

- [ ] 4. **修复 claims.yaml — 降级 3 个幽灵 kernel 节点**

  **What to do**:
  基于 Task 3 的清单，在 claims.yaml 中：
  - `kernel.pauli_exclusion` → `law.pauli_exclusion`：改 `id`、改 `layer: kernel` → `layer: effective_law`、改 `_from: []` → `_from: [kernel.lorentz_invariance, kernel.superposition_principle, kernel.unitary_evolution]`
  - `kernel.light_speed_invariance`：**删除**（其内容已覆盖于 `kernel.lorentz_invariance`）。若其他 claim 引用它，将引用重定向至 `kernel.lorentz_invariance`
  - `kernel.second_law`：**删除**（其内容已覆盖于 `law.second_law_thermo`）。若其他 claim 引用它，将引用重定向至 `law.second_law_thermo`
  - 更新所有 claims.yaml 内部引用这三个 ID 的其他条目

  **Must NOT do**:
  - 不要改动 frameworks.yaml 中真实的 13 个 kernel 节点
  - 不要删除 physics.scihf 或 LANGUAGE.md 中的条目（那是后续任务）
  - 不要改动 `law.pauli_exclusion` 在 effective_laws.yaml 中的既有定义（claims.yaml 与 effective_laws.yaml 需保持一致）

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: 需要理解 claims.yaml 的内部结构（1150 行），追踪所有引用，确保降级不破坏其他条目的依赖
  - **Skills**: []
  - **Skills Evaluated but Omitted**: None

  **Parallelization**:
  - **Can Run In Parallel**: Task 4-7 可并行（各自独立修改不同文件）
  - **Parallel Group**: Wave 2 (with Tasks 5, 6, 7)
  - **Blocks**: Task 8, Task 9（physics.scihf/LANGUAGE.md 需基于正确的 claims.yaml）
  - **Blocked By**: Task 3（幽灵节点清单）

  **References**:
  - `layer1/claims.yaml:650-720` — 幽灵 kernel 节点预计位置（line 656 起）
  - `layer1/effective_laws.yaml:210-227` — `law.pauli_exclusion` 的正确 derived_from 定义
  - `layer1/effective_laws.yaml:284-300` — `law.second_law_thermo` 的正确定义
  - `layer1/frameworks.yaml:160-179` — `kernel.lorentz_invariance` 的完整表述

  **Acceptance Criteria**:
  - [ ] claims.yaml 中无 `kernel.pauli_exclusion` 作为 `id:` 字段
  - [ ] claims.yaml 中无 `kernel.light_speed_invariance` 作为 `id:` 字段
  - [ ] claims.yaml 中无 `kernel.second_law` 作为 `id:` 字段
  - [ ] `law.pauli_exclusion` 的 `derived_from` 包含 `kernel.lorentz_invariance, kernel.superposition_principle, kernel.unitary_evolution`
  - [ ] 所有曾引用幽灵节点的 claims 条目更新为正确 ID

  **QA Scenarios**:

  ```
  Scenario: claims.yaml 幽灵节点已消除
    Tool: Bash (grep)
    Preconditions: Task 3 清单作为参考
    Steps:
      1. grep "id: kernel\.pauli_exclusion" layer1/claims.yaml → 应返回空
      2. grep "id: kernel\.light_speed_invariance" layer1/claims.yaml → 应返回空
      3. grep "id: kernel\.second_law" layer1/claims.yaml → 应返回空
      4. grep "id: law\.pauli_exclusion" layer1/claims.yaml → 应返回匹配
      5. grep -A5 "id: law\.pauli_exclusion" layer1/claims.yaml | grep "_from" → 应包含正确的 3 个 kernel 源
    Expected Result: 3 个幽灵节点消失，law.pauli_exclusion 正确声明
    Failure Indicators: 仍有 `kernel.pauli_exclusion` 的 id 声明；_from 仍为空
    Evidence: .sisyphus/evidence/task-4-claims-fix.txt

  Scenario: claims.yaml 内部交叉引用已更新
    Tool: Bash (grep)
    Steps:
      1. grep "kernel\.light_speed_invariance" layer1/claims.yaml → 应仅在注释中出现（非 derived_from/premise）
      2. grep "kernel\.second_law" layer1/claims.yaml → 应仅在注释中出现
    Expected Result: derived_from/premise 字段中无幽灵节点引用
    Evidence: .sisyphus/evidence/task-4-claims-fix-crossref.txt
  ```

  **Commit**: YES
  - Message: `fix: demote phantom kernel nodes in claims.yaml`
  - Files: `layer1/claims.yaml`

- [ ] 5. **修复 rigorous_derivations.yaml — 修正 premise 引用**

  **What to do**:
  - `deriv.fermi_dirac_distribution` (line ~1807): premise 中 `kernel.pauli_exclusion` → `law.pauli_exclusion`
  - `deriv.thermo_third_law` (line ~1662): 在 premise 中添加 `kernel.unitary_evolution` + `kernel.canonical_commutation` + `kernel.operator_observable`（因为推导明确需要 Schrödinger 方程的离散能谱）
  - `deriv.energy_frequency` (line ~1121): 在 premise 中添加 `kernel.gauge_interactions` + `kernel.least_action` + `kernel.lorentz_invariance`（因为需要 Maxwell 方程确定电磁场动力学 → 谐振子模式）
  - `deriv.lorentz_transformation` (line ~1278): 删除重复的 `kernel.lorentz_invariance` 行（当前 line 1283 是重复的）
  - 检查所有 deriv.* 条目的 premise 与 effective_laws.yaml 的 derived_from 一致性

  **Must NOT do**:
  - 不要重写推导步骤本身（仅修正 premise 和 necessity_conditions）
  - 不要改动 Lovelock 相关文本或 de Broglie 的经验性标注

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: 1903 行 YAML，需要精确追踪每条 deriv 的 premise 与 effective_laws 的 derived_from 对应关系
  - **Skills**: []
  - **Skills Evaluated but Omitted**: None

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 4, 6, 7)
  - **Parallel Group**: Wave 2
  - **Blocks**: Task 10（source_graph 验证）
  - **Blocked By**: Task 3（幽灵节点清单）

  **References**:
  - `layer1/rigorous_derivations.yaml:1807-1858` — deriv.fermi_dirac_distribution 的定义位置
  - `layer1/rigorous_derivations.yaml:1662-1705` — deriv.thermo_third_law 的定义位置
  - `layer1/rigorous_derivations.yaml:1121-1178` — deriv.energy_frequency 的定义位置
  - `layer1/rigorous_derivations.yaml:1278-1358` — deriv.lorentz_transformation 的定义位置
  - `layer1/effective_laws.yaml` — 所有 derived_from 字段作为基准

  **Acceptance Criteria**:
  - [ ] `deriv.fermi_dirac_distribution.premise` 中无 `kernel.pauli_exclusion`
  - [ ] `deriv.thermo_third_law.premise` 包含 `kernel.unitary_evolution`、`kernel.canonical_commutation`、`kernel.operator_observable`
  - [ ] `deriv.energy_frequency.premise` 包含电磁场相关的前提
  - [ ] `deriv.lorentz_transformation.premise` 无重复的 `kernel.lorentz_invariance`

  **QA Scenarios**:

  ```
  Scenario: 幽灵节点已从 rigorous_derivations 消除
    Tool: Bash (grep)
    Steps:
      1. grep "kernel\.pauli_exclusion" layer1/rigorous_derivations.yaml → 应仅在注释中
      2. grep "kernel\.light_speed_invariance" layer1/rigorous_derivations.yaml → 应仅在注释中
      3. grep "kernel\.second_law" layer1/rigorous_derivations.yaml → 应仅在注释中
    Expected Result: premise 字段中无幽灵节点
    Evidence: .sisyphus/evidence/task-5-rigorous-fix.txt

  Scenario: therm_third_law premise 完整
    Tool: Bash (grep)
    Steps:
      1. grep -A10 "id: deriv.thermo_third_law" layer1/rigorous_derivations.yaml | grep "kernel.unitary_evolution"
      2. grep -A10 "id: deriv.thermo_third_law" layer1/rigorous_derivations.yaml | grep "kernel.canonical_commutation"
    Expected Result: 两条新增前提均存在
    Evidence: .sisyphus/evidence/task-5-third-law-premise.txt
  ```

  **Commit**: YES
  - Message: `fix: correct derivation premises to remove phantom kernel refs`
  - Files: `layer1/rigorous_derivations.yaml`

- [ ] 6. **修复 effective_laws.yaml — 补充缺失 derived_from**

  **What to do**:
  - `law.third_law_thermo` (line ~321): 当前 `derived_from: [kernel.boltzmann_entropy, kernel.superposition_principle]` → 添加 `kernel.unitary_evolution`、`kernel.canonical_commutation`、`kernel.operator_observable`（因为需要离散能谱 = Schrödinger 方程的前提）
  - `cor.fermi_dirac` (line ~498): 当前 `derived_from: [law.pauli_exclusion, kernel.boltzmann_entropy]` → 保持不变（law.pauli_exclusion 已被正确定义于 effective_laws），但需确认 `law.pauli_exclusion` 的完整参照链可追溯至 R1-R6
  - `law.energy_frequency` (line ~227): 当前 `derived_from: [kernel.canonical_commutation, kernel.least_action, kernel.unitary_evolution, kernel.spacetime_dimensionality]` → 添加 `kernel.gauge_interactions`（需要电磁场动力学 = Maxwell → R3）
  - `law.de_broglie_wavelength` (line ~242): 在 relation 字段添加注释说明其为经验性推广非纯逻辑推导（不改变 derived_from 结构）

  **Must NOT do**:
  - 不要改变 law.pauli_exclusion 的 derived_from
  - 不要在此轮将 de Broglie 重新分类为 contingent

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 几条 derived_from 字段的精确定点修改
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 4, 5, 7)
  - **Parallel Group**: Wave 2
  - **Blocks**: Task 10
  - **Blocked By**: Task 3

  **References**:
  - `layer1/effective_laws.yaml:321-333` — law.third_law_thermo 当前定义
  - `layer1/effective_laws.yaml:227-241` — law.energy_frequency 当前定义
  - `layer1/effective_laws.yaml:242-254` — law.de_broglie_wavelength 当前定义

  **Acceptance Criteria**:
  - [ ] `law.third_law_thermo.derived_from` 包含 kernel.unitary_evolution, kernel.canonical_commutation, kernel.operator_observable
  - [ ] `law.energy_frequency.derived_from` 包含 kernel.gauge_interactions
  - [ ] `law.de_broglie_wavelength.relation` 末尾有 `[NOTE: empirical generalization, not pure logical deduction from E=hν]` 注释

  **QA Scenarios**:

  ```
  Scenario: 缺失前提已补充
    Tool: Bash (grep)
    Steps:
      1. grep -A15 "id: law.third_law_thermo" layer1/effective_laws.yaml | grep "kernel.unitary_evolution"
      2. grep -A15 "id: law.third_law_thermo" layer1/effective_laws.yaml | grep "kernel.canonical_commutation"
      3. grep -A15 "id: law.energy_frequency" layer1/effective_laws.yaml | grep "kernel.gauge_interactions"
    Expected Result: 所有检查项均返回匹配
    Evidence: .sisyphus/evidence/task-6-laws-fix.txt
  ```

  **Commit**: YES
  - Message: `fix: add missing derived_from premises for third law and energy-frequency`
  - Files: `layer1/effective_laws.yaml`

- [ ] 7. **修复 rules.md — 清理冗余和表引用**

  **What to do**:
  - **R1.8 子组件表** (line ~122-129): 将 `kernel.light_speed_invariance` 条目改为 `kernel.lorentz_invariance` 的注释子项，标注 "（等价表述，已合并入 kernel.lorentz_invariance）"
  - **R6.1 第二定律陈述** (line ~553-555): 添加注释说明 "ΔS ≥ 0 是统计推论，其精确表述见 law.second_law_thermo"
  - **定理推导清单** (line ~735): 将 Fermi-Dirac 的前提列从 `kernel.pauli_exclusion` 更新为 `law.pauli_exclusion`
  - **派生定理** (line ~657): "自旋-统计定理是 R2/R4 的数学推论" → 保持不变。但在 Pauli 不相容原理的引用处添加括号说明 "(← 自旋-统计定理 ← R4+R1)"
  - **R1-R6 依赖图** (line ~665-696): 如有引用 `kernel.*` 但实际 ID 已变的，同步更新

  **Must NOT do**:
  - 不要修改 R1-R6 的核心陈述（只修表、注释、引用）
  - 不要删除任何规则（这超出了本修复的范围）

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 精确的文本修改（表、注释、引用），不涉及结构重构
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 4, 5, 6)
  - **Parallel Group**: Wave 2
  - **Blocks**: None（下游无依赖 rules.md 的任务）
  - **Blocked By**: Task 3

  **References**:
  - `rules.md:122-129` — R1.8 子组件表
  - `rules.md:553-555` — R6.1 第二定律部分
  - `rules.md:735` — 定理推导清单 Fermi-Dirac 行
  - `rules.md:657` — 派生定理表

  **Acceptance Criteria**:
  - [ ] R1.8 表中的 kernel.light_speed_invariance 已标注为合并项
  - [ ] R6.1 有注释说明第二定律的推导性质
  - [ ] 定理推导清单中 Fermi-Dirac 引用 law.pauli_exclusion（非 kernel）

  **QA Scenarios**:

  ```
  Scenario: rules.md 引用一致性
    Tool: Bash (grep)
    Steps:
      1. grep "kernel\.light_speed_invariance" rules.md → 应仅在注释/表说明中（非活跃引用）
      2. grep "kernel\.pauli_exclusion" rules.md → 不应出现在推导清单中（如出现则应为注释）
      3. grep "law\.pauli_exclusion" rules.md → 推导清单中应有此引用
    Expected Result: 幽灵节点不在活跃引用位置
    Evidence: .sisyphus/evidence/task-7-rules-fix.txt
  ```

  **Commit**: YES
  - Message: `fix: clean up rules.md references for kernel node migration`
  - Files: `rules.md`

---

### Wave 3: 传播同步

- [ ] 8. **修复 physics.scihf — 同步 .scihf 示例**

  **What to do**:
  - 搜索 physics.scihf 中所有引用 `kernel.pauli_exclusion`、`kernel.light_speed_invariance`、`kernel.second_law` 的行
  - 将示例中的 `kernel.pauli_exclusion` → `law.pauli_exclusion`
  - 将示例中的 `kernel.light_speed_invariance` → 删除或替换为 `kernel.lorentz_invariance`
  - 将示例中的 `kernel.second_law` → `law.second_law_thermo`
  - 确保修改后的 .scihf 语法仍符合 LANGUAGE.md 规范

  **Must NOT do**:
  - 不要改动 .scihf 的语法结构（只改 ID 字符串）

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 搜索替换 ID 字符串，不涉及语法变更
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 9)
  - **Parallel Group**: Wave 3 (depends on Task 4, 5, 6, 7 completion)
  - **Blocks**: Task 10
  - **Blocked By**: Tasks 4, 5, 6, 7

  **References**:
  - `layer1/physics.scihf:440-460` — .scihf 示例中幽灵节点的估计位置
  - `layer1/LANGUAGE.md` — 确认 .scihf 语法规范

  **Acceptance Criteria**:
  - [ ] physics.scihf 中无 `kernel.pauli_exclusion`（或仅在注释中）
  - [ ] physics.scihf 中无 `kernel.light_speed_invariance`（或仅在注释中）
  - [ ] physics.scihf 中无 `kernel.second_law`（或仅在注释中）

  **QA Scenarios**:

  ```
  Scenario: physics.scihf 语法示例已同步
    Tool: Bash (grep)
    Steps:
      1. grep "kernel\.pauli_exclusion\|kernel\.light_speed_invariance\|kernel\.second_law" layer1/physics.scihf
      2. 确认返回空（或全部在注释中）
    Expected Result: 0 活跃引用
    Evidence: .sisyphus/evidence/task-8-scihf-fix.txt
  ```

  **Commit**: YES (groups with Task 9)
  - Message: `fix: sync scihf examples for kernel node migration`
  - Files: `layer1/physics.scihf`

- [ ] 9. **修复 LANGUAGE.md — 同步语法示例**

  **What to do**:
  - 搜索 LANGUAGE.md 中所有引用幽灵 kernel 节点的 token/node 示例
  - 将示例中的 ID 更新为与 claims.yaml 一致的版本
  - 更新 kernel/law 节点数量描述（如适用）

  **Must NOT do**:
  - 不要重写 .scihf 语法规范（只改示例中的 ID）

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 精确的 ID 字符串替换
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 8)
  - **Parallel Group**: Wave 3
  - **Blocks**: Task 10
  - **Blocked By**: Tasks 4, 5, 6, 7

  **References**:
  - `layer1/LANGUAGE.md:270-280` — 语法示例中幽灵节点的估计位置
  - `layer1/claims.yaml` — 修改后的正确 ID

  **Acceptance Criteria**:
  - [ ] LANGUAGE.md 示例中的 ID 与 claims.yaml 一致

  **QA Scenarios**:

  ```
  Scenario: LANGUAGE.md 示例已同步
    Tool: Bash (grep)
    Steps:
      1. grep "kernel\.pauli_exclusion\|kernel\.light_speed_invariance\|kernel\.second_law" layer1/LANGUAGE.md
      2. 确认返回空（或仅在历史/说明性文本中）
    Expected Result: 语法示例中无幽灵节点引用
    Evidence: .sisyphus/evidence/task-9-language-fix.txt
  ```

  **Commit**: YES (groups with Task 8)
  - Message: `fix: sync scihf examples for kernel node migration`
  - Files: `layer1/LANGUAGE.md`

---

### Wave 4: 验证

- [ ] 10. **运行 post-fix source_graph 审查**

  **What to do**:
  - 运行 `python3 -m mvp.source_graph --layer1 reference/layer1 --output /tmp/post-fix-review.md`
  - 与 `/tmp/pre-fix-review.md` 对比差异
  - 验证 V1-V5 全部 PASS
  - 记录 node/edge 计数变化（预期：-3 kernel nodes, +1 effective_law node, net -2 nodes）

  **Must NOT do**:
  - 如果 V1-V5 有任何 FAIL，不要继续后续任务——回 Task 4-9 修复

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 执行命令 + 对比输出
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 4 (depends on ALL Wave 3 tasks)
  - **Blocks**: Task 11, F1-F4
  - **Blocked By**: Tasks 8, 9

  **References**:
  - `/tmp/pre-fix-review.md` — baseline 对比
  - `layer1/SOURCE.md` — V1-V5 规范

  **Acceptance Criteria**:
  - [ ] post-fix source_graph V1-V5 ALL PASS
  - [ ] node 计数合理变化（-2 至 -3 nodes 预期）
  - [ ] 与 baseline diff 仅包含预期的变更

  **QA Scenarios**:

  ```
  Scenario: post-fix 审查全部通过
    Tool: Bash
    Steps:
      1. cd /home/room115/physics-foundations && python3 -m mvp.source_graph --layer1 reference/layer1 --output /tmp/post-fix-review.md
      2. grep "Overall" /tmp/post-fix-review.md
      3. grep "V1:" /tmp/post-fix-review.md && grep "V2:" /tmp/post-fix-review.md && grep "V3:" /tmp/post-fix-review.md && grep "V4:" /tmp/post-fix-review.md && grep "V5:" /tmp/post-fix-review.md
      4. diff /tmp/pre-fix-review.md /tmp/post-fix-review.md
    Expected Result: ALL PASS, diff 仅含预期变更（kernel 节点减少，effective_law 节点增加）
    Failure Indicators: 任何 FAIL → 需要回 Task 4-9 修复
    Evidence: .sisyphus/evidence/task-10-postfix.txt
  ```

  **Commit**: NO（验证任务）

- [ ] 11. **跨文件引用一致性审计**

  **What to do**:
  - 对 frameworks.yaml 的 13 个 kernel 节点，验证所有 effective_laws.yaml 的 derived_from 引用都存在（V1 检查由 source_graph 覆盖，此任务做人类可读的语义验证）
  - 验证以下关键推导链完整：
    - `cor.fermi_dirac` → `law.pauli_exclusion` → `kernel.lorentz_invariance` + `kernel.superposition_principle` + `kernel.unitary_evolution`
    - `law.third_law_thermo` → `kernel.boltzmann_entropy` + `kernel.superposition_principle` + `kernel.unitary_evolution` + `kernel.canonical_commutation` + `kernel.operator_observable`
    - `law.lorentz_transform` → `kernel.lorentz_invariance`（不引用已删除的 kernel.light_speed_invariance）
  - 验证 derivations.yaml（如存在）与 rigorous_derivations.yaml 之间无冲突

  **Must NOT do**:
  - 不要修改任何文件（审计发现问题 → 记录为失败项，回 Task 4-9 修复）

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: 需要理解全部推导链的语义关系，执行跨文件引用追踪
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 4 (after Task 10)
  - **Blocks**: F1-F4
  - **Blocked By**: Task 10

  **References**:
  - `layer1/frameworks.yaml` — 真实 kernel 节点清单
  - `layer1/effective_laws.yaml` — 所有 derived_from 字段
  - `layer1/rigorous_derivations.yaml` — 所有 premise 字段

  **Acceptance Criteria**:
  - [ ] 关键推导链 3 条全部通过语义验证
  - [ ] 无 dangling references（derived_from 指向不存在的 ID）
  - [ ] derivations.yaml 与 rigorous_derivations.yaml 无冲突

  **QA Scenarios**:

  ```
  Scenario: 关键推导链完整性
    Tool: Bash (grep + manual trace)
    Steps:
      1. 从 cor.fermi_dirac 开始，逐级追溯 derived_from 至 kernel.* 根节点
      2. 从 law.third_law_thermo 开始，逐级追溯至 kernel.* 根节点
      3. 从 law.lorentz_transform 开始，确认不经过已删除节点
    Expected Result: 三条链均可达 kernel 根，无断裂
    Evidence: .sisyphus/evidence/task-11-audit.txt
  ```

  **Commit**: NO（审计任务）

- [ ] 12. **重新生成 atom 表并更新 layer1/README.md**

  **What to do**:
  - 运行 source_graph checker 重新生成完整的 atom 清单
  - 将输出中的 atom 表部分（`| Atom ID | Layer | Source file | Logical sources |` 格式）替换 layer1/README.md 中对应的表格
  - 更新 README.md 中的 node/edge 计数

  **Must NOT do**:
  - 不要手动编写 atom 表（必须由 source_graph 自动生成）

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 运行命令 + 复制输出到 README
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 11)
  - **Parallel Group**: Wave 4
  - **Blocks**: F1-F4
  - **Blocked By**: Task 10

  **References**:
  - `layer1/README.md` — atom 表位置
  - `/tmp/post-fix-review.md` — source_graph 输出

  **Acceptance Criteria**:
  - [ ] atom 表不包含 `kernel.pauli_exclusion`、`kernel.light_speed_invariance`、`kernel.second_law`
  - [ ] atom 表包含 `law.pauli_exclusion`（layer: effective_law）
  - [ ] node/edge 计数与 post-fix source_graph 输出一致

  **QA Scenarios**:

  ```
  Scenario: atom 表已同步
    Tool: Bash (grep)
    Steps:
      1. grep "kernel\.pauli_exclusion\|kernel\.light_speed_invariance\|kernel\.second_law" layer1/README.md → 应返回空
      2. grep "law\.pauli_exclusion" layer1/README.md → 应返回匹配
    Expected Result: 幽灵节点从 atom 表中消失
    Evidence: .sisyphus/evidence/task-12-readme.txt
  ```

  **Commit**: YES
  - Message: `fix: regenerate atom table after kernel node migration`
  - Files: `layer1/README.md`

---

## Final Verification Wave

- [ ] F1. **Plan Compliance Audit** — `oracle`
  Read the plan end-to-end. Verify all "Must Have" items satisfied, all "Must NOT Have" constraints respected. Check evidence files exist in `.sisyphus/evidence/`. Compare deliverables against plan.
  Output: `Must Have [N/N] | Must NOT Have [N/N] | Tasks [N/N] | VERDICT: APPROVE/REJECT`

- [ ] F2. **Code Quality Review** — `unspecified-high`
  Run `python3 -m mvp.source_graph --layer1 reference/layer1 --output /tmp/post-fix-review.md`. Verify V1-V5 ALL PASS. Check YAML syntax validity. Review all changed files for formatting consistency.
  Output: `Build [PASS/FAIL] | V1-V5 [N pass/N fail] | Files [N clean/N issues] | VERDICT`

- [ ] F3. **Real Manual QA** — `unspecified-high`
  Execute EVERY QA scenario from EVERY task. Verify no phantom kernel node references remain. Verify all derivation chains traceable to R1-R6. Save evidence to `.sisyphus/evidence/final-qa/`.
  Output: `Scenarios [N/N pass] | Integration [N/N] | VERDICT`

- [ ] F4. **Scope Fidelity Check** — `deep`
  For each task: verify exactly what was specified was changed, nothing beyond scope. Check "Must NOT do" compliance. Detect cross-task contamination. Flag unaccounted changes.
  Output: `Tasks [N/N compliant] | Contamination [CLEAN/N issues] | VERDICT`

---

## Commit Strategy

- **1**: `fix: restore mvp module symlink for source_graph verification` — `.sisyphus/plans/`, mvp symlink
- **2**: `fix: demote phantom kernel nodes and fix derivation premises` — claims.yaml, rigorous_derivations.yaml, effective_laws.yaml
- **3**: `fix: update rules.md and scihf examples for kernel node migration` — rules.md, physics.scihf, LANGUAGE.md

---

## Success Criteria

### Verification Commands
```bash
# Pre and post fix comparison
python3 -m mvp.source_graph --layer1 reference/layer1 --output /tmp/post-fix-review.md

# Phantom node elimination check (should return 0 for derived_from/premise fields)
grep -r "kernel\.pauli_exclusion" layer1/*.yaml | grep -v "^[^:]*:#"
grep -r "kernel\.light_speed_invariance" layer1/*.yaml
grep -r "kernel\.second_law" layer1/*.yaml

# Cross-reference consistency
# Every derived_from ID must resolve to a defined node
```

### Final Checklist
- [ ] V1-V5 ALL PASS after fixes
- [ ] 0 phantom kernel node references in YAML derived_from/premise fields
- [ ] law.third_law_thermo derived_from includes all required kernel components
- [ ] cor.fermi_dirac chain traces to R1-R6 via law.pauli_exclusion
- [ ] rules.md table and references consistent with frameworks.yaml
