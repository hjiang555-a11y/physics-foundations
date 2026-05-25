# physics-foundations — Layer 1 Physics Deductions

## REPO OVERVIEW
- Layer 1 kernel laws and derivations in YAML format
- Remote: origin → https://github.com/hjiang555-a11y/physics-foundations.git
- Branch: main only (no feature branches)

## KEY FILES
- layer1/claims.yaml — kernel claim definitions (id, statement, layer)
- layer1/derivations.yaml — derivation steps linking premises to conclusions
- layer1/effective_laws.yaml — derived effective laws with quantities
- layer1/rigorous_derivations.yaml — detailed mathematical derivations
- layer1/physics.scihf — SciHF markup of physical laws
- layer1/README.md — atom inventory and edge graph (59 nodes / 105 edges)
- rules.md — R1-R6 core rules documentation

## DEPENDENCY TRACING
- Kernel nodes: `kernel.<name>` — foundational claims (least_action, lorentz_invariance, etc.)
- Law nodes: `law.<name>` — derived effective laws
- `derived_from` / `premise` / `_from` fields link laws back to kernel nodes
- `kernel.light_speed_invariance` was merged into `kernel.lorentz_invariance`
- Source graph: currently 59 nodes, 105 edges

## COMMIT CONVENTIONS
- English, semantic style: `type: message` (feat, fix, docs, refactor, chore)
- Atomic commits split by concern (separate YAML data types, docs)
- Footer: "Ultraworked with Sisyphus" + Co-authored-by trailer
- Use `GIT_MASTER=1` prefix for all git commands

## GITIGNORE
- `.sisyphus/` — sisyphus working files
- `mvp` — symlink to ~/Sci-hf/mvp
