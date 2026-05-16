# 基本规则 — 精炼版 (Round 1)

> 物理世界最底层基础的 6 条核心原则。每一条均按"充分且必要"标准描述：
> 变量完整定义、数学表达式精确、成立条件与失效边界明确、必要性论证、充分性论证。
> 除数值参数与 contingent 事实外，所有已知物理定律均可由这 6 条原则推出。
> 
> **Round 11 (2026-05-16) 审计修正**：R1 重构为三独立子原则（明确 1c 等效原理的独立公设地位）；
> R3.3 新增 U(1) 规范群选择显式声明；R6 重构为两独立公设（6a S=k_B ln W + 6b 等概率先验）；
> 移除 `kernel.second_law` 和 `kernel.pauli_exclusion` 的 kernel 层错误分类（第二定律为有效定律，Pauli 由 R1+R4 导出）。

---

## 符号与量纲约定

| 量纲符号 | 含义 | SI 单位 |
|---------|------|--------|
| T | 时间 | s |
| L | 长度 | m |
| M | 质量 | kg |
| I | 电流 | A |
| Θ | 热力学温度 | K |
| N | 物质的量 | mol |
| J | 发光强度 | cd |

向量 **v** ∈ ℝ³；张量以指标记法 $T^{\mu\nu}$；$\partial_\mu \equiv \partial/\partial x^\mu$；$\nabla$ 为三维梯度算符。
希腊指标 $\mu,\nu,\lambda,\ldots \in \{0,1,2,3\}$（0 = 时间，1,2,3 = 空间）；拉丁指标 $i,j,k,\ldots \in \{1,2,3\}$。
Einstein 求和约定默认启用。度规符号约定 $(+,-,-,-)$。

**充分且必要判定标准**：
- **必要性 (Necessity)**：若移除或弱化本条，哪些已确认的物理定律将无法推出或与实验矛盾。
- **充分性 (Sufficiency)**：本条 + 前序规则组合，可覆盖的物理现象域与可导出的定理集合。

**跨规则物理常数**：

| 常数 | 符号 | 量纲 | 主要定义处 | 含义 |
|------|------|------|-----------|------|
| 真空光速 | $c$ | L·T⁻¹ | R1.2 | 因果传播速度上限；SI 定义常数 |
| 约化 Planck 常数 | $\hbar$ | M·L²·T⁻¹ | R4.2 | 量子作用量单元 |
| Boltzmann 常数 | $k_B$ | M·L²·T⁻²·Θ⁻¹ | R6.2 | 能量–温度转换标度 |
| Newton 引力常数 | $G$ | M⁻¹·L³·T⁻² | Einstein 场方程（← R1+R2） | 引力耦合强度；$G = 6.67430(15) \times 10^{-11}$ m³·kg⁻¹·s⁻²，**非 SI 定义常数**，仍由实验测定 |
| 真空介电常数 | $\varepsilon_0$ | M⁻¹·L⁻³·T⁴·I² | Maxwell 方程（← R3+R2+R1） | 真空电响应；$\varepsilon_0 \mu_0 c^2 = 1$ |
| 真空磁导率 | $\mu_0$ | M·L·T⁻²·I⁻² | Maxwell 方程（← R3+R2+R1） | 真空磁响应；$\mu_0 = 1/(\varepsilon_0 c^2)$ |

---

## R1. 因果时空结构 (Causal Spacetime Structure)

### R1.1 陈述

时空是四维 Lorentz 流形 $(\mathcal{M}, g_{\mu\nu})$，3 个空间维度和 1 个时间维度（$D=3$ 为本宇宙 contingent 事实，见 R1.2）。R1 包含**三个逻辑上独立但物理上紧密关联的子原则**：

**(1a) 最大传播速度**：真空中任何信号、能量或因果影响的传播速度不超过 $c$。$c$ 在所有惯性系中取相同数值——它是普适常数，不是特定参考系的属性。

**(1b) Lorentz 因果结构**（与 1a 等价）：时空间隔 $ds^2 = g_{\mu\nu}dx^\mu dx^\nu$ 的符号将事件对分为三类——类时（$ds^2 > 0$，可因果连接）、类光（$ds^2 = 0$，仅光速信号可连接）、类空（$ds^2 < 0$，无因果联系）。因为 $ds^2 = c^2dt^2 - |d\mathbf{r}|^2$，类空即 $|d\mathbf{r}|/dt > c$——所以"无超光速信号"（1a）与"类空事件无因果联系"（1b）是同一事实的两种表述。

**(1c) 等效原理（独立公设）**：惯性质量严格等于引力质量（$m_i = m_g$）。局域上，引力场与加速参考系不可区分。此原理与 1a/1b **逻辑独立**——光速不变 + Lorentz 因果结构本身不蕴含 $m_i = m_g$——但它是使引力成为时空几何的必要桥梁。正因为等效原理，度规 $g_{\mu\nu}$ 可升格为动力学场：广义协变性要求物理定律在所有坐标系中取相同形式；等效原理保证引力可被几何化。两者结合 ⇒ 引力即时空弯曲 ⇒ 广义相对论。

### R1.2 变量定义

| 变量 | 符号 | 类型 | 量纲 | 定义域 | 物理含义 |
|------|------|------|------|--------|---------|
| 时间坐标 | $t$ | $\mathbb{R}$ | T | $t \in \mathbb{R}$ | 类时坐标，参数化因果序列 |
| 空间坐标 | $x^i$ | $\mathbb{R}^3$ | L | $x^i \in \mathbb{R}$，$i \in \{1,2,3\}$ | 类空坐标，参数化同时性超曲面 |
| 时空坐标 | $x^\mu$ | $\mathbb{R}^4$ | — | $x^0 \equiv ct$，$x^i \equiv x^i$ | 4 维流形上的坐标系 |
| 度规张量 | $g_{\mu\nu}$ | $\mathbb{R}^{4\times4}$，对称 | [1] | $\det(g) < 0$；符号差 $(+,-,-,-)$ | 定义线元与因果结构 |
| 线元 | $ds^2$ | $\mathbb{R}$ | L² | $ds^2 \in \mathbb{R}$ | Lorentz 不变量；符号决定事件因果分类 |
| 真空光速 | $c$ | 常数 | L·T⁻¹ | $c = 2.99792458 \times 10^8$ m/s (exact) | 因果传播速度上限；SI 定义常数 |
| 固有时间 | $\tau$ | $\mathbb{R}_{\geq 0}$ | T | $d\tau^2 \equiv ds^2/c^2 \geq 0$（类时世界线） | 沿类时世界线的弧长参数 |
| 空间维数 | $D$ | $\mathbb{N}^+$ | [1] | $D = 3$（本宇宙 contingent 事实） | 宏观延展空间维度数；D=3 保证平方反比律、稳定 Kepler 轨道和 Huygens 原理 |
| 惯性参考系 | — | 概念 | — | 度规取 Minkowski 形式 $\eta_{\mu\nu}$ 且 Christoffel 符号 $\Gamma^\lambda_{\mu\nu}=0$ 的坐标系 | 无加速度、无引力的局域参考系；Newton 定律和狭义相对论成立的舞台 |

### R1.3 数学表达式

**局域惯性系中的 Minkowski 度规**（平直时空极限）：

$$ds^2 = c^2 dt^2 - (dx^1)^2 - (dx^2)^2 - (dx^3)^2$$

**一般坐标系中的弯曲时空**：

$$ds^2 = g_{\mu\nu}(x)\, dx^\mu dx^\nu$$

其中 $g_{\mu\nu}$ 为二阶对称协变张量，10 个独立分量。

**因果分类**：对两个不同事件 $A,B$，定义间隔 $\Delta s^2 \equiv g_{\mu\nu}\Delta x^\mu \Delta x^\nu$。按 $\Delta s^2$ 的符号分类：

