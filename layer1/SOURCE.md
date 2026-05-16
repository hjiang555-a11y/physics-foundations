# Source Node — 形式化规范

**版本**: 1.0
**依赖**: LANGUAGE.md §1 (Node 类型 N4, N8), LANGUAGE.md §2 (BNF)
**读者**: 实现者（parser/checker 开发者）、AI 审查系统

---

## 1. 定义 Definition

### 1.1 Source 是什么

`← parent₁, parent₂, ...` 声明了一条**逻辑推导依赖**：

> 本断言为真，**因为** parent₁, parent₂, ... 为真（加上推导步骤）。

Source 是 `Assertion(N4)` 的必选子节点（对 law 和 corollary）或禁止子节点（对 kernel）。

### 1.2 Source 不是什么

| 误解 | 纠正 |
|------|------|
| Source 是文献引用 | 文献引用在 `provenance` 字段。Source 是**逻辑前提**。 |
| Source 是"相关阅读" | Source 是**推导的必要条件**。移除 source 中的任何一条，推导不成立。 |
| Source 是可选的元数据 | 对 law/corollary，source **必须非空**。无 source 的 law 是无效的。 |
| Source 只是记录 | Source 是**可机验的图结构**。系统必须在加载时验证其一致性。 |

### 1.3 形式定义

```
设 A 为知识库中所有 Assertion 的集合。
设 S: A → P(A) 为 source 函数：S(a) = {p ∈ A | p.id ∈ a.source}。

推导图 G = (A, E)，其中 E = {(a, p) | a ∈ A, p ∈ S(a)}。
边 (a, p) 读作: "a 逻辑依赖于 p"。
```

---

## 2. 推导图结构 Derivation Graph

### 2.1 四种节点角色

```
          ┌─────────────────────┐
          │  kernel (N=16)      │  indegree = 0  (无 source)
          │  推导的根            │  outdegree ≥ 0
          └────────┬────────────┘
                   │
          ┌────────▼────────────┐
          │  law (N=29)         │  indegree ≥ 1  (有 source)
          │  有效定律            │  outdegree ≥ 0
          └────────┬────────────┘
                   │
          ┌────────▼────────────┐
          │  corollary (N=3)    │  indegree ≥ 1
          │  推论               │  outdegree = 0  (无被依赖)
          └─────────────────────┘

          ┌─────────────────────┐
          │  contingent (N=9)   │  indegree ≥ 0
          │  经验事实            │  outdegree ≥ 0
          └─────────────────────┘
```

### 2.2 关键性质

| 性质 | 定义 | 违反意味着 |
|------|------|-----------|
| **无环性** | G 中不存在环路 | 循环论证 — 至少一条断言错误 |
| **根可达性** | 每个 law/corollary 存在一条路径到达至少一个 kernel | 推导链断裂 — 前提缺失 |
| **层次单调性** | 沿边方向，层次只能升不能降：corollary → law → kernel | 层次逆流 — 推导顺序错误 |
| **最小性** | S(a) 中不包含冗余前提（移除任一条，a 不能再被推导） | 过度声明 — 不精确 |
| **去重性** | S(a) 中同一 parent ID 只能出现一次 | 重复前提 — 存储漂移 |

---

## 3. 验证规则 Validation Rules

以下规则在 parser 构建 AST 后由 checker 强制。**任何一条失败 → 知识库拒绝加载**。

### V1: 引用解析 Reference Resolution

```
∀ a ∈ A, ∀ p_id ∈ a.source:
  ∃ p ∈ A such that p.id = p_id
```

检查方式：遍历所有 Assertion(N4) 的 Source(N8)，验证每个 ID 在 Program(N1) 中存在对应的 Assertion。

**示例违反**：
```
[law] F = m·a ← kernel.nonexistent    ;; V1 失败：kernel.nonexistent 不存在
```

### V2: 无环性 Acyclicity

