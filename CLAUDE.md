# physics-foundations — Layer 1 Physics Deductions (Round 13)

## REPO OVERVIEW
- Layer 1 kernel laws and derivations in YAML format
- Remote: origin → https://github.com/hjiang555-a11y/physics-foundations.git
- Branch: main only (no feature branches)
- Current: 150 nodes / 43 derivations / 63 DOT graph nodes / 119 edges
- Validator: V1-V5 ALL PASS (0 errors, 0 warnings)
- Meta-validator: tools/meta_validate.py — 100% completeness, all kernels necessary

## KEY FILES
- layer1/frameworks.yaml — kernel root nodes (13) + structural rules (3)
- layer1/claims.yaml — kernel claim definitions (id, statement, layer)
- layer1/derivations.yaml — 43 compact derivations (steps + necessity/sufficiency)
- layer1/effective_laws.yaml — 30 laws + 7 corollaries (37 total derivable)
- layer1/rigorous_derivations.yaml — 43 detailed mathematical derivations
- layer1/contingent.yaml — 11 contingent facts (7 derived + 4 pure empirical)
- layer1/PROOF.md — completeness/necessity/consistency formal proof
- layer1/README.md — atom inventory and edge graph
- rules.md — R1-R6 core rules documentation (round 12)
- ROADMAP.md — project roadmap (round 13)

## DEPENDENCY TRACING
- Kernel nodes: `kernel.<name>` — 13 foundational claims
- Law nodes: `law.<name>` — 30 derived effective laws
- Corollary nodes: `cor.<name>` — 7 derived corollaries
- Contingent nodes: `contingent.<name>` — 11 empirical/derived facts
- `derived_from` / `premise` fields link nodes back to kernel roots
- Max derivation depth: 2 (cor.kepler_third, via law.newton_second)

## DERIVATION GROUPS (G1-G11)
- G1: Euler-Lagrange (1 derivation)
- G2: Noether + Conservation (5)
- G3: Newton's Laws (3)
- G4: Maxwell + Lorentz (6)
- G5: Quantum Mechanics (5)
- G6: Relativity (4)
- G7: Thermodynamics (5)
- G8: Corollaries (3)
- G9: Contingent Consequences (7)
- G10: Nernst Unattainability (1)
- G11: Standard Model EFT (3)

## VALIDATION
```bash
python3 validate_derivations.py layer1/       # V1-V5 checks
python3 tools/meta_validate.py layer1/         # Completeness + necessity + consistency
python3 tools/visualize_graph.py layer1/       # DOT graph generation
```

## COMMIT CONVENTIONS
- English, semantic style: `type: message` (feat, fix, docs, refactor, chore)
- Atomic commits split by concern
- Footer: "Ultraworked with Sisyphus" + Co-authored-by trailer
- Use `GIT_MASTER=1` prefix for all git commands