| 条件 | 分类 | 物理含义 |
|------|------|---------|
| $\Delta s^2 = g_{\mu\nu}\Delta x^\mu \Delta x^\nu > 0$ | 类时 (timelike) | 存在惯性系中两事件同地先后发生；可因果连接 |
| $\Delta s^2 = 0$ | 类光 (lightlike/null) | 仅以光速信号可连接 |
| $\Delta s^2 < 0$ | 类空 (spacelike) | 任何惯性系中两事件均不同地；无因果联系 |

**局域性约束**：物理量 $\phi(x)$ 在点 $x$ 的值仅依赖于其在过去光锥 $J^-(x)$ 内的初始数据。

### R1.4 成立条件 (Scope)

- **有效场论范围**：R1 在能量远低于 Planck 尺度（$E \ll E_P \approx 1.22 \times 10^{19}$ GeV）、距离远大于 Planck 长度（$l \gg l_P$）的范围内精确成立。这是目前所有已确认物理实验的适用域。
- 狭义相对论：$g_{\mu\nu} \rightarrow \eta_{\mu\nu}$（平直极限，忽略引力）。
- 广义相对论：$g_{\mu\nu}$ 为动力学场，由 Einstein 场方程（$\leftarrow$ R1 + R2）决定。

### R1.5 失效边界 (Boundary)

- **Planck 尺度** $l_P = \sqrt{\hbar G/c^3} \approx 1.616 \times 10^{-35}$ m：时空本身的量子涨落不可忽略。连续流形假设可能破缺（量子引力候选：弦论、圈量子引力、因果动力学三角化）。注：$c$ 见 R1.2，$\hbar$ 见 R4.2，$G$ 为 Newton 引力常数（由 Einstein 场方程的 Newton 极限确定）。
- **Planck 时间** $t_P = l_P/c \approx 5.391 \times 10^{-44}$ s：此时间尺度以下，经典因果结构可能不再适用。
- **初始奇点**（大爆炸 $t \rightarrow 0$）：度规退化，广义相对论失效。

### R1.6 必要性 (Necessity)

若移除或弱化 R1 的任一部分：

| 移除/弱化 | 后果 |
|-----------|------|
| 3+1 维 → 其他维数 | 无稳定 Kepler 轨道 (D≠3)；无 Huygens 原理 (D even)；引力和静电力的平方反比律改变 |
| Lorentz 符号差 → Euclidean 符号差 | 无因果序；无波传播；量子场论无法定义 |
| 光速上限 $c$ → 无上限 | 因果悖论（封闭类时曲线）；无稳定物质结构 |
| 广义协变性 → 特殊坐标系 | 非惯性系物理定律形式改变；无法描述引力为时空几何 |
| 等效原理 $m_i=m_g$ → 破缺 | 引力无法几何化；Einstein 场方程无法导出；无法解释 Eötvös 实验零结果（$m_i/m_g$ 在 $10^{-15}$ 精度内为 1） |

### R1.7 充分性 (Sufficiency)

R1 的三个子原则各自提供：

**(1a+1b) 因果-相对论结构** 单独提供：
- 平直时空极限 → 狭义相对论全部运动学（Lorentz 变换、时间膨胀、长度收缩、同时性相对性）
- + R4（量子公设） → 相对论量子场论的因果结构（微观因果性 → 自旋-统计定理）

**(1c) 等效原理 + 广义协变性** 提供：
- + R2（最小作用量）→ 弯曲时空动力学（Einstein 场方程）→ 引力理论
- 度规 $g_{\mu\nu}$ 从固定背景升格为动力学场——这是通往广义相对论的独立入口，不由 1a/1b 蕴含

### R1.8 子组件与 R1-R6 映射

R1 的五个子组件逻辑关系：
- **(1a+1b)** — `kernel.lorentz_invariance`, `kernel.light_speed_invariance`（因果-相对论结构，彼此等价）
- **(1c)** — `kernel.equivalence_principle`, `kernel.general_covariance`（引力几何化路径，独立于 1a/1b）
- **contingent** — `kernel.spacetime_dimensionality`（D=3 为偶然事实）

| 子组件 | frameworks.yaml ID | 逻辑分组 |
|--------|-------------------|---------|
| 3+1 时空维度 | `kernel.spacetime_dimensionality` | contingent 事实 |
| 光速不变 | `kernel.light_speed_invariance` | 1a ⇔ 1b |
| Lorentz 不变性 + 因果结构 | `kernel.lorentz_invariance` | 1a ⇔ 1b |
| 等效原理（$m_i=m_g$） | `kernel.equivalence_principle` | 1c（独立公设） |
| 广义协变性 | `kernel.general_covariance` | 1c |

---

## R2. 最小作用量原理 (Principle of Stationary Action)

### R2.1 陈述

物理系统在两个给定构型之间的真实演化路径，是使作用量泛函取平稳值（极值或鞍点）的路径——由此自然得出决定性动力学（给定初始条件后演化唯一确定）。系统的全部动力学内容编码于拉格朗日量 $L$（或拉格朗日密度 $\mathcal{L}$），作用量取平稳值的条件是导出所有动力学方程的统一数学机制。

### R2.2 变量定义

| 变量 | 符号 | 类型 | 量纲 | 定义域 | 物理含义 |
|------|------|------|------|--------|---------|
| 作用量 | $S$ | $\mathbb{R}$ | M·L²·T⁻¹ | $S \in \mathbb{R}$ | 动力学泛函；Lorentz 不变量 |
| 拉格朗日量 | $L$ | $\mathbb{R}$ | M·L²·T⁻² | $L$ 为 $(q,\dot{q},t)$ 的函数 | 动能 − 势能；编码系统全部动力学 |
| 拉格朗日密度 | $\mathcal{L}$ | $\mathbb{R}$ | M·L⁻¹·T⁻² | $\mathcal{L}$ 为 $(\phi,\partial_\mu\phi,x^\mu)$ 的函数 | 场论中的基本标量密度 |
| 广义坐标 | $q_i$ | 依赖系统 | 依赖系统 | $i \in \{1,\ldots,N\}$，$N$ 为自由度 | 描述系统位形的独立变量 |
| 广义速度 | $\dot{q}_i \equiv dq_i/dt$ | 依赖系统 | 依赖系统 | 与 $q_i$ 对应 | $q_i$ 对时间的导数 |
| 场变量 | $\phi(x)$ | 依赖场类型 | 依赖场类型 | 标量 / 向量 / 旋量 | 场论中的基本动力学变量 |
| 初始时间 | $t_1, t_2$ | $\mathbb{R}$ | T | $t_1 < t_2$ | 作用量积分的起止时刻（固定端点） |
| 变分 | $\delta$ | 算符 | — | 作用于泛函 | 函数无穷小变化，固定端点 $\delta q(t_1)=\delta q(t_2)=0$ |

### R2.3 数学表达式

**作用量定义**（粒子力学）：

$$S[q_i] \equiv \int_{t_1}^{t_2} L\big(q_i(t), \dot{q}_i(t), t\big)\, dt$$

**作用量定义**（场论）：

$$S[\phi] \equiv \int \mathcal{L}\big(\phi(x), \partial_\mu\phi(x), x^\mu\big)\, d^4x$$

**平稳作用量条件**：

$$\delta S = 0$$

对路径的无穷小变分 $\delta q_i$（固定端点：$\delta q_i(t_1) = \delta q_i(t_2) = 0$），作用量的一阶变分为零。

### R2.4 成立条件 (Scope)

