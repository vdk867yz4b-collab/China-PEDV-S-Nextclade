import csv
import json
from collections import Counter
from datetime import date
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
DATASET = REPO / "nextclade_dataset_pedv_s_genbank_china_isolates"
AUSPICE = REPO / "auspice"
SUPPLEMENTARY = REPO / "supplementary"
TREE_JSON = DATASET / "tree.json"
AUSPICE_TREE_JSON = AUSPICE / "china_pedv_s_genbank.json"
FREQUENCY_METADATA = SUPPLEMENTARY / "frequency_metadata.tsv"
SUMMARY_JSON = SUPPLEMENTARY / "frequency_streamtree_summary.json"


def get_attr(attrs, key):
    value = attrs.get(key)
    if isinstance(value, dict):
        return value.get("value")
    return value


def walk(node):
    yield node
    for child in node.get("children", []):
        yield from walk(child)


def tip_rows(tree):
    rows = []
    for node in walk(tree):
        if node.get("children"):
            continue
        attrs = node.get("node_attrs", {})
        strain = node.get("name")
        collection_date = get_attr(attrs, "collection_date")
        genotype = get_attr(attrs, "pedv_genotype") or get_attr(attrs, "clade_membership")
        if not strain or not collection_date or not genotype:
            continue
        rows.append(
            {
                "strain": strain,
                "date": collection_date,
                "collection_date": collection_date,
                "pedv_genotype": genotype,
                "clade_membership": get_attr(attrs, "clade_membership") or genotype,
            }
        )
    return rows


def clear_stream_labels(node, label_key):
    labels = node.get("branch_attrs", {}).get("labels")
    if isinstance(labels, dict):
        labels.pop(label_key, None)


def add_stream_labels(node, label_key, parent_pure=None):
    children = node.get("children", [])
    if not children:
        attrs = node.get("node_attrs", {})
        genotype = get_attr(attrs, "pedv_genotype") or get_attr(attrs, "clade_membership")
        return {genotype} if genotype else set(), 0

    child_sets = []
    label_count = 0
    for child in children:
        child_set, child_labels = add_stream_labels(child, label_key, parent_pure=None)
        child_sets.append(child_set)
        label_count += child_labels

    descendant_genotypes = set().union(*child_sets) if child_sets else set()
    current_pure = next(iter(descendant_genotypes)) if len(descendant_genotypes) == 1 else None

    if current_pure and current_pure != parent_pure:
        labels = node.setdefault("branch_attrs", {}).setdefault("labels", {})
        labels[label_key] = current_pure
        label_count += 1

    for child in children:
        suppress_descendant_labels(child, label_key, current_pure)

    return descendant_genotypes, label_count


def suppress_descendant_labels(node, label_key, inherited_pure):
    children = node.get("children", [])
    if not children:
        return
    genotypes = set()
    for child in children:
        genotypes.update(collect_tip_genotypes(child))
    current_pure = next(iter(genotypes)) if len(genotypes) == 1 else None
    if current_pure and current_pure == inherited_pure:
        labels = node.get("branch_attrs", {}).get("labels")
        if isinstance(labels, dict):
            labels.pop(label_key, None)
    for child in children:
        suppress_descendant_labels(child, label_key, inherited_pure if current_pure == inherited_pure else current_pure)


def collect_tip_genotypes(node):
    if not node.get("children"):
        attrs = node.get("node_attrs", {})
        genotype = get_attr(attrs, "pedv_genotype") or get_attr(attrs, "clade_membership")
        return {genotype} if genotype else set()
    genotypes = set()
    for child in node.get("children", []):
        genotypes.update(collect_tip_genotypes(child))
    return genotypes


def count_branch_labels(tree, label_key):
    counts = Counter()
    for node in walk(tree):
        labels = node.get("branch_attrs", {}).get("labels", {})
        value = labels.get(label_key) if isinstance(labels, dict) else None
        if value:
            counts[value] += 1
    return counts


def write_frequency_metadata(rows):
    fieldnames = ["strain", "date", "collection_date", "pedv_genotype", "clade_membership"]
    with FREQUENCY_METADATA.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main():
    data = json.loads(TREE_JSON.read_text(encoding="utf-8"))
    tree = data["tree"]
    label_key = "pedv_genotype"

    for node in walk(tree):
        clear_stream_labels(node, label_key)
    add_stream_labels(tree, label_key)

    meta = data.setdefault("meta", {})
    panels = meta.setdefault("panels", [])
    for panel in ["tree", "frequencies", "entropy"]:
        if panel not in panels:
            panels.append(panel)
    meta["panels"] = [panel for panel in ["tree", "frequencies", "entropy"] if panel in panels]
    meta["stream_labels"] = [label_key]

    display_defaults = meta.setdefault("display_defaults", {})
    display_defaults["layout"] = "rect"
    display_defaults["color_by"] = "pedv_genotype"
    display_defaults["branch_label"] = "clade"
    display_defaults["stream_label"] = label_key
    display_defaults["distance_measure"] = "num_date"

    rows = tip_rows(tree)
    write_frequency_metadata(rows)

    json_text = json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n"
    TREE_JSON.write_text(json_text, encoding="utf-8")
    AUSPICE.mkdir(exist_ok=True)
    AUSPICE_TREE_JSON.write_text(json_text, encoding="utf-8")

    summary = {
        "updated": date.today().isoformat(),
        "frequency_metadata": str(FREQUENCY_METADATA.relative_to(REPO)).replace("\\", "/"),
        "auspice_tree": str(AUSPICE_TREE_JSON.relative_to(REPO)).replace("\\", "/"),
        "auspice_tip_frequencies": "auspice/china_pedv_s_genbank_tip-frequencies.json",
        "tips_with_frequency_metadata": len(rows),
        "tip_genotype_counts": dict(Counter(row["pedv_genotype"] for row in rows)),
        "stream_label_key": label_key,
        "stream_label_counts": dict(count_branch_labels(tree, label_key)),
        "panels": meta["panels"],
        "display_defaults": display_defaults,
    }
    SUMMARY_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