```
不存在序列 a₁, a₂, ..., aₖ 使得:
  a₁ ∈ S(a₂) ∧ a₂ ∈ S(a₃) ∧ ... ∧ aₖ ∈ S(a₁)
```

检查方式：对 G 运行拓扑排序。若无法生成全序 → 存在环路。

**示例违反**：
```
a: [law] X = Y ← b
b: [law] Y = Z ← a            ;; V2 失败：a → b → a 循环
```

### V3: 层次序 Layer Discipline

```
∀ a ∈ A:
  a.layer = kernel      ⇒ S(a) = ∅
  a.layer = contingent  ⇒ S(a) = ∅  (除非 a 标注了 derived_from)
  a.layer = law         ⇒ ∀ p ∈ S(a): p.layer ∈ {kernel, law}
  a.layer = corollary   ⇒ ∀ p ∈ S(a): p.layer ∈ {law, corollary}
```

检查方式：对每个 Assertion(N4)，检查其 Source(N8) 指向的 Assertion 的 layer 属性。

**示例违反**：
```
[kernel] δS = 0 ← kernel.noether    ;; V3 失败：kernel 不能有 source

[law] E = m·c² ← cor.kepler_third   ;; V3 失败：law 不能 source from corollary

[corollary] T² ∝ r³ ← kernel.least_action  ;; V3 失败：corollary 只能 source from law/corollary
```

### V4: 根可达性 Root Reachability（连通性）

```
∀ a ∈ A where a.layer ∈ {law, corollary}:
  ∃ k ∈ A such that k.layer = kernel ∧ 存在路径 a → ... → k
```

检查方式：对每个 law/corollary，反向 BFS 遍历 source 边。终止于 kernel 或 contingent 节点。若遍历结束未到达 kernel → 失败。

注意：contingent 断言不计入根可达性要求。一条 law 可以仅从 contingent + kernel 推导，但不能仅从 contingent 推导（必须有 kernel 支撑）。

**示例违反**：
```
a: [law] X = Y ← b
b: [law] Y = Z ← c
c: [law] Z = W               ;; V4 失败：链路 a→b→c，c 无 kernel 根
```

### V5: Source-Derivation 一致性（若 Derivation 存在）

```
若存在 d ∈ Derivations such that d.conclusion = a.id:
  则 d.premise ⊆ S(a)   (所有声明的推导前提都必须出现在 source 中)
  且 S(a) ⊆ d.premise   (所有 source 中的前提都必须出现在推导中)
```

即：`S(a) = d.premise` 当存在对应 Derivation 时。若不存在 Derivation 条目，V5 跳过（仅记录警告）。

同一 assertion 的 contingent 支撑项若需要可机验，应先在 `contingent.yaml` 中形成独立 `contingent.*` 节点，再由 Derivation 指向该节点；不得把无对应 assertion 的支撑推导混入 law/kernel 的 `conclusion`。

---

## 4. 操作语义 Operations

以下操作定义在推导图 G 上。实现者必须提供这些操作，AI 审查系统使用它们进行诊断。

### O1: Ancestors(a) — 全祖先

```
Ancestors(a) = S(a) ∪ ⋃_{p ∈ S(a)} Ancestors(p)
```

返回 a 的直接和间接逻辑前提的**全集**。

用途：追溯一条推论的完整前提链。

示例：
```
cor.kepler_third 的 Ancestors = {
  law.newton_second,                    ;; 直接 source
  law.newton_gravitation,               ;; 直接 source
  kernel.least_action,                  ;; 通过 newton_second
  law.euler_lagrange,                   ;; 通过 newton_second
  kernel.equivalence_principle,         ;; 通过 newton_gravitation
  kernel.general_covariance             ;; 通过 newton_gravitation
}
```

### O2: Descendants(a) — 全后代

```
Descendants(a) = {d ∈ A | a ∈ Ancestors(d)}
```

返回**直接或间接**依赖于 a 的所有断言。