- **有效场论范围**：同 R1.4，R2 在 Planck 尺度以上成立。在 Planck 尺度以下，连续作用量 + 连续路径的假设可能失效。
- **固定端点变分**：$\delta q(t_1) = \delta q(t_2) = 0$。
- **拉格朗日量存在性**：系统必须可被一个标量函数 $L$ 或 $\mathcal{L}$ 完备描述。对于有耗散或非保守力的系统，需扩展框架（如 Rayleigh 耗散函数）。
- **$L$ 的形式不由 R2 确定**：R2 只规定变分框架（$\delta S = 0$），不固定 $L$ 的具体函数形式。$L$ 的形式由对称性原理（R1 的 Lorentz/Galilei 不变性 → 动能项 $\propto v^2$；R3 的规范不变性 → 最小耦合 $p \to p - qA$）和实验参数（质量 $m$、耦合常数 $g$ 等）共同约束。R2 是"空容器"——动力学内容由外部输入填入。
- **可微性**：$L$ 对 $q, \dot{q}, t$ 充分光滑（$L \in C^2$）。

### R2.5 失效边界 (Boundary)

| 失效条件 | 说明 |
|---------|------|
| 非势场力（耗散） | 摩擦力等不可由势函数导出的力，标准 $L = T - V$ 不适用；需扩展框架 |
| 非完整约束 | 不可积分的速度约束，变分原理需修正（如 d'Alembert 原理） |
| Planck 尺度量子引力 | 连续时空 + 连续路径假设可能失效；作用量可能需要离散化或全息表述 |
| 初始条件不确定 | 作用量原理只决定演化方程，不决定初始条件 |

### R2.6 必要性 (Necessity)

| 移除/弱化 | 后果 |
|-----------|------|
| 最小作用量 → Newton 运动方程 | 无法导出 Euler-Lagrange 方程 → 无法导出任何动力学方程 |
| 作用量 → Lagrangian 不存在 | Noether 定理失效 → 无守恒律（能量、动量、角动量、电荷） |
| 作用量 → 场论 Lagrangian | 无法导出 Maxwell 方程、Yang-Mills 方程、Einstein 场方程、Dirac 方程 |
| $\delta S = 0$ → 弱化为近似 | 动力学方程不再严格成立 |

**为什么必须是平稳值（不是最小值）**：在有些情况下（如类时测地线在某些 Lorentz 流形中），作用量取鞍点而非最小值。R2 以"平稳作用量"表述覆盖全部情况。

**为什么必须是作用量（不是其他泛函）**：仅作用量具有 Lorentz 不变性且量纲与 $\hbar$ 一致，使得量子力学的路径积分 $\int \mathcal{D}\phi\, e^{iS/\hbar}$ 在 $\hbar \to 0$ 时退化为经典极限 $\delta S = 0$。作用量是经典力学与量子力学之间的唯一桥梁量。

### R2.7 充分性 (Sufficiency)

R2 + R1（时空结构）提供：
- $\delta S = 0$ → Euler-Lagrange 方程（变分法的数学恒等式）
- + 具体 $L$ 的选择 → 全部动力学方程
- + 连续对称性 → Noether 定理 → 全部守恒律
- + 量子化手续 → Feynman 路径积分 → 量子场论

### R2.8 直接推论

| 推论 | 说明 |
|------|------|
| Euler-Lagrange 方程 | $\frac{d}{dt}\frac{\partial L}{\partial \dot{q}_i} - \frac{\partial L}{\partial q_i} = 0$ |
| Noether 定理 | 作用量的每个连续对称性对应一个守恒量 |
| 最小作用量 + 量子化 | 路径积分 $\int \mathcal{D}\phi\, e^{iS/\hbar}$ |

---

## R3. 局域规范不变性 (Local Gauge Invariance)

### R3.1 陈述

物质场的拉格朗日量在任意局域（位置依赖的）规范变换下保持不变。为维持这种不变性，必须引入补偿场——规范场 $A_\mu^a$。规范场与物质场的耦合自然产生基本相互作用力。规范群的结构完全决定了相互作用的形式。

### R3.2 变量定义

| 变量 | 符号 | 类型 | 量纲 | 定义域 | 物理含义 |
|------|------|------|------|--------|---------|
| 物质场 | $\psi(x)$ | 依赖表示 | 依赖场类型 | $x \in \mathcal{M}$ | 承载规范荷的物质场（标量/旋量） |
| 规范参数 | $\alpha^a(x)$ | $\mathbb{R}$（对 Abel 群） | [1] | $x \in \mathcal{M}$，任意光滑函数 | 局域规范变换的角度/参数 |
| 规范势 | $A_\mu^a(x)$ | $\mathbb{R}$（分量） | 依赖群表示 | $x \in \mathcal{M}$，$\mu \in \{0,1,2,3\}$ | 补偿场；传递相互作用的玻色子 |
| 场强张量 | $F_{\mu\nu}^a$ | $\mathbb{R}$（分量） | 依赖群表示 | 反对称：$F_{\mu\nu}^a = -F_{\nu\mu}^a$ | 规范场的物理自由度（电场 + 磁场） |
| 协变导数 | $D_\mu$ | 算符 | 依赖作用对象 | $\mu \in \{0,1,2,3\}$ | 在规范变换下协变地变换的导数 |
| 规范耦合常数 | $g$ | $\mathbb{R}^+$ | [1] | $g > 0$ | 物质场与规范场的耦合强度 |
| 规范群生成元 | $T^a$ | 矩阵 | [1] | $a \in \{1,\ldots,\dim(G)\}$ | Lie 代数的基础表示矩阵 |
| 结构常数 | $f^{abc}$ | $\mathbb{R}$ | [1] | $[T^a, T^b] = i f^{abc} T^c$ | 规范群的非 Abel 特性度量 |

### R3.3 数学表达式

> **⚠️ 群选择声明**：以下数学表达式以 **U(1) Abel 规范群**（电磁学）为例书写。Maxwell 方程组的完整推导 **必须** 选择 U(1) 群——这是本宇宙的 contingent 事实，不由 R3 的抽象结构唯一决定。非 Abel 群（SU(2), SU(3)）的推广形式在对应处注释。此声明贯穿全文：每一条具体物理定律的"从 R1-R6 推出"均隐含了对应规范群的具体选择（如 `contingent.sm_gauge_group`），这属于宇宙参数而非逻辑必然。

**局域规范变换**（以 U(1) Abel 群为例）：

$$\psi(x) \to e^{i\alpha(x)}\psi(x)$$

**协变导数**（最小耦合）：

$$D_\mu \equiv \partial_\mu - i g A_\mu(x)$$

要求 $D_\mu\psi$ 满足与 $\psi$ 相同的规范变换律：

$$D_\mu\psi \to e^{i\alpha(x)} D_\mu\psi$$

**规范场的变换律**：

$$A_\mu(x) \to A_\mu(x) + \frac{1}{g}\,\partial_\mu\alpha(x)$$

**场强张量定义**：

$$F_{\mu\nu} \equiv \partial_\mu A_\nu - \partial_\nu A_\mu$$

（对非 Abel 群：$F_{\mu\nu}^a \equiv \partial_\mu A_\nu^a - \partial_\nu A_\mu^a + g f^{abc} A_\mu^b A_\nu^c$）

**规范不变拉格朗日量**（纯规范场部分，SI 单位以 U(1) EM 为例）：

$$\mathcal{L}_{\text{gauge}} = -\frac{1}{4\mu_0} F_{\mu\nu} F^{\mu\nu}$$

系数 $1/\mu_0$（$\mu_0$ 为真空磁导率）由 Newton 极限下恢复 Coulomb 定律的实验要求确定，不由规范对称性本身决定。对于非 Abel 规范群（如 SU(2), SU(3)），对应的系数为 $1/g^2$（$g$ 为规范耦合常数）。

