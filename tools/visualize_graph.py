#!/usr/bin/env python3
# Render with: dot -Tpng physics_foundations_graph.dot -o graph.png

import yaml
import sys
import os
from collections import defaultdict

LAYER_STYLE = {
    "kernel":     {"color": "#DC143C", "fillcolor": "#FFE4E1", "fontcolor": "#8B0000", "shape": "box",     "penwidth": "2"},
    "rule":       {"color": "#FF8C00", "fillcolor": "#FFF5E0", "fontcolor": "#8B4513", "shape": "box",     "penwidth": "2"},
    "law":        {"color": "#1E90FF", "fillcolor": "#E8F4FD", "fontcolor": "#003366", "shape": "ellipse", "penwidth": "1.5"},
    "corollary":  {"color": "#228B22", "fillcolor": "#E8F5E9", "fontcolor": "#1B5E20", "shape": "ellipse", "penwidth": "1.2"},
    "contingent": {"color": "#808080", "fillcolor": "#F5F5F5", "fontcolor": "#333333", "shape": "ellipse", "penwidth": "1"},
}

GRAPH_LAYERS = frozenset(LAYER_STYLE.keys())  # Only these layers appear in the graph

DEFAULT_STYLE = {"color": "black", "fillcolor": "white", "fontcolor": "black", "shape": "ellipse", "penwidth": "1"}


def load_yaml(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)


def _short_label(nid, statement):
    if statement and len(statement) <= 60:
        return statement
    return nid.split(".", 1)[-1].replace("_", " ")


def build_graph(layer1_dir):
    nodes, sources = {}, {}

    fw = load_yaml(os.path.join(layer1_dir, "frameworks.yaml"))
    for k in fw.get("kernels", []):
        nid = k["id"]
        nodes[nid] = {"layer": k.get("layer", "kernel"), "file": "frameworks.yaml",
                      "label": _short_label(nid, k.get("statement"))}
        sources[nid] = []
    for r in fw.get("structural_rules", []):
        nid = r["id"]
        nodes[nid] = {"layer": "rule", "file": "frameworks.yaml",
                      "label": _short_label(nid, r.get("statement"))}
        sources[nid] = []

    el = load_yaml(os.path.join(layer1_dir, "effective_laws.yaml"))
    for law_item in el.get("effective_laws", []):
        nid = law_item["id"]
        layer = law_item.get("layer", "effective_law")
        if layer == "effective_law":
            layer = "corollary" if nid.startswith("cor.") else "law"
        nodes[nid] = {"layer": layer, "file": "effective_laws.yaml",
                      "label": _short_label(nid, law_item.get("statement"))}
        sources[nid] = list(law_item.get("derived_from", []))

    ct = load_yaml(os.path.join(layer1_dir, "contingent.yaml"))
    for c in ct.get("contingent_facts", []):
        nid = c["id"]
        nodes[nid] = {"layer": "contingent", "file": "contingent.yaml",
                      "label": _short_label(nid, c.get("statement"))}
        sources[nid] = list(c.get("derived_from", []))

    return nodes, sources


def sanitize_id(raw_id):
    return raw_id.replace(".", "_").replace("-", "_")


def write_dot(nodes, sources, output_path):
    lines = [
        "digraph physics_foundations {",
        "    rankdir=LR;",
        '    label="Physics Foundations — Layer1 Dependency Graph";',
        "    labelloc=t;",
        "    fontsize=20;",
        '    fontname="Helvetica";',
        "    node [fontname=\"Helvetica\", fontsize=11];",
        "    edge [fontname=\"Helvetica\", fontsize=9, color=\"#666666\"];",
        "",
    ]

    graph_ids = {nid for nid, info in nodes.items() if info.get("layer") in GRAPH_LAYERS}

    for nid in sorted(graph_ids):
        info = nodes[nid]
        sid = sanitize_id(nid)
        style = LAYER_STYLE.get(info.get("layer", "unknown"), DEFAULT_STYLE)
        label = info.get("label", nid).replace('"', '\\"')
        lines.append(
            f'    {sid} ['
            f'label="{label}", '
            f'color="{style["color"]}", '
            f'fillcolor="{style["fillcolor"]}", '
            f'fontcolor="{style["fontcolor"]}", '
            f'shape={style["shape"]}, '
            f'penwidth={style["penwidth"]}, '
            f'style=filled'
            f'];'
        )

    lines.append("")

    for nid in sorted(graph_ids):
        for src in sources.get(nid, []):
            if src in graph_ids:
                lines.append(f"    {sanitize_id(src)} -> {sanitize_id(nid)};")

    lines.append("}")

    with open(output_path, "w") as f:
        f.write("\n".join(lines) + "\n")

    return output_path


def main():
    layer1_dir = "layer1/"
    output_path = "physics_foundations_graph.dot"
    args = sys.argv[1:]

    for i, arg in enumerate(args):
        if arg in ("--output", "-o") and i + 1 < len(args):
            output_path = args[i + 1]
        elif not arg.startswith("-") and arg != output_path:
            layer1_dir = arg

    if not os.path.isdir(layer1_dir):
        print(f"Error: '{layer1_dir}' is not a directory.", file=sys.stderr)
        sys.exit(1)

    nodes, sources = build_graph(layer1_dir)

    by_layer = defaultdict(int)
    graph_edges = 0
    graph_ids = {nid for nid, info in nodes.items() if info.get("layer") in GRAPH_LAYERS}
    for nid in graph_ids:
        by_layer[nodes[nid]["layer"]] += 1
        for src in sources.get(nid, []):
            if src in graph_ids:
                graph_edges += 1

    print(f"Graph nodes: {len(graph_ids)} | Edges: {graph_edges}")
    print("By layer:", dict(by_layer))

    write_dot(nodes, sources, output_path)
    print(f"\nGraph written to: {output_path}")
    print(f"Render with: dot -Tpng {output_path} -o graph.png")


if __name__ == "__main__":
    main()
