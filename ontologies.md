# 参考本体论

## QUDT — Quantities, Units, Dimensions and Types

- **网址**: `qudt.org`
- **来源**: NASA NExIOM (AMES Research Center) → QUDT.org 公益组织
- **许可证**: CC BY 4.0
- **版本**: v3.2 (2026)

**核心模型**:
```
QuantityKind → DimensionVector → Unit → QuantityValue
```

**量纲向量**: SI 7 维 $(\text{M,L,T,I,Θ,N,J})$。同时支持 CGS, CGS-ESU, CGS-EMU, Gaussian, Planck 自然单位。

**Vocabularies**:
- `qudt.org/vocab/unit` — 单位
- `qudt.org/vocab/quantitykind` — 量种类
- `qudt.org/vocab/dimensionvector` — 量纲向量 (274 个实例)
- `qudt.org/vocab/constant` — 物理常数
- `qudt.org/vocab/sou` — 单位制
- `qudt.org/vocab/soqk` — 量种类制

**对 sci-hf 的启示**:
- 量纲分析 = 向量比较（等价 ↔ 向量相等）
- 多单位制支持证明语言必须允许基本量纲集可配置
- DimensionVector 格式可直接作为 sci-hf 量纲系统的参考实现
- `QuantityKind vs Quantity` 对应 sci-hf 的 `QuantityDef (类型) vs 命题中的量引用 (实例)`
- QUDT **不建模**物理定律、命题关系、推导——sci-hf 的增量在此

---

## OM 2.0 — Ontology of units of Measure

- **网址**: `github.com/HajoRijgersberg/OM`
- **实现**: OWL 2
- **覆盖域**: 力学、热力学、电磁学、流体力学、核物理、天文学、食品工程等
- **特点**: Unit + Quantity + Measure + Dimension 四层；支持 scale（如 Celsius 温标 vs Kelvin 单位）