**耦合到物质场**（以 Dirac 场为例；为简洁使用自然单位 $\hbar=c=1$，恢复 SI 需 $i\gamma^\mu D_\mu \to i\hbar c\gamma^\mu D_\mu$, $m \to mc^2$, $g \to e/\hbar$，纯规范场部分见上文）：

$$\mathcal{L} = \bar{\psi}(i\gamma^\mu D_\mu - m)\psi - \frac{1}{4\mu_0}F_{\mu\nu}F^{\mu\nu}$$

### R3.4 规范场动力学的确定

R3 本身只强制规范场 $A_\mu^a$ 的**存在性**和**与物质的耦合形式**（最小耦合 $p \to p - gA$）。规范场的**动能项**（纯规范场 Lagrangian）需要额外原则确定：

- **Lorentz 不变性 (R1)** + **至多二阶导数**（有效场论）→ 唯一可能的数学形式是 $\mathcal{L}_{\text{gauge}} \propto F_{\mu\nu}^a F^{a\mu\nu}$（规范不变 + Lorentz 标量 + 二阶场方程）。比例系数（如电磁学中的 $1/4\mu_0$）由实验确定——规范对称性本身不固定耦合强度。
- 高阶导数项（如 $RF^2$ 等）在低能极限下被压低，可忽略。
- 在 4 维时空中，这是给出二阶场方程的唯一规范不变、Lorentz 不变的标量。

**注意**：R3 不指定规范群的具体选择（$U(1)$, $SU(2)$, $SU(3)$ 等）——那是 contingent 事实。R3 只规定：**若**存在规范对称性，则必然伴随着规范场和规范相互作用。

### R3.5 成立条件 (Scope)

- **可微规范变换**：$\alpha(x)$ 必须充分光滑。
- **规范群已指定**：规范群的具体选择（如 $U(1)$、$SU(2)$、$SU(3)$）是 contingent 事实。R3 只规定规范不变性的结构必然性，不决定哪个群在自然界实现。
- **可重整性**（微扰量子场论中）：规范对称性保证可重整性（'t Hooft 1971）。

### R3.6 失效边界 (Boundary)

| 失效条件 | 说明 |
|---------|------|
| 反常 (Anomaly) | 经典规范对称性在量子层面可被破坏（如 Adler-Bell-Jackiw 反常）；理论需满足反常消除条件才能自洽 |
| 极高能标（Planck 尺度） | 若量子引力修正改变规范相互作用的结构（如弦论中规范群由紧化决定），局域规范对称性可能 emergent 而非 fundamental |
| 强耦合区 | 微扰展开失效；需非微扰方法（格点规范理论、全息对偶） |
| Higgs 机制（自发对称破缺） | 规范对称性未被破坏——真空期望值破缺的是全局对称性部分，规范对称性本身保持完好。W/Z 玻色子获得质量是规范理论的成就，非失效。 |

### R3.7 必要性 (Necessity)

| 移除/弱化 | 后果 |
|-----------|------|
| $\alpha(x)$ 局域 → $\alpha$ 全局常数 | 无规范场 → 无光子、无电磁力；量子场论不可重整 |
| 规范不变性 → 显式破缺 | 非物理自由度不消除；概率不守恒 (Ward 恒等式破缺) |
| 规范群为 Abel 群（无非 Abel 自相互作用） | 规范场之间无直接耦合 → 无渐近自由 → 无 QCD 禁闭机制；弱力的 $W^\pm$/$Z$ 自相互作用缺失 → 弱力结构改变 |

### R3.8 充分性 (Sufficiency)

R3 + R1 + R2 提供：
- Maxwell 方程组（$U(1)$ 规范群 + 最小作用量原理）
- Yang-Mills 理论（非 Abel 规范群推广）
- 规范相互作用的普适形式（规范场与物质场的最小耦合）
- 自发对称破缺 + R3 → Higgs 机制 → 弱力玻色子质量生成

---

## R4. 量子力学公设 (Quantum Postulates)

### R4.1 陈述

量子系统的状态由复 Hilbert 空间 $\mathcal{H}$ 中的归一化向量 $|\psi\rangle$ 完备描述。量子力学包含四条相互关联的公设：

**(4a) 叠加原理** — 合法量子态的线性组合仍为合法量子态。

**(4b) 幺正演化** — 孤立系统的时间演化由幺正算符实现，保证概率守恒。

**(4c) 正则对易关系** — 经典共轭变量升格为满足对易关系的算符。这是量子与经典物理的结构分界线。

**(4d) 算符–可观测量对应** — 每个物理可观测量对应一个厄米（自伴）算符；测量结果必为其本征值之一。

### R4.2 变量定义

| 变量 | 符号 | 类型 | 量纲 | 定义域 | 物理含义 |
|------|------|------|------|--------|---------|
| 量子态 | $|\psi\rangle$ | $\mathcal{H}$ 中向量 | [1] | $\||\psi\rangle\| = 1$（归一化） | 系统全部物理信息的完备编码 |
| Hilbert 空间 | $\mathcal{H}$ | 复内积空间 | — | $\dim \mathcal{H} \geq 1$ | 量子态的可能取值空间 |
| 基态 | $|i\rangle$ | $\mathcal{H}$ 中向量 | [1] | $\langle i|j\rangle = \delta_{ij}$，完备性 $\sum_i |i\rangle\langle i| = I$ | Hilbert 空间的一组完备正交归一基向量 |
| 概率幅 | $\alpha_i \equiv \langle i|\psi\rangle$ | $\mathbb{C}$ | [1] | $\sum_i |\alpha_i|^2 = 1$ | 系统态在基态 $|i\rangle$ 上的投影分量 |
| 幺正演化算符 | $U(t_2, t_1)$ | $\mathcal{H} \to \mathcal{H}$，线性 | [1] | $U^\dagger U = UU^\dagger = I$ | 时间平移；保证概率守恒 |
| 哈密顿算符 | $\hat{H}$ | $\mathcal{H}$ 上厄米算符 | M·L²·T⁻² | $H^\dagger = H$ | 能量算符；时间演化的生成元 |
| 约化 Planck 常数 | $\hbar$ | 常数 | M·L²·T⁻¹ | $\hbar = h/2\pi = 1.054571817...\times 10^{-34}$ J·s (exact) | 量子作用量单元；量子–经典分界线 |
| 位置算符 | $\hat{x}$ | $\mathcal{H}$ 上厄米算符 | L | $\hat{x}^\dagger = \hat{x}$ | 位置可观测量的算符表示 |
| 动量算符 | $\hat{p}$ | $\mathcal{H}$ 上厄米算符 | M·L·T⁻¹ | $\hat{p}^\dagger = \hat{p}$ | 动量可观测量的算符表示 |
| 对易子 | $[A,B] \equiv AB - BA$ | $\mathcal{H}$ 上算符 | 依赖 $A,B$ | — | 衡量两个算符是否可同时对角化 |
| 可观测量算符 | $\hat{O}$ | $\mathcal{H}$ 上厄米算符 | 依赖物理量 | $\hat{O}^\dagger = \hat{O}$ | 物理可观测量的数学表示 |
| 本征值 | $o_i$ | $\mathbb{R}$（厄米算符） | 依赖 $\hat{O}$ | $\hat{O}|o_i\rangle = o_i|o_i\rangle$ | 可能测量结果的值 |
| 本征态 | $|o_i\rangle$ | $\mathcal{H}$ 中向量 | [1] | $\hat{O}|o_i\rangle = o_i|o_i\rangle$ | 测量得到确定值 $o_i$ 的态 |

### R4.3 数学表达式

**(4a) 叠加原理**：

$$|\psi\rangle = \sum_{i} \alpha_i |i\rangle, \quad \sum_i |\alpha_i|^2 = 1$$

