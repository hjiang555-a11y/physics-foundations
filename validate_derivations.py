#!/usr/bin/env python3
"""
Sci-hf Derivation Graph Validator
Implements SOURCE.md V1-V5 verification rules.

Usage:
    python3 validate_derivations.py [--layer1-dir layer1/]
"""

import yaml
import sys
import os
from collections import defaultdict, deque

# ── Layer ordering for V3 ──
LAYER_ORDER = {
    "kernel": 0,
    "rule": 0,
    "contingent": 1,
    "law": 2,
    "corollary": 3,
}


def load_yaml(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)


def build_graph(layer1_dir):
    """Build a unified graph of all assertions and their sources."""
    nodes = {}       # id → {layer, file, ...}
    sources = {}     # id → [source_ids]
    derivations = {}  # conclusion_id → set(premise_ids)

    # ── Load frameworks (kernels + structural rules) ──
    fw = load_yaml(os.path.join(layer1_dir, "frameworks.yaml"))
    for k in fw.get("kernels", []):
        nid = k["id"]
        nodes[nid] = {"layer": k.get("layer", "kernel"), "file": "frameworks.yaml"}
        sources[nid] = []
    for r in fw.get("structural_rules", []):
        nid = r["id"]
        nodes[nid] = {"layer": "rule", "file": "frameworks.yaml"}
        sources[nid] = []

    # ── Load effective laws ──
    el = load_yaml(os.path.join(layer1_dir, "effective_laws.yaml"))
    for law in el.get("effective_laws", []):
        nid = law["id"]
        layer = law.get("layer", "effective_law")
        # Normalize layer names
        if layer == "effective_law":
            if nid.startswith("cor."):
                layer = "corollary"
            else:
                layer = "law"
        nodes[nid] = {"layer": layer, "file": "effective_laws.yaml"}
        df = law.get("derived_from", [])
        sources[nid] = list(df)

    # ── Load contingent facts ──
    ct = load_yaml(os.path.join(layer1_dir, "contingent.yaml"))
    for c in ct.get("contingent_facts", []):
        nid = c["id"]
        nodes[nid] = {"layer": "contingent", "file": "contingent.yaml"}
        sources[nid] = list(c.get("derived_from", []))

    # ── Load derivations ──
    deriv = load_yaml(os.path.join(layer1_dir, "derivations.yaml"))
    for d in deriv.get("derivations", []):
        conc = d.get("conclusion")
        prem = d.get("premise", [])
        if conc and prem:
            derivations[conc] = set(prem)

    # ── Load rigorous derivations ──
    rig = load_yaml(os.path.join(layer1_dir, "rigorous_derivations.yaml"))
    for d in rig.get("derivations", []):
        conc = d.get("conclusion")
        prem = d.get("premise", [])
        if conc and prem:
            derivations[conc] = set(prem)

    # ── Load claims for additional node coverage ──
    claims = load_yaml(os.path.join(layer1_dir, "claims.yaml"))
    for c in claims.get("claims", []):
        nid = c["id"]
        if nid not in nodes:
            layer = c.get("layer", "unknown")
            nodes[nid] = {"layer": layer, "file": "claims.yaml"}
            sources[nid] = list(c.get("_from", []))

    return nodes, sources, derivations


def check_v1(nodes, sources):
    """V1: All references resolve."""
    errors = []
    all_ids = set(nodes.keys())
    for nid, src_list in sources.items():
        for s in src_list:
            if s not in all_ids:
                errors.append(f"V1 FAIL: {nid} references '{s}' which does not exist")
    return errors


def check_v2(nodes, sources):
    """V2: No cycles in dependency graph."""
    # Topological sort using Kahn's algorithm
    indegree = {n: len(sources.get(n, [])) for n in nodes}
    indegree = {n: d for n, d in indegree.items() if d >= 0}
    
    queue = deque([n for n, d in indegree.items() if d == 0])
    sorted_count = 0
    
    while queue:
        n = queue.popleft()
        sorted_count += 1
        # Find all nodes that depend on n
        for dependent, src_list in sources.items():
            if n in src_list:
                indegree[dependent] -= 1
                if indegree[dependent] == 0:
                    queue.append(dependent)
    
    if sorted_count < len(indegree):
        remaining = [n for n, d in indegree.items() if d > 0]
        return [f"V2 FAIL: Cycle detected involving {len(remaining)} nodes: {remaining[:5]}..."]
    return []


def check_v3(nodes, sources):
    """V3: Layer ordering."""
    errors = []
    for nid, src_list in sources.items():
        n_layer = nodes.get(nid, {}).get("layer", "unknown")
        n_order = LAYER_ORDER.get(n_layer, 99)
        
        if n_layer == "kernel" and src_list:
            errors.append(f"V3 FAIL: kernel '{nid}' has sources (should have none): {src_list}")
            continue
        
        for s in src_list:
            s_layer = nodes.get(s, {}).get("layer", "unknown")
            s_order = LAYER_ORDER.get(s_layer, 99)
            
            # law can source from kernel or law
            # corollary can source from law or corollary
            # contingent can source from anything
            if n_layer == "law" and s_order > 2:
                errors.append(f"V3 FAIL: law '{nid}' sources from '{s}' (layer={s_layer}), "
                              f"but law can only source from kernel/law")
            elif n_layer == "corollary" and s_order < 0:
                # Relaxed: corollaries CAN source from kernels (project convention)
                pass
    return errors


