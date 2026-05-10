# 量纲系统

## 基础

BIPM SI Brochure (9th ed., 2019) §2.3.3。任意物理量 $Q$ 的量纲为：

$$\dim Q = L^\alpha \, M^\beta \, T^\gamma \, I^\delta \, \Theta^\varepsilon \, N^\zeta \, J^\eta$$

## 向量表示

量纲以 7 维整数向量表示，位置固定：

```
[L, M, T, I, Θ, N, J]
 0  1  2  3  4  5  6
```

| 索引 | 维度 | 符号 | SI 基本单位 |
|------|------|------|-----------|
| 0 | length | L | metre (m) |
| 1 | mass | M | kilogram (kg) |
| 2 | time | T | second (s) |
| 3 | electric current | I | ampere (A) |
| 4 | thermodynamic temperature | Θ | kelvin (K) |
| 5 | amount of substance | N | mole (mol) |
| 6 | luminous intensity | J | candela (cd) |

## 运算规则

**量纲一致性（等式检查）**：
两个量可以出现在等式/和/差的两边，当且仅当它们的量纲向量相等。

$$A = B \implies \dim(A) = \dim(B)$$

$$A + B \implies \dim(A) = \dim(B)$$

**乘法**：量纲向量逐分量相加。
$$\dim(A \cdot B) = \dim(A) + \dim(B)$$

**除法**：量纲向量逐分量相减。
$$\dim(A / B) = \dim(A) - \dim(B)$$

**幂**：量纲向量逐分量乘以指数。
$$\dim(A^n) = n \cdot \dim(A)$$

**无量纲量**：全零向量。
$$\dim(Q) = [0,0,0,0,0,0,0]$$

## 验证示例

速度 $v = dr/dt$：
$$\dim(v) = \dim(r) - \dim(t) = [1,0,0,0,0,0,0] - [0,0,1,0,0,0,0] = [1,0,-1,0,0,0,0]$$

力 $F = ma$：
$$\dim(F) = \dim(m) + \dim(a) = [0,1,0,0,0,0,0] + [1,0,-2,0,0,0,0] = [1,1,-2,0,0,0,0]$$

真空光速验证 $c = 1/\sqrt{\varepsilon_0\mu_0}$：
$$\dim(\varepsilon_0) + \dim(\mu_0) = [-3,-1,4,2,0,0,0] + [1,1,-2,-2,0,0,0] = [-2,0,2,0,0,0,0]$$
$$\dim(1/c^2) = -2 \cdot [1,0,-1,0,0,0,0] = [-2,0,2,0,0,0,0] \; \checkmark$$

## 实现约束

- 指数为整数（BIPM 规范）。量子波函数 $\psi(x)$ 的量纲 $L^{-3/2}$ 以注释标注。
- 状态向量 $\vert\psi\rangle$ 无量纲（量纲吸收在基底 $\vert x\rangle$ 中）。
- 此 7 维系统覆盖全部经典物理。电磁学使用 SI。如需 Gaussian/CGS，基本量纲集需可配置。

## 来源

[BIPM] SI Brochure, 9th ed. (2019, updated 2025), §2.3.3
ISO/IEC 80000-1