其中 $\{|i\rangle\}$ 为 $\mathcal{H}$ 的一组完备正交归一基：$\langle i|j\rangle = \delta_{ij}$。

**(4b) 幺正演化**：

$$|\psi(t)\rangle = U(t, t_0) |\psi(t_0)\rangle, \quad U^\dagger U = I$$

时间平移生成元为 $\hat{H}$：

$$U(t, t_0) = \exp\!\left(-\frac{i}{\hbar} \hat{H} (t - t_0)\right)$$

微分形式（Schrödinger 绘景的演化方程）：

$$i\hbar \frac{d}{dt}|\psi(t)\rangle = \hat{H} |\psi(t)\rangle$$

注意：此处 $i\hbar\, d|\psi\rangle/dt = H|\psi\rangle$ 是抽象的 Hilbert 空间中的演化方程（R4 公设的直接推论），NOT 坐标表示中的 Schrödinger 偏微分方程（$\leftarrow$ law.schroedinger_equation）。

**(4c) 正则对易关系**：

$$[\hat{x}_i, \hat{p}_j] = i\hbar\,\delta_{ij}$$

推广到任意一对经典共轭变量 $(q, p)$：

$$[\hat{q}, \hat{p}] = i\hbar$$

坐标表示中动量算符的作用：

$$\hat{p} \equiv -i\hbar\nabla, \quad \hat{p}_i \equiv -i\hbar\frac{\partial}{\partial x_i}$$

**(4d) 算符–可观测量对应**：

$$\hat{O}|o_i\rangle = o_i|o_i\rangle, \quad o_i \in \mathbb{R}$$

$\hat{O}$ 的本征态 $\{|o_i\rangle\}$ 构成 $\mathcal{H}$ 的完备正交归一基。

**注**：R4d 仅声明"测量结果 = 本征值"。测量后系统态是否坍缩到对应本征态（投影公设），属于量子力学诠释层面（哥本哈根 / 多世界 / 退相干），不是 R4 的一部分。R4+R5 构成**最小统计诠释**——对任意量子测量问题给出完备的概率预言，而不承诺坍缩本体论。

### R4.4 成立条件 (Scope)