用途：影响分析 — 若 a 被修正或推翻，Descendants(a) 全部需要重新验证。

### O3: Roots(a) — 内核根

```
Roots(a) = {r ∈ Ancestors(a) | r.layer = kernel}
```

返回 a 最终依赖的所有内核公理。

用途：检测 a 的内核基础是否充分。

示例：
```
cor.fermi_dirac 的 Roots = {law.pauli_exclusion, kernel.boltzmann_entropy}
```

### O4: ImpactSet(a) — 影响集

```
ImpactSet(a) = Descendants(a)
```

当断言 a 被标记为"需重新验证"时，ImpactSet(a) 中的所有断言也需要重新验证。

实现注意：当一条 kernel 断言被修改时，所有 law 和 corollary 可能受影响。系统应标记 ImpactSet 而非级联拒绝。

### O5: Path(a, b) — 推导路径

```
Path(a, b) = 若 b ∈ Ancestors(a)，返回从 a 到 b 的最短 source 边序列
             否则返回 null
```

用途：解释 a 是如何从 b 推出的。

### O6: ContradictionSource(A, B) — 矛盾溯源

```
若 A 和 B 矛盾（两者不能同时为真）：
  CommonAncestors = Ancestors(A) ∩ Ancestors(B)
  DivergencePoint  = 最大的 c ∈ CommonAncestors 使得
                     存在 a ∈ S*(A)−S*(B) 且 b ∈ S*(B)−S*(A)
                     且 c ∈ Ancestors(a) ∩ Ancestors(b)
```

用途：当两个断言冲突时，定位推导分叉点 — 这是修正的起点。

---

## 5. Source 与 Derivation 的关系

Source 和 Derivation 是两个不同的概念，共同描述推导：

| | Source (←) | Derivation |
|---|-----------|------------|
| **记录什么** | 逻辑前提（WHAT） | 推导步骤（HOW） |
| **存储位置** | `.scihf` 文件中的 `←` 或 YAML 中的 `derived_from` | `derivations.yaml` 中的 `steps` |
| **是否必需** | 对 law/corollary 是 | 对非平凡推导推荐，非强制 |
| **验证级别** | V1-V4 强制 | V5 在有 Derivation 时强制 |

YAML 文件到 Source/Derivation 节点的确定性抽取顺序见 [`EXTRACTION.md`](EXTRACTION.md)。

### 5.1 一致性约束

```
设 D(a) = {d ∈ Derivations | d.conclusion = a.id}

若 D(a) ≠ ∅:
  则对于每个 d ∈ D(a):
    d.premise = S(a)     ;; 前提集合必须一致
    d.steps ≠ []          ;; 推导步骤不能为空

若 D(a) = ∅:
  S(a) 仍然必须满足 V1-V4，但 V5 不适用。
  系统输出 INFO 级别日志："a 声明了 source 但无对应 Derivation 条目。"
```

### 5.2 推导链的完整性

一个完整的推导链应满足：

```
对于断言 a，存在 Derivation 条目 d 使得：
  1. d.conclusion = a.id
  2. d.premise = S(a)
  3. 对于每个 p ∈ S(a)，存在 Derivation 条目 d' 使得 d'.conclusion = p.id
     （递归至 kernel）
```

即：从 kernel 到任意 law/corollary 的路径上，每一步都有对应的 Derivation 条目。

---

## 6. AI 审查协议 AI Review Protocol

当 AI 系统审查知识库时，Source 图提供以下审查能力：

### 6.1 结构完整性检查 Structural Integrity

| 检查项 | 使用操作 | 通过标准 |
|--------|---------|---------|
| 无孤立节点 | 对所有 a: `|Ancestors(a)| > 0` 或 `a.layer = kernel` | 所有 law/corollary 有祖先 |
| 无悬空引用 | V1 检查 | 所有 source ID 解析成功 |
| 无环路 | V2 检查 | 拓扑排序成功 |
| 层次合规 | V3 检查 | 无跨层 source |