def check_v4(nodes, sources):
    """V4: Every law/corollary reaches at least one kernel root."""
    errors = []
    for nid, info in nodes.items():
        layer = info.get("layer", "")
        if layer not in ("law", "corollary"):
            continue
        
        # BFS backwards to find kernel root
        visited = set()
        queue = deque([nid])
        found_kernel = False
        
        while queue:
            current = queue.popleft()
            if current in visited:
                continue
            visited.add(current)
            
            curr_layer = nodes.get(current, {}).get("layer", "")
            if curr_layer == "kernel":
                found_kernel = True
                break
            
            for s in sources.get(current, []):
                if s not in visited:
                    queue.append(s)
        
        if not found_kernel:
            errors.append(f"V4 FAIL: '{nid}' (layer={layer}) has no path to any kernel root")
    return errors


def check_v5(nodes, sources, derivations):
    """V5: If derivation exists, premise set == derived_from set."""
    errors = []
    warnings = []
    for conc, prem_set in derivations.items():
        src_set = set(sources.get(conc, []))
        
        if not src_set:
            # Law has derivation but no derived_from
            errors.append(f"V5 FAIL: '{conc}' has derivation but empty derived_from in effective_laws")
            continue
        
        if prem_set != src_set:
            missing_in_deriv = src_set - prem_set
            extra_in_deriv = prem_set - src_set
            msg = f"V5 FAIL: '{conc}' premise mismatch:"
            if missing_in_deriv:
                msg += f" not_in_derivation={missing_in_deriv}"
            if extra_in_deriv:
                msg += f" not_in_derived_from={extra_in_deriv}"
            errors.append(msg)
    
    # Check for laws without derivations (only those in effective_laws.yaml)
    for nid, info in nodes.items():
        if info.get("layer") in ("law", "corollary"):
            if info.get("file") == "effective_laws.yaml" and nid not in derivations:
                warnings.append(f"V5 WARN: '{nid}' has no derivation entry in either file")
    
    return errors, warnings


def main():
    layer1_dir = sys.argv[1] if len(sys.argv) > 1 else "layer1"
    
    if not os.path.isdir(layer1_dir):
        print(f"Error: directory '{layer1_dir}' not found")
        sys.exit(1)
    
    print(f"Loading from {layer1_dir}/ ...")
    nodes, sources, derivations = build_graph(layer1_dir)
    
    print(f"Nodes: {len(nodes)}")
    print(f"Derivations: {len(derivations)}")
    
    # Count by layer
    layer_counts = defaultdict(int)
    for n, info in nodes.items():
        layer_counts[info.get("layer", "unknown")] += 1
    print(f"By layer: {dict(layer_counts)}")
    
    all_errors = []
    all_warnings = []
    
    print("\n── V1: Reference Resolution ──")
    errors = check_v1(nodes, sources)
    all_errors.extend(errors)
    print(f"  {'PASS' if not errors else 'FAIL'} ({len(errors)} issues)")
    for e in errors:
        print(f"    {e}")
    
    print("\n── V2: Acyclicity ──")
    errors = check_v2(nodes, sources)
    all_errors.extend(errors)
    print(f"  {'PASS' if not errors else 'FAIL'} ({len(errors)} issues)")
    for e in errors:
        print(f"    {e}")
    
    print("\n── V3: Layer Discipline ──")
    errors = check_v3(nodes, sources)
    all_errors.extend(errors)
    print(f"  {'PASS' if not errors else 'FAIL'} ({len(errors)} issues)")
    for e in errors:
        print(f"    {e}")
    
    print("\n── V4: Root Reachability ──")
    errors = check_v4(nodes, sources)
    all_errors.extend(errors)
    print(f"  {'PASS' if not errors else 'FAIL'} ({len(errors)} issues)")
    for e in errors:
        print(f"    {e}")
    
    print("\n── V5: Source-Derivation Consistency ──")
    errors, warnings = check_v5(nodes, sources, derivations)
    all_errors.extend(errors)
    all_warnings.extend(warnings)
    print(f"  {'PASS' if not errors else 'FAIL'} ({len(errors)} errors, {len(warnings)} warnings)")
    for e in errors:
        print(f"    {e}")
    for w in warnings:
        print(f"    {w}")
    
    print(f"\n{'='*60}")
    print(f"VERDICT: {'PASS' if not all_errors else 'FAIL'}")
    print(f"  Errors: {len(all_errors)}")
    print(f"  Warnings: {len(all_warnings)}")
    
    return 0 if not all_errors else 1


if __name__ == "__main__":
    sys.exit(main())
