# 第一层：有效定律

> 从基本公理推出。不是公理，但科学描述语言必须能表达。

---

## 力学

**牛顿第一定律**
$$\mathbf{F}=0 \implies \frac{d\mathbf{v}}{dt}=0$$
推出：最小作用量 + 均匀时空（无外力时 $L=\frac{1}{2}mv^2$）。

**牛顿第二定律**
$$\mathbf{F}=\frac{d\mathbf{p}}{dt}$$
推出：最小作用量 → Euler-Lagrange → $\frac{d}{dt}\frac{\partial L}{\partial\dot{q}} = \frac{\partial L}{\partial q}$。定义 $\mathbf{F} = -\nabla V$ 即得。

**牛顿第三定律**
$$\mathbf{F}_{12}=-\mathbf{F}_{21}$$
推出：动量守恒（空间平移对称 → Noether）。弱形式（等大反向）必然成立；强形式（沿连线）不普遍（电磁学中失效）。

**万有引力定律**
$$\mathbf{F}=-G\frac{m_1m_2}{r^2}\hat{\mathbf{r}}$$
推出：广义相对论的弱场、低速极限。

---

## 电磁学 — Maxwell 方程组

全部四条由 $U(1)$ 规范对称 + 最小作用量 + 相对论协变性推出。

**Gauss 定律**
$$\nabla\cdot\mathbf{E}=\frac{\rho}{\varepsilon_0}$$
来源：$\partial_\mu F^{\mu\nu} = J^\nu$ 的 $\nu=0$ 分量。

**磁 Gauss 定律**
$$\nabla\cdot\mathbf{B}=0$$
来源：$F_{\mu\nu} = \partial_\mu A_\nu - \partial_\nu A_\mu$ 的比安基恒等式（几何必然）。

**法拉第感应定律**
$$\nabla\times\mathbf{E}=-\frac{\partial\mathbf{B}}{\partial t}$$
来源：比安基恒等式 $\partial_\lambda F_{\mu\nu} + \partial_\mu F_{\nu\lambda} + \partial_\nu F_{\lambda\mu} = 0$。

**Ampère-Maxwell 定律**
$$\nabla\times\mathbf{B}=\mu_0\mathbf{J}+\mu_0\varepsilon_0\frac{\partial\mathbf{E}}{\partial t}$$
来源：$\partial_\mu F^{\mu\nu} = J^\nu$ 的 $\nu=1,2,3$ 分量。位移电流项是 Maxwell 为自洽性引入的理论修正。

**洛伦兹力定律**
$$\mathbf{F}=q(\mathbf{E}+\mathbf{v}\times\mathbf{B})$$
推出：$U(1)$ 规范相互作用的必然形式。

---

## 量子力学

**薛定谔方程**
$$i\hbar\frac{\partial\psi}{\partial t} = \hat{H}\psi$$
推出：幺正演化公设 + 能量算符 $\hat{H} = -\frac{\hbar^2}{2m}\nabla^2 + V$。

**$E=h\nu$**
推出：正则量子化（$[x,p]=i\hbar$ + 谐振子本征值 $E_n = (n+\frac{1}{2})h\nu$）。

**$\lambda=h/p$（德布罗意关系）**
推出：$E=h\nu$ + $p=E/c$（光子）→ 推广至物质波（1924 假设，Davisson-Germer 1927 验证）。

**泡利不相容原理**
推出：自旋-统计定理（量子场论；依赖微观因果性 + 正能量）。非相对论 QM 中作为独立假设。

**不确定性原理**
$$\sigma_x\sigma_p \geq \frac{\hbar}{2}$$
推出：$[x,p]=i\hbar$ 的数学推论（Kennard 1927）。

**Born 规则**
$$P = |\psi|^2$$
推出：量子力学测量公设的推论。

---

## 统计力学与热力学

**$S=k\ln W$（玻尔兹曼熵公式）**
$$S=k_B\ln W$$
推出：统计力学对熵的微观定义。不是热力学公理。

**第二定律 $\Delta S \geq 0$**
推出：$S=k\ln W$ + 过去假设（宇宙低熵初始条件）。

**第三定律 $S\to 0$ 当 $T\to 0$**
推出：量子统计力学。完美晶体基态非简并 → $W=1$ → $S=0$。

**第一定律（能量守恒）**
推出：时间平移对称 → Noether。

**第零定律（热平衡传递性）**
推出：统计力学平衡态的定义性质。

---

## 相对论

**洛伦兹变换**
$$t' = \gamma(t - vx/c^2), \quad x' = \gamma(x - vt), \quad \gamma = 1/\sqrt{1-v^2/c^2}$$
推出：光速不变 + 相对性原理。

**$E=mc^2$**
推出：狭义相对论。四维动量 $p^\mu = (E/c, \mathbf{p})$ 的不变量 $p_\mu p^\mu = m^2 c^2$。

**广义相对论场方程**
$$G_{\mu\nu} = \frac{8\pi G}{c^4} T_{\mu\nu}$$
推出：等效原理 + 最小作用量（Einstein-Hilbert action）+ 广义协变性。

---

## 保守律

全部由 Noether 定理推出（见 fundamental.md §2）。

- 能量守恒 ← 时间平移对称
- 动量守恒 ← 空间平移对称
- 角动量守恒 ← 旋转对称
- 电荷守恒 ← $U(1)$ 规范对称