### 6.2 推导充分性检查 Derivational Adequacy

| 检查项 | 方法 | 通过标准 |
|--------|------|---------|
| 内核覆盖 | 对所有 kernel k: `|Descendants(k)| > 0` | 每个 kernel 至少被一条 law 引用 |
| 推导链完整 | 对所有 law l: `Path(l, k)` 存在且所有边有 Derivation | 无"跳跃推导" |
| 无冗余 kernel | 对所有 kernel k₁, k₂: 若 `Descendants(k₁) = Descendants(k₂)` 且 k₁ ≠ k₂ | 警告可能冗余 |

### 6.3 审查报告格式

AI 审查器应输出以下格式：

```
SOURCE GRAPH REVIEW REPORT
==========================
Graph size: N nodes, E edges

PASS:  V1 Reference Resolution    (N/A violations)
PASS:  V2 Acyclicity              (no cycles detected)
FAIL:  V3 Layer Discipline        (3 violations, see below)
PASS:  V4 Root Reachability       (all laws reachable)

VIOLATIONS:
  V3: [corollary] T² ∝ r³ ← kernel.least_action
      Fix: kernel.least_action → law.newton_second
      (corollary cannot directly source from kernel)

ORPHANS:
  kernel.boltzmann_entropy: 11 descendants
  (structural axiom — may be intentional)

WARNINGS:
  law.em_wave_equation: no Derivation entry
  (source chain exists but derivation steps not recorded)
```

---

## 7. 伪代码参考 Pseudocode

以下伪代码供实现者参考。函数签名和语义是规范性的；具体实现可以优化。

```
function validate_source_graph(assertions: List[Assertion]) -> ValidationReport:
    id_map = {a.id: a for a in assertions}
    
    report = ValidationReport()
    
    // V1: Reference resolution
    for each a in assertions:
        for each p_id in a.source:
            if p_id not in id_map:
                report.add_violation(V1, a.id, f"unresolved source: {p_id}")
    
    // V2: Acyclicity
    if has_cycle(assertions):
        report.add_violation(V2, "cycle detected")
    
    // V3: Layer discipline
    for each a in assertions:
        for each p_id in a.source:
            p = id_map[p_id]
            if a.layer == "kernel":
                report.add_violation(V3, a.id, "kernel has source")
            if a.layer == "law" and p.layer not in {"kernel", "law"}:
                report.add_violation(V3, a.id, f"law sources from {p.layer}")
            if a.layer == "corollary" and p.layer not in {"law", "corollary"}:
                report.add_violation(V3, a.id, f"corollary sources from {p.layer}")
    
    // V4: Root reachability
    for each a in assertions where a.layer in {"law", "corollary"}:
        roots = find_roots(a, id_map)
        kernel_roots = {r for r in roots if r.layer == "kernel"}
        if not kernel_roots:
            report.add_violation(V4, a.id, "no kernel root reachable")
    
    return report

function has_cycle(assertions) -> bool:
    // Tarjan's SCC or Kahn's topological sort
    indegree = {a.id: 0 for a in assertions}
    for each a in assertions:
        for each p_id in a.source:
            indegree[a.id] += 1
    queue = [a.id for a in assertions if indegree[a.id] == 0]
    visited = 0
    while queue:
        id = queue.pop(0)
        visited += 1
        for each a in assertions:
            if id in a.source:
                indegree[a.id] -= 1
                if indegree[a.id] == 0:
                    queue.append(a.id)
    return visited != len(assertions)

function ancestors(a: Assertion, id_map: Map) -> Set[Assertion]:
    result = set()
    for p_id in a.source:
        p = id_map[p_id]
        result.add(p)
        result.update(ancestors(p, id_map))
    return result

function find_roots(a: Assertion, id_map: Map) -> Set[Assertion]:
    all_ancestors = ancestors(a, id_map)
    return {x for x in all_ancestors if not x.source}  // no further source = root
```
