# 第一层：基本公理

> 不可推导。现代物理学的逻辑起点。所有有效定律从此推出。

---

## 1. 最小作用量原理

$$\delta S = \delta\int L\,dt = 0$$

**地位**：全部动力学的生成器。给定 Lagrangian $L$，变分得运动方程。

**子要素**：
- 作用量 $S$ 的定义
- Lagrangian $L=T-U$（经典力学）或推广形式
- 变分法 → Euler-Lagrange 方程
- 作用量是 Lorentz 不变量

**来源**：Hamilton (1834-35); [FEYN II] Ch.19; [LAND] §2; [GOLD] Ch.2

---

## 2. 对称性与规范不变性

**Noether 定理**：每个连续对称性对应一个守恒流。

若作用量在变换 $q_i\to q_i+\epsilon Q_i$ 下不变（$\delta L = dF/dt$），则

$$Q = \sum_i \frac{\partial L}{\partial \dot{q}_i}Q_i - F$$

是守恒量：$dQ/dt=0$。

| 对称性 | 守恒量 |
|--------|--------|
| 时间平移不变 | 能量 |
| 空间平移不变 | 动量 |
| 空间旋转不变 | 角动量 |
| 规范不变性 | 电荷 |

**规范对称性决定相互作用**：
- $U(1)$ → 电磁力（光子）
- $SU(2)$ → 弱力（W⁺, W⁻, Z⁰）
- $SU(3)$ → 强力（胶子）

**来源**：[NOETHER]; [GOLD] §12.7; [GROSS]; [WEINBERG]

---

## 3. 量子力学公设

**3.1 态叠加原理**
$$|\psi\rangle = \alpha|\psi_1\rangle + \beta|\psi_2\rangle$$
系统态由 Hilbert 空间复矢量描述。合法态的线性组合仍是合法态。

**3.2 算符-观测对应**
物理可观测量对应厄米算符。测量结果为算符的本征值。

**3.3 幺正演化**
$$i\hbar\frac{\partial}{\partial t}|\psi\rangle = \hat{H}|\psi\rangle$$
孤立系统态演化是幺正的。薛定谔方程 = 此公设 + 能量算符 $\hat{H}$。

**3.4 正则对易关系**
$$[x,p]=i\hbar$$
量子与经典的核心分界线。不确定性原理 $\sigma_x\sigma_p \geq \hbar/2$ 是直接推论。

**来源**：Dirac (1930); [FEYN III]; [HEISENBERG]

---

## 4. 相对论原理

**4.1 光速不变**
$c = 2.99792458 \times 10^8$ m/s 在所有惯性系中恒定。
来源：Michelson-Morley (1887); Einstein (1905)。

**4.2 等效原理**
$m_{\text{惯}} = m_{\text{引}}$。局域无法区分引力场与加速参考系。
来源：Einstein (1907); [WILL]; [ZYCH]。

**4.3 广义协变性**
物理定律在所有坐标系中同形式。
推论：引力 = 时空弯曲 → 广义相对论场方程。

---

## 5. 热力学第二定律

$$\Delta S \geq 0$$

孤立系统的熵永不减少。

**特殊地位**：所有微观定律（QM、相对论）在时间上反演对称。时间箭头的来源需额外的"过去假设"（Past Hypothesis）：宇宙起始于极低熵状态。

**来源**：Clausius (1850); Boltzmann $S=k\ln W$ (1877); Past Hypothesis: [STAN-CAUSAL]
