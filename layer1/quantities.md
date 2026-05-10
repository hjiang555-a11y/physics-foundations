# 量注册表

> 从 12 条公理和有效定律提取的全部物理量。
> 量纲向量格式：`[L, M, T, I, Θ, N, J]`（见 `dimensions.md`）。
> 值来源：[CODATA2022], [SI2019]。括号内为 1σ 不确定度。

## 基本力学量

| id | symbol | name | dim | unit_si |
|----|--------|------|-----|---------|
| qty.time | t | time | [0,0,1,0,0,0,0] | s |
| qty.length | r, x, l | length | [1,0,0,0,0,0,0] | m |
| qty.mass | m | mass | [0,1,0,0,0,0,0] | kg |
| qty.velocity | v | velocity | [1,0,-1,0,0,0,0] | m/s |
| qty.momentum | p | momentum | [1,1,-1,0,0,0,0] | kg·m/s |
| qty.force | F | force | [1,1,-2,0,0,0,0] | N |
| qty.energy | E | energy | [2,1,-2,0,0,0,0] | J |
| qty.action | S | action | [2,1,-1,0,0,0,0] | J·s |

**导出关系**：
```
p = m·v         dim: [0,1,0] + [1,0,-1] = [1,1,-1] ✓
F = m·a         dim: [0,1,0] + [1,0,-2] = [1,1,-2] ✓
E = F·r         dim: [1,1,-2] + [1,0,0] = [2,1,-2] ✓
S = ∫L dt       dim: [2,1,-2] + [0,0,1] = [2,1,-1] ✓
```

## 引力量

| id | symbol | name | dim | value |
|----|--------|------|-----|-------|
| qty.inertial_mass | mᵢ | inertial mass | [0,1,0,0,0,0,0] | — |
| qty.gravitational_mass | m_g | gravitational mass | [0,1,0,0,0,0,0] | — |
| cst.G | G | gravitational constant | [3,-1,-2,0,0,0,0] | 6.67430(15)×10⁻¹¹ m³/(kg·s²) |

## 电磁量

| id | symbol | name | dim | value |
|----|--------|------|-----|-------|
| qty.electric_charge | q | electric charge | [0,0,1,1,0,0,0] | — |
| qty.electric_field | E | electric field | [1,1,-3,-1,0,0,0] | — |
| qty.magnetic_field | B | magnetic flux density | [0,1,-2,-1,0,0,0] | — |
| cst.ε₀ | ε₀ | vacuum permittivity | [-3,-1,4,2,0,0,0] | 8.8541878188(14)×10⁻¹² F/m |
| cst.μ₀ | μ₀ | vacuum permeability | [1,1,-2,-2,0,0,0] | 1.25663706127(20)×10⁻⁶ N/A² |

**导出关系**：
```
F = qE          dim: [0,0,1,1] + [1,1,-3,-1] = [1,1,-2,0] ✓
F = qv×B        dim: [0,0,1,1] + [1,0,-1,0] + [0,1,-2,-1] = [1,1,-2,0] ✓
c = 1/√(ε₀μ₀)  dim: -½·([-3,-1,4,2] + [1,1,-2,-2]) = -½·[-2,0,2,0] = [1,0,-1,0] ✓
```

## 热力学量

| id | symbol | name | dim | value |
|----|--------|------|-----|-------|
| qty.entropy | S | entropy | [2,1,-2,0,-1,0,0] | — |
| qty.temperature | T | temperature | [0,0,0,0,1,0,0] | — |
| qty.pressure | P | pressure | [-1,1,-2,0,0,0,0] | — |
| qty.volume | V | volume | [3,0,0,0,0,0,0] | — |
| qty.amount_of_substance | n | amount of substance | [0,0,0,0,0,1,0] | — |
| cst.k | k | Boltzmann constant | [2,1,-2,0,-1,0,0] | 1.380649×10⁻²³ J/K (exact) |
| cst.R | R | gas constant | [2,1,-2,0,-1,-1,0] | 8.314462618 J/(mol·K) |

**导出关系**：
```
PV = nRT        dim: [-1,1,-2] + [3,0,0] = [2,1,-2]  vs  [0,0,0,0,0,1] + [2,1,-2,0,-1,-1] + [0,0,0,0,1] = [2,1,-2] ✓
S = k ln W      dim: [2,1,-2,0,-1] = [2,1,-2,0,-1] (ln W 无量纲) ✓
R = N_A·k       dim: [0,0,0,0,0,-1] + [2,1,-2,0,-1,0] = [2,1,-2,0,-1,-1] ✓
```

## 量子量

| id | symbol | name | dim |
|----|--------|------|-----|
| qty.state_vector | \|ψ⟩ | state vector | [0,0,0,0,0,0,0] |
| qty.complex_amplitude | α, β | complex amplitude | [0,0,0,0,0,0,0] |
| cst.ℏ | ℏ | reduced Planck constant | [2,1,-1,0,0,0,0] |

**ℏ 值**: 1.054571817...×10⁻³⁴ J·s (exact, h/2π)

**注**：波函数 ψ(x) 在位置表象中量纲为 $L^{-d/2}$（非整数，BIPM 规范以外）。状态向量 \|ψ⟩ 无量纲——量纲由基底 \|x⟩ 携带。本注册表统一使用无量纲的态矢量。

**导出关系**：
```
[ℏ] = [action] = M·L²·T⁻¹  dim: [2,1,-1] ✓
[ℏ] = [energy]·[time]       dim: [2,1,-2] + [0,0,1] = [2,1,-1] ✓
```

## 相对论量

| id | symbol | name | dim | value |
|----|--------|------|-----|-------|
| cst.c | c | speed of light | [1,0,-1,0,0,0,0] | 299792458 m/s (exact) |

**导出关系**：
```
E = mc²         dim: [0,1,0] + 2·[1,0,-1] = [2,1,-2] ✓
```

## 量纲常数汇总

| id | symbol | dim | value | exact? |
|----|--------|-----|-------|--------|
| cst.c | c | [1,0,-1,0,0,0,0] | 2.99792458×10⁸ m/s | ✓ |
| cst.ℏ | ℏ | [2,1,-1,0,0,0,0] | 1.054571817...×10⁻³⁴ J·s | ✓ |
| cst.k | k | [2,1,-2,0,-1,0,0] | 1.380649×10⁻²³ J/K | ✓ |
| cst.G | G | [3,-1,-2,0,0,0,0] | 6.67430(15)×10⁻¹¹ m³/(kg·s²) | ✗ |
| cst.ε₀ | ε₀ | [-3,-1,4,2,0,0,0] | 8.8541878188(14)×10⁻¹² F/m | ✗ |
| cst.μ₀ | μ₀ | [1,1,-2,-2,0,0,0] | 1.25663706127(20)×10⁻⁶ N/A² | ✗ |
| cst.R | R | [2,1,-2,0,-1,-1,0] | 8.314462618 J/(mol·K) | ✗ |

ε₀ 和 μ₀ 自 SI 2019 起非 exact：μ₀ = 4παℏ/(e²c)，ε₀ = 1/(μ₀c²)。G 为最不精确的基本常数 (2.2×10⁻⁵)。