- **量子区 (quantum_regime)**：当作用量 $\sim \hbar$ 时量子效应显著。宏观极限 $\hbar \to 0$ 恢复经典力学。
- **孤立系统 (isolated_system)**：R4b（幺正演化）仅适用于未进行测量的孤立系统。测量时发生 R5（Born 规则）描述的坍缩。
- **连续谱**：对位置、动量等连续谱算符，求和 $\to$ 积分，$\delta_{ij} \to \delta(x-x')$。
- **注**：R4a–R4d 的公设形式是框架无关的（不预设相对论或非相对论）。非相对论极限仅在将 $\hat{H}$ 具体化为 $-\hbar^2\nabla^2/(2m) + V$ 时需要，这已属于 law.schroedinger_equation 的推导（$\leftarrow$ R4b + R4c）。

### R4.5 失效边界 (Boundary)

| 失效条件 | 说明 |
|---------|------|
| 测量过程 | 幺正演化（R4b）在测量时中断；R5 接管。测量问题的本体论（哥本哈根坍缩 vs. 多世界退相干）不在 R1–R6 范围内 |
| Planck 尺度量子引力 | 时间是否为参数（非算符）可能不再成立（Pauli 定理只适用于标准 QM）；可能需修改对易关系（广义不确定性原理） |
| 开放量子系统 | 非幺正演化需量子主方程（Lindblad 方程）；R4b 仅适用于孤立系统 |

### R4.6 必要性 (Necessity)

| 移除/弱化 | 后果 |
|-----------|------|
| 无叠加原理 | 无干涉、无纠缠、无量子计算 → 退化为经典概率论 |
| 无幺正演化 | 概率不守恒；无稳定量子态；能量不守恒 |
| 无正则对易关系 | 无不确定性原理；无零点能；无离散能谱；无稳定原子（电子会螺旋坠入核） |
| 正则对易关系 $\to [\hat{x},\hat{p}] = 0$ | 位置和动量可同时精确确定 → 不确定性原理消失 → 退化为经典力学（无离散能谱、无零点能、无隧穿） |
| 无可观测量–算符对应 | 无法从态向量提取物理预言 |

### R4.7 充分性 (Sufficiency)

R4 + R1（时空结构）提供：
- 所有单粒子量子力学（Schrödinger 方程、能级量子化、隧穿效应）
- + R2（最小作用量） → 路径积分量子化
- + R1 + 相对论性推广 → 量子场论（Klein-Gordon、Dirac、Yang-Mills 量子化）
- 自旋–统计定理（R4 + R1 → Pauli 不相容原理）

### R4.8 四条公设的独立性论证 (Independence of the Four Postulates)

R4 的四条公设 (4a–4d) 是逻辑上相互独立的——没有任何一条可以从其他三条推出。以下逐条论证。

**4a（叠加原理）的独立性**：

| 情形 | 说明 |
|------|------|
| 保留 4b–4d，移除 4a | 无法定义 Hilbert 空间结构 → 4b–4d 失去数学载体。4a 是其余三条的作用域 |
| 保留 4a，移除 4b–4d | 4a 仅定义"线性组合合法"，不涉及演化、代数结构或测量——不能推出任何实验预言 |
| 反例 | 经典统计力学中，相空间上的概率分布满足 Kolmogorov 公理（线性组合仍是合法分布，类比 4a 的结构），但不满足幺正演化（4b）、正则对易（4c）或算符–可观测量对应（4d） |

**4b（幺正演化）的独立性**：

| 情形 | 说明 |
|------|------|
| 保留 4a+4c+4d，移除 4b | 态空间、算符代数、可观测量对应均在，但态如何随时间变化无定义 → 无动力学。可以定义瞬时测量理论（做一次测量 → 结束），但无法描述含时过程 |
| 为何 4c 推不出 4b | 4c 定义了 $[\hat{x},\hat{p}]=i\hbar$，但不规定态如何演化。可将 4c 与随机演化（非幺正，如主方程）结合——不会推出幺正性 |
| 为何 4d 推不出 4b | 4d 关联可观测量与厄米算符，但不涉及时间演化。静态测量理论不需要 4b |
| Stone 定理的局限 | Stone 定理（强连续单参数酉群的生成元必为自伴算符）需要"演化是酉的"作为前提——**这一定理需要 4b 才成立**，不能反过来从其他公设推出 4b |

**4c（正则对易关系）的独立性**：

| 情形 | 说明 |
|------|------|
| 保留 4a+4b+4d，移除 4c | Hilbert 空间上有幺正演化和可观测量对应，但算符之间的代数关系未固定。若 $[\hat{x},\hat{p}]=0$（经典对易），量子力学退化为 Liouville 方程描述的经典统计力学——仍满足 4a+4b+4d（厄米算符仍对应可观测量，只是对易），但无不确定性原理、无离散能谱、无零点能 |
| 注：4c 是否可从 R1 + 4a 推出？ | 在非相对论量子力学中，Galilei 群的投影表示可导出 $[\hat{x},\hat{p}]=i\hbar$（Bargmann 1954；$\hbar$ 为群中心扩张参数）。但此推导 (a) 需要 R1 的时空对称性作为额外前提，(b) $\hbar$ 的数值仍需实验确定，(c) 在相对论推广中需改用 Poincaré 群。因此将 4c 作为独立公设是保守且正确的：它避免了用特定时空群的表示论替代一个明确的物理原理 |

**4d（算符–可观测量对应）的独立性**：

| 情形 | 说明 |
|------|------|
| 保留 4a+4b+4c，移除 4d | Hilbert 空间上有幺正演化和对易关系，但不规定哪些算符对应物理可观测量，也不规定测量结果如何从算符提取。可构造一个满足 4a–4c 但可观测量不由厄米算符本征值决定的自洽理论（如隐藏变量理论） |
| Gleason 定理的局限 | Gleason 定理（1957）论证概率测度必然形如 $P = \langle\psi|\hat{P}|\psi\rangle$——但此定理依赖 R5（Born 规则）的"概率"概念，不在 4a–4c 范围内。4a–4c 本身不能推出"概率 = 本征态投影模方" |
| 反例 | de Broglie–Bohm 理论保留了 4a+4b+4c（波函数服从 Schrödinger 方程，$[\hat{x},\hat{p}]=i\hbar$ 成立），但否认 4d：粒子有确定轨迹，可观测量不由厄米算符的本征值定义。该理论在经验上与标准量子力学等价，证明 4d 不是 4a–4c 的逻辑推论 |

**独立性矩阵**：

|  | 4a | 4b | 4c | 4d |
|--|:--:|:--:|:--:|:--:|
| **依赖 4a** | — | ✓ | ✓ | ✓ |
| **依赖 4b** | ✗ | — | ✗ | ✗ |
| **依赖 4c** | ✗ | ✗ | — | ✗ |
| **依赖 4d** | ✗ | ✗ | ✗ | — |

- ✓ = 该条公设的定义依赖另一条（失去另一条则该条无法陈述）
- ✗ = 逻辑独立，可独立陈述和变体

**结论**：R4a–R4d 四条公设逻辑独立。移除任何一条，其余三条均不能推出完整量子力学框架。四条不可再合并或约化。

---

## R5. Born 概率规则 (Born's Probability Rule)

### R5.1 陈述

对量子系统测量可观测量 $\hat{A}$ 时，得到本征值 $a_i$ 的概率等于系统态 $|\psi\rangle$ 在对应本征态 $|a_i\rangle$ 上投影的模方。此规则将 R4 的确定性幺正演化与实验观测的随机结果连接起来。

### R5.2 变量定义

| 变量 | 符号 | 类型 | 量纲 | 定义域 | 物理含义 |
|------|------|------|------|--------|---------|
| 测量前系统态 | $|\psi\rangle$ | $\mathcal{H}$ 中向量 | [1] | $\||\psi\rangle\|=1$ | 测量发生前系统的量子态 |
| 被测可观测量 | $\hat{A}$ | $\mathcal{H}$ 上厄米算符 | 依赖 $A$ | $\hat{A}^\dagger = \hat{A}$ | 实验装置测量的物理量算符 |
| 本征态 | $|a_i\rangle$ | $\mathcal{H}$ 中向量 | [1] | $\hat{A}|a_i\rangle = a_i|a_i\rangle$ | 可观测量 $\hat{A}$ 的确定值态 |
| 本征值 | $a_i$ | $\mathbb{R}$ | 依赖 $\hat{A}$ | $\hat{A}|a_i\rangle = a_i|a_i\rangle$ | 测量可能得到的结果值 |
| 概率幅 | $\langle a_i|\psi\rangle$ | $\mathbb{C}$ | [1] | — | 系统态在本征态上的投影 |
| 概率 | $P(a_i)$ | $\mathbb{R}_{[0,1]}$ | [1] | $\sum_i P(a_i) = 1$ | 得到结果 $a_i$ 的概率 |
| 简并度 | $g_i$ | $\mathbb{N}^+$ | [1] | 对应本征值 $a_i$ 的线性独立本征态数 | 同一本征值对应的 Hilbert 子空间维数 |

### R5.3 数学表达式

**离散谱**（本征值非简并）：

$$P(a_i) = |\langle a_i | \psi \rangle|^2$$

**离散谱**（本征值 $g_i$ 重简并）：

$$P(a_i) = \sum_{k=1}^{g_i} |\langle a_i^{(k)} | \psi \rangle|^2$$

其中 $|a_i^{(k)}\rangle$ 为简并子空间的标准正交基。

**连续谱**（例如位置 $x$）：

$$dP(x) = |\psi(x)|^2\, dx, \quad \psi(x) \equiv \langle x | \psi \rangle$$

**归一化条件**（概率完备性）：

$$\sum_i P(a_i) = 1 \quad \text{或} \quad \int dP(x) = 1$$

**期望值**：

$$\langle \hat{A} \rangle_\psi \equiv \langle\psi|\hat{A}|\psi\rangle = \sum_i a_i\, P(a_i)$$

### R5.4 成立条件 (Scope)

- **量子区 (quantum_regime)**：R5 适用于量子测量语境。
- **测量完成**：R5 描述测量后的结果统计，不描述"如何进行测量"或"坍缩何时发生"的本体论。
- **理想测量**：假设测量装置完美区分 $\hat{A}$ 的本征值。实际测量中的有限分辨率、效率等需额外建模。

### R5.5 失效边界 (Boundary)

| 失效条件 | 说明 |
|---------|------|
| 弱测量 (Weak measurement) | 不坍缩波函数的弱耦合测量，结果由弱值（weak value）描述而非 Born 规则 |
| 测量问题本体论 | R5 不解释为什么得到的是"这个结果而非那个"。多世界、退相干、客观坍缩等诠释给出不同本体论说明，但不改变 $P = |\langle a_i|\psi\rangle|^2$ 作为有效计算规则的地位 |
| 连续测量 | Zeno 效应 / 反 Zeno 效应需含时测量理论 |

### R5.6 必要性 (Necessity)

| 移除/弱化 | 后果 |
|-----------|------|
| 概率 ≠ 模方 | 无干涉项 → 双缝实验的干涉图样消失 |
| 复概率幅 → 实概率直接相加 | 退化为经典概率论；无量子干涉、无纠缠、无量子计算加速 |
| 无 Born 规则 | R4 的幺正演化只给出确定性的 $|\psi(t)\rangle$，无法连接到实验观测值 → 量子力学失去预言能力 |

**为什么必须是模方（不是模、不是四次方）**：
- 模方保证概率非负：$P \geq 0$。
- 模方保证总概率守恒（从幺正演化 $U^\dagger U = I$ + Born 规则）：$\sum_i |\langle a_i|U|\psi\rangle|^2 = \langle\psi|U^\dagger U|\psi\rangle = 1$。
- Gleason 定理（1957）：在 $\dim \mathcal{H} \geq 3$ 的 Hilbert 空间中，任何满足可加性的概率测度必然形如 $P = \langle\psi|\hat{P}|\psi\rangle$，Born 规则是唯一解。
- 实验：Born 规则经受了所有精度级别的检验，无一例外。

### R5.7 充分性 (Sufficiency)

R5 + R4（量子公设）提供：
- 全部量子力学的实验预言（谱线强度、散射截面、衰变率）
- 测量结果的统计分布（期望值、方差、高阶矩）
- 量子态层析（quantum state tomography）的理论基础

---

## R6. 统计力学基础 (Statistical Mechanics Foundations)

### R6.1 陈述

R6 由**两个互相独立但协同工作的公设**组成：

**(6a) Boltzmann 熵公式**：宏观系统的熵正比于系统在给定宏观约束（总能量 $E$、体积 $V$、粒子数 $N$ 等）下可及的微观状态总数的对数。在量子语境下，微观状态由 R4 的量子态结构确定；在经典极限（$\hbar \to 0$）下，微观状态计数退化为相空间体积元 $d^{3N}x\,d^{3N}p / h^{3N}$ 的计数。Boltzmann 常数 $k_B$ 提供了熵（无量纲统计量）与热力学熵（量纲 M·L²·T⁻²·Θ⁻¹）的单位转换。

**(6b) 等概率先验假设 (Fundamental Postulate of Statistical Mechanics)**：孤立系统在平衡态时，所有可及的量子微观状态以相等概率出现——$P_i = 1/W$ 对所有能量在 $[E, E+\delta E]$ 内的微观态 $|i\rangle$ 成立。这是统计力学的**唯一基本假设**——(6a) 定义 $S$ 与 $W$ 的关系，但要将 $W$ 与物理概率联系起来并推出热力学第二定律，必须追加此假设。

**6a 与 6b 的独立性**：$S = k_B \ln W$ 单独不蕴含等概率——熵的统计定义是组合计数工具，不规定各微观态的概率权重。反过来，等概率本身不定义熵——它只是概率分配规则。两者结合 ⇒ 热力学第二定律（$\Delta S \geq 0$ 是系统自发趋向最概然宏观态的统计推论）+ 宇宙低熵初始条件（contingent 事实，见 boundaries.md E4）。

### R6.2 变量定义

| 变量 | 符号 | 类型 | 量纲 | 定义域 | 物理含义 |
|------|------|------|------|--------|---------|
| 熵 | $S$ | $\mathbb{R}_{\geq 0}$ | M·L²·T⁻²·Θ⁻¹ | $S \geq 0$ | 系统无序度的定量量度；状态函数 |
| Boltzmann 常数 | $k_B$ | 常数 | M·L²·T⁻²·Θ⁻¹ | $k_B = 1.380649 \times 10^{-23}$ J/K (exact) | 能量–温度转换的普适标度；SI 定义常数 |
| 微观状态数 | $W$ | $\mathbb{N}^+$ | [1] | $W \geq 1$ | 给定宏观约束下系统可及的量子微观状态总数 |
| 热力学温度 | $T$ | $\mathbb{R}_{\geq 0}$ | Θ | $T \geq 0$（除特殊自旋系统外） | 由 $1/T \equiv \partial S/\partial E$ 定义 |
| 系统内能 | $E$ 或 $U$ | $\mathbb{R}$ | M·L²·T⁻² | 由宏观约束确定 | 系统总能量（不含整体动能/势能） |
| 体积 | $V$ | $\mathbb{R}_{>0}$ | L³ | $V > 0$ | 系统占据的空间体积 |
| 粒子数 | $N$ | $\mathbb{N}$ | [1] | $N \geq 0$ | 系统包含的微观粒子总数 |
| 化学势 | $\mu$ | $\mathbb{R}$ | M·L²·T⁻² | — | 增加一个粒子所需能量；由 $\mu \equiv -T(\partial S/\partial N)_{E,V}$ 定义 |
| 微观态能量 | $E_i$ | $\mathbb{R}$ | M·L²·T⁻² | $\hat{H}|i\rangle = E_i|i\rangle$ | 系统第 $i$ 个量子微观态的能量本征值 |

### R6.3 数学表达式

**Boltzmann 熵公式**：

$$S(E, V, N) = k_B \ln W(E, V, N)$$

其中 $W(E, V, N)$ 为系统在总能量 $E$、体积 $V$、粒子数 $N$ 约束下的量子微观状态数。

**能量壳层计数**（微正则系综）：

$$W(E, V, N) \equiv \#\{ \text{微观态 } |i\rangle : E_i \in [E, E+\delta E] \}$$

**温度的定义**（由 $S = k_B \ln W$ 自然导出）：

$$\frac{1}{T} \equiv \left(\frac{\partial S}{\partial E}\right)_{V, N}$$

Entropy 是状态函数，$dS$ 是全微分。

**热力学第二定律**（统计形式）：

$$\Delta S_{\text{total}} \geq 0 \quad \text{（孤立系统自发过程）}$$

等号仅在可逆过程中成立。

**Boltzmann 分布**（正则系综，系统与温度为 $T$ 的热库接触）：

$$P_i = \frac{e^{-E_i/k_B T}}{Z}, \quad Z \equiv \sum_i e^{-E_i/k_B T}$$

这是公设 6a（$S = k_B \ln W$）+ 公设 6b（等概率先验）+ 能量约束在最概然分布下的直接推论。

### R6.4 公设 6b 详解：等概率先验

> 本条公设已在 R6.1 中与 (6a) 并列声明。此处提供其数学表述、推论的完整链和边界。

**等概率先验假设 (Fundamental Postulate of Statistical Mechanics)**：
孤立系统在平衡态时，所有可及的量子微观状态以相等概率出现。
即：$P_i = 1/W$ 对所有能量在 $[E, E+\delta E]$ 内的微观态 $|i\rangle$ 成立。

这是统计力学的唯一基本假设——所有其他结论（正则分布、巨正则分布、涨落-耗散定理等）都从此假设 + R4（量子态结构）+ R6（$S = k_B \ln W$）推出。

**等价表述**：
- 微正则系综：$P_i = 1/W$（等概率）
- 正则系综：$P_i = e^{-\beta E_i}/Z$（从微正则 + 热库耦合推出，非假设）
- 巨正则系综：从微正则 + 粒子库耦合推出

### R6.5 成立条件 (Scope)

- **宏观极限 (macroscopic_limit)**：$N \gg 1$（通常 $N \sim 10^{23}$）。统计涨落 $\sim 1/\sqrt{N}$ 可忽略。
- **热平衡 (thermal_equilibrium)**：$T$ 是全局定义的状态变量，仅在系统处于热平衡或局部热平衡时有明确定义。
- **遍历性条件**：等概率假设仅在系统能够遍历所有可及微观态时严格成立。对于非遍历系统（如玻璃态、自旋玻璃），需修正。

### R6.6 失效边界 (Boundary)

| 失效条件 | 说明 |
|---------|------|
| 小系统（$N \sim 1\text{–}100$） | 统计涨落显著；系综不等价；需微正则/正则的精确处理而非热力学极限 |
| 非平衡过程 | $T$ 无统一定义；需非平衡统计力学（Boltzmann 方程、线性响应、涨落耗散定理） |
| 引力系统 | 自引力系统的热容为负（向热平衡演化时温度反而升高 $\to$ 引力热灾变）；系综不等价；熵的广延性破缺 |
| 量子纠缠熵 | 对于量子系统的子系统，von Neumann 熵 $S_{\text{vN}} = -\text{Tr}(\rho \ln \rho)$ 替代 Boltzmann 熵；在热力学极限下两者等价 |
| 黑洞 | Bekenstein-Hawking 熵 $S_{\text{BH}} = k_B c^3 A/(4G\hbar)$ ——熵正比于视界面积而非体积（全息原理）；R6 的 $S \propto \ln W$ 在此失效或需修改。（$c$ 见 R1，$\hbar$ 见 R4，$G$ 为引力常数） |

### R6.7 必要性 (Necessity)

| 移除/弱化 | 后果 |
|-----------|------|
| 无 $S = k_B \ln W$ | 无微观–宏观桥梁 → 无法从量子力学导出热力学；第二定律仅为经验规律 |
| 无熵增 | 无时间箭头；无热机效率限制；无生命过程的方向性 |
| 无温度定义（$1/T \equiv \partial S/\partial E$） | 温度退化为经验标度（如理想气体温度计）；无法与其他物理量纲关联 |
| 无 $k_B$ | 熵和温度的量纲独立；$k_B T$ 的能量尺度消失 → 量子统计（Bose-Einstein / Fermi-Dirac 分布）失去标度 |

### R6.8 充分性 (Sufficiency)

R6 + R4（量子微观态）提供：
- 热力学全部定律（第零、第一、第二、第三定律）
- 理想气体状态方程 $PV = Nk_B T$
- 量子统计分布（Fermi-Dirac + Bose-Einstein）→ 金属电子论、黑体辐射、BEC
- 化学平衡条件（$\mu_A = \mu_B$）
- 相变理论（Landau 理论及其统计力学基础）

---

## 派生定理

以下两条重要定理是 R1–R6 的数学推论，因其在物理学中的基础地位在此列出：

| 定理 | 从何推出 | 核心内容 |
|------|---------|---------|
| **Noether 定理** | R2（最小作用量） | 作用量的每个连续对称性对应一个守恒量。时间平移 $\to$ 能量守恒；空间平移 $\to$ 动量守恒；旋转 $\to$ 角动量守恒；规范对称 $\to$ 电荷守恒 |
| **自旋–统计定理** | R1 + R4 | 在相对论量子场论中，整数自旋粒子服从 Bose-Einstein 统计（波函数对称），半整数自旋粒子服从 Fermi-Dirac 统计（波函数反对称 $\to$ Pauli 不相容原理） |

**注意**：Noether 定理和自旋–统计定理是 R1–R6 的数学推导产物，不列为独立规则（R7/R8）。它们已归入 `effective_laws.yaml` 的 `law.noether_theorem` 和 `law.pauli_exclusion`（自旋–统计定理的推论）。

---

## R1–R6 之间的依赖关系

```
R1 (Causal Spacetime)
 ├─→ 定义因果结构、度规、光速上限
 ├─→ R2 (Least Action) 的舞台：作用量积分在 R1 定义的流形上进行
 ├─→ R3 (Gauge Invariance) 的舞台：规范变换定义于 R1 的时空点上
 ├─→ R4 (Quantum) 在 R1 定义的时空中演化
 │    └─→ R4 + R1 → 微观因果性 → 自旋–统计定理
 ├─→ R3 + R2 + R1 → 全部相互作用力（Maxwell, Yang-Mills, GR）
 └─→ R6 (Entropy) 的微观状态计数基于 R4 的量子态结构

R2 (Least Action)
 ├─→ Euler-Lagrange 方程 → 全部动力学方程
 ├─→ Noether 定理 → 全部守恒律（依赖 R1 定义对称性）
 └─→ + R1 → Einstein-Hilbert 作用量 → Einstein 场方程

R3 (Gauge Invariance)
 └─→ + R2 + R1 → 规范场动力学 → 全部基本力

R4 (Quantum)
 ├─→ + R1 → 量子场论（Klein-Gordon, Dirac, Yang-Mills）
 ├─→ + R5 (Born) → 实验预言的提取
 └─→ + R6 (Entropy) → 量子统计力学

R5 (Born Rule)
 └─→ 连接 R4 的数学结构与实验数据

R6 (Entropy)
 ├─→ + R4 → 从微观态计数导出全部热力学
 └─→ + R2（Noether → 能量守恒）→ 热力学第一定律
```

---

## 定理推导清单

以下 30 条定理 / 有效定律 / 推论均从 R1–R6（加上 contingent 事实）严格推出。
`[N]` = 必要性条件；`[S]` = 充分条件。括号中的 G1–G8 为推导分组。

| # | ID | 定律名 | 主要前提 |
|---|-----|--------|---------|
| 1 | law.euler_lagrange | Euler-Lagrange 方程 | R2 |
| 2 | law.noether_theorem | Noether 定理 | R2, R1 |
| 3 | law.energy_conservation | 能量守恒 | Noether |
| 4 | law.momentum_conservation | 动量守恒 | Noether |
| 5 | law.angular_momentum_conservation | 角动量守恒 | Noether |
| 6 | law.charge_conservation | 电荷守恒 | Noether, R3 |
| 7 | law.newton_first | Newton 第一定律 | R2, R1 |
| 8 | law.newton_second | Newton 第二定律 | R2, Euler-Lagrange, R1 |
| 9 | law.newton_third | Newton 第三定律 | Noether, R1 |
| 10 | law.gauss_electric | Gauss 电定律 | R3, R2, R1 |
| 11 | law.gauss_magnetic | Gauss 磁定律 | R3, R1 |
| 12 | law.faraday_induction | Faraday 感应定律 | R3, R1 |
| 13 | law.ampere_maxwell | Ampère-Maxwell 定律 | R3, R2, R1 |
| 14 | law.lorentz_force | Lorentz 力定律 | R3, R1 |
| 15 | law.em_wave_equation | 电磁波方程 | Gauss+Faraday+Ampere |
| 16 | law.schroedinger_equation | Schrödinger 方程 | R4b, R4c, R1 |
| 17 | law.energy_frequency | Planck-Einstein 关系 $E=h\nu$ | R4c |
| 18 | law.de_broglie_wavelength | de Broglie 波长 $\lambda = h/p$ | energy_frequency |
| 19 | law.uncertainty_principle | 不确定性原理 | R4c, R5, R4d, R1 |
| 20 | law.lorentz_transform | Lorentz 变换 | R1 |
| 21 | law.mass_energy | 质能等价 $E=mc^2$ | R1 |
| 22 | law.einstein_field | Einstein 场方程 | R1, R2 |
| 23 | law.newton_gravitation | Newton 万有引力 | Einstein 场方程（弱场极限） |
| 24 | law.zeroth_law | 热力学第零定律 | R6 |
| 25 | law.first_law_thermo | 热力学第一定律 | 能量守恒 + R6 |
| 26 | law.third_law_thermo | 热力学第三定律 | R6, R4a |
| 27 | law.ideal_gas | 理想气体状态方程 | R6, 热力学第一定律 |
| 28 | cor.kepler_third | Kepler 第三定律 | Newton 第二 + 万有引力 |
| 29 | cor.fermi_dirac | Fermi-Dirac 分布 | law.pauli_exclusion, R6 |
| 30 | cor.bose_einstein | Bose-Einstein 分布 | kernel.superposition_principle, R6 |

---

## 迭代记录

| Round | 日期 | 变更 |
|-------|------|------|
| 1 | 2026-05-12 | 初始精炼：每条规则增加变量表、失效边界、必要性、充分性；追加符号约定、依赖关系图、推导清单 |
| 2 | 2026-05-12 | 推导 G1-G3（Euler-Lagrange、Noether + 守恒律、Newton 三定律）→ 创建 rigorous_derivations.yaml |
| 3 | 2026-05-12 | 推导 G4-G8（Maxwell、量子力学、相对论、热力学、推论）→ 30 条推导完整；结构审计修复 |
| 4 | 2026-05-12 | R1-R6 精炼：修正 scope 矛盾、R3.6 错误条目、R4.4/R4.2/R6.1/R6.6；推导清单修正标签 |
| 5 | 2026-05-12 | 数学精度：决定性动力学、因果链细化、间隔定义分离、最小统计诠释注释 |
| 6 | 2026-05-12 | 严重数学错误：R3.3 缺 1/μ₀；度规升降 F^{i0} 符号错误（(−)(−)=+） |
| 7 | 2026-05-12 | Dirac Lagrangian 单位混合修复；ℏ,c 恢复规则注释 |
| 8 | 2026-05-12 | Levi-Civita 指标 F^{ji}=ε_{ijk} 修正；新增跨规则常数表；R1.1 D=3 contingent 标注 |
| 9 | 2026-05-12 | R1.1 重构：(1a) 最大速度 ⇔ (1b) 因果结构，明确等价性并附证明 |
| 10 | 2026-05-14 | R4.8 新增：四条量子公设 (4a–4d) 独立性论证——逻辑独立矩阵、反例与 Stone/Bargmann/Gleason 定理的局限 |
| 11 | 2026-05-16 | R1-R6 充分必要性审计 Round 1-2：R1 重构为三独立子原则、R3.3 U(1) 声明、R6 双公设、kernel 层清理、L-form 来源、½mv² 对称性论证、热力学极限桥接 |
| 12 | 2026-05-16 | Round 3：新增 deriv.pauli_exclusion 推导草图 + caveat (自旋-统计定理)；R1.2 合并空间维数/时间维数变量行 |
