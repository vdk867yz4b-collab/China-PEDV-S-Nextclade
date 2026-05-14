import csv
import json
import os
import shutil
import subprocess
import zipfile
from collections import Counter
from datetime import date
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
CHINA_ROOT = REPO.parent
OLD_WORK = Path("C:/ChinaPEDVnextstrain_work/nextclade_2011_clade_build")
WORK = Path("C:/ChinaPEDVnextstrain_work/nextclade_aj1102_reference_build")
DATASET = REPO / "nextclade_dataset_pedv_s_genbank_china_isolates"
SUPPLEMENTARY = REPO / "supplementary"
SOURCE_COMPANION = CHINA_ROOT / "ChinaPEDVnextstrain" / "nextclade_dataset_pedv_s_genbank_china_isolates_companion"
SOURCE_DATASET = CHINA_ROOT / "ChinaPEDVnextstrain" / "nextclade_dataset_pedv_s_genbank_china_isolates"
REFERENCE_ACCESSION = "JX188454.1"
REFERENCE_STRAIN = "AJ1102"
REFERENCE_NAME = "PEDV_S_AJ1102"
DATASET_TITLE = "GenBank China PEDV S isolate Nextclade dataset"
CLADE_COLORS = {
    "G1a": "#4E79A7",
    "G1b": "#59A14F",
    "S-INDEL": "#76B7B2",
    "G2a": "#F28E2B",
    "G2b": "#E15759",
    "G2c": "#B07AA1",
}


def read_fasta(path):
    records = []
    name = None
    seq = []
    with path.open(encoding="utf-8", errors="ignore") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if name is not None:
                    records.append((name, "".join(seq).upper()))
                name = line[1:].strip()
                seq = []
            else:
                seq.append(line)
    if name is not None:
        records.append((name, "".join(seq).upper()))
    return records


def write_fasta(path, records):
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for name, seq in records:
            handle.write(f">{name}\n")
            for i in range(0, len(seq), 80):
                handle.write(seq[i : i + 80] + "\n")


def accession_from_header(header):
    return header.split("|", 1)[0].split()[0].split("_", 1)[0]


def load_tsv(path):
    with path.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path, rows, fieldnames):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def numeric_date(date_text):
    if not date_text:
        return None
    parts = [int(part) for part in date_text.split("-") if part]
    if len(parts) == 1:
        return float(parts[0])
    if len(parts) == 2:
        year, month = parts
        start = date(year, month, 1)
        end = date(year + (month == 12), 1 if month == 12 else month + 1, 1)
        midpoint = start.toordinal() + (end.toordinal() - start.toordinal()) / 2
    else:
        year, month, day = parts[:3]
        midpoint = date(year, month, day).toordinal()
    year_start = date(parts[0], 1, 1).toordinal()
    next_year = date(parts[0] + 1, 1, 1).toordinal()
    return parts[0] + (midpoint - year_start) / (next_year - year_start)


def run(cmd):
    print(" ".join(str(part) for part in cmd), flush=True)
    subprocess.run(cmd, check=True)


def docker_path(path):
    path = Path(path)
    try:
        rel = path.relative_to(WORK)
        return f"/work/{rel.as_posix()}"
    except ValueError:
        raise RuntimeError(f"Path is not inside work directory: {path}")


def load_old_tip_attrs():
    old_tree_path = SOURCE_DATASET / "tree.json"
    if not old_tree_path.exists():
        old_tree_path = DATASET / "tree.json"
    if not old_tree_path.exists():
        return {}
    tree = json.loads(old_tree_path.read_text(encoding="utf-8"))
    attrs = {}

    def visit(node):
        if not node.get("children"):
            attrs[node["name"]] = node.get("node_attrs", {})
        for child in node.get("children", []):
            visit(child)

    visit(tree["tree"])
    return attrs


def summarize_child_clades(node):
    counts = Counter()

    def visit(current):
        if not current.get("children"):
            clade = current.get("node_attrs", {}).get("clade_membership", {}).get("value", "")
            counts[clade] += 1
        for child in current.get("children", []):
            visit(child)

    visit(node)
    return dict(counts)


def annotate_tree(raw_tree, clade_by_accession, old_tip_attrs):
    stats = {
        "tree_tips_total": 0,
        "tree_tip_labels": 0,
        "tree_tips_without_clade": 0,
        "tree_internal_pure_labels": 0,
        "tree_internal_majority_labels": 0,
        "tips_with_collection_date": 0,
    }

    def set_clade_attrs(node_attrs, clade):
        node_attrs["clade_membership"] = {"value": clade}
        node_attrs["pedv_genotype"] = {"value": clade}
        node_attrs["clade_display"] = {"value": clade}

    def visit(node):
        node_attrs = node.setdefault("node_attrs", {})
        children = node.get("children", [])
        if not children:
            stats["tree_tips_total"] += 1
            accession = node["name"]
            for key, value in old_tip_attrs.get(accession, {}).items():
                if key not in node_attrs:
                    node_attrs[key] = value
            clade = clade_by_accession.get(accession, "")
            if clade:
                set_clade_attrs(node_attrs, clade)
                stats["tree_tip_labels"] += 1
            else:
                stats["tree_tips_without_clade"] += 1
            if node_attrs.get("collection_date", {}).get("value"):
                stats["tips_with_collection_date"] += 1
            return [clade] if clade else [], [node_attrs.get("num_date", {}).get("value")] if node_attrs.get("num_date") else []

        clades = []
        dates = []
        for child in children:
            child_clades, child_dates = visit(child)
            clades.extend(child_clades)
            dates.extend([value for value in child_dates if isinstance(value, (int, float))])
        counts = Counter(clades)
        if len(counts) == 1:
            clade = next(iter(counts))
            set_clade_attrs(node_attrs, clade)
            stats["tree_internal_pure_labels"] += 1
        elif counts:
            clade, count = sorted(counts.items(), key=lambda item: (-item[1], item[0]))[0]
            if count / sum(counts.values()) >= 0.5:
                set_clade_attrs(node_attrs, clade)
                stats["tree_internal_majority_labels"] += 1
        if dates:
            node_attrs["num_date"] = {"value": sum(dates) / len(dates)}
        return clades, dates

    visit(raw_tree["tree"])

    def add_branch_labels(node, parent_clade=None):
        clade = node.get("node_attrs", {}).get("clade_membership", {}).get("value")
        if clade and clade != parent_clade:
            node.setdefault("branch_attrs", {}).setdefault("labels", {})["clade"] = clade
        for child in node.get("children", []):
            add_branch_labels(child, clade or parent_clade)

    add_branch_labels(raw_tree["tree"])
    return stats


def main():
    if not OLD_WORK.exists():
        raise RuntimeError(f"Missing old work directory: {OLD_WORK}")
    if WORK.exists():
        shutil.rmtree(WORK)
    WORK.mkdir(parents=True)

    old_metadata_path = SOURCE_COMPANION / "metadata.tsv"
    if not old_metadata_path.exists():
        old_metadata_path = OLD_WORK / "metadata.tsv"
    old_metadata = load_tsv(old_metadata_path)
    wanted = [row["accession"] for row in old_metadata]
    wanted_set = set(wanted)
    clade_by_accession = {row["accession"]: row["clade"] for row in old_metadata}

    aligned_records = read_fasta(CHINA_ROOT / "ChinaPEDVS.fas")
    aligned_by_accession = {accession_from_header(header): (header, seq) for header, seq in aligned_records}
    if REFERENCE_ACCESSION not in aligned_by_accession:
        raise RuntimeError(f"Reference {REFERENCE_ACCESSION} not found in ChinaPEDVS.fas")
    missing = sorted(wanted_set - set(aligned_by_accession))
    if missing:
        raise RuntimeError(f"Accessions missing from ChinaPEDVS.fas: {missing[:20]}")

    reference_header, reference_aligned = aligned_by_accession[REFERENCE_ACCESSION]
    keep_columns = [index for index, base in enumerate(reference_aligned) if base != "-"]
    reference_sequence = "".join(reference_aligned[index] for index in keep_columns)
    alignment_records = []
    for accession in wanted:
        _, aligned = aligned_by_accession[accession]
        alignment_records.append((accession, "".join(aligned[index] for index in keep_columns)))

    source_unaligned = OLD_WORK / "sequences_unaligned.fasta"
    if not source_unaligned.exists():
        source_unaligned = SOURCE_COMPANION / "pedv_s_examples.fasta"
    if not source_unaligned.exists():
        raise RuntimeError("Missing unaligned source FASTA for examples and supplementary output")

    source_tree = SOURCE_COMPANION / "tree.nwk"
    if not source_tree.exists():
        source_tree = OLD_WORK / "tree.nwk"
    shutil.copy2(source_tree, WORK / "tree.nwk")
    shutil.copy2(source_unaligned, WORK / "sequences_unaligned.fasta")
    write_tsv(WORK / "metadata.tsv", old_metadata, ["strain", "accession", "clade"])
    source_label_rows = [
        {"accession": accession, "clade": clade}
        for accession, clade in sorted(clade_by_accession.items())
    ]
    write_tsv(WORK / "source_clade_labels.tsv", source_label_rows, ["accession", "clade"])
    write_fasta(WORK / "alignment_refcoords.fasta", alignment_records)
    write_fasta(WORK / "reference_aj1102.fasta", [(REFERENCE_NAME, reference_sequence)])
    gff = (
        "##gff-version 3\n"
        f"##sequence-region {REFERENCE_NAME} 1 {len(reference_sequence)}\n"
        f"{REFERENCE_NAME}\tPEDV-S\tgene\t1\t{len(reference_sequence)}\t.\t+\t.\tID=gene-S;Name=S;gene=S\n"
        f"{REFERENCE_NAME}\tPEDV-S\tCDS\t1\t{len(reference_sequence)}\t.\t+\t0\tID=S;Parent=gene-S;Name=S;gene=S;product=spike protein\n"
    )
    (WORK / "genome_annotation.gff3").write_text(gff, encoding="utf-8", newline="\n")

    run([
        "docker", "run", "--rm",
        "-v", f"{WORK.as_posix()}:/work",
        "nextstrain/base",
        "augur", "ancestral",
        "--tree", "/work/tree.nwk",
        "--alignment", "/work/alignment_refcoords.fasta",
        "--root-sequence", "/work/reference_aj1102.fasta",
        "--inference", "joint",
        "--output-node-data", "/work/nt_muts.json",
        "--output-sequences", "/work/ancestral_sequences.fasta",
    ])
    run([
        "docker", "run", "--rm",
        "-v", f"{WORK.as_posix()}:/work",
        "nextstrain/base",
        "augur", "translate",
        "--tree", "/work/tree.nwk",
        "--ancestral-sequences", "/work/nt_muts.json",
        "--reference-sequence", "/work/genome_annotation.gff3",
        "--genes", "S",
        "--output-node-data", "/work/aa_muts.json",
        "--alignment-output", "/work/translated_%GENE.fasta",
    ])
    run([
        "docker", "run", "--rm",
        "-v", f"{WORK.as_posix()}:/work",
        "nextstrain/base",
        "augur", "export", "v2",
        "--tree", "/work/tree.nwk",
        "--node-data", "/work/nt_muts.json", "/work/aa_muts.json",
        "--output", "/work/tree_raw.json",
        "--include-root-sequence-inline",
        "--validation-mode", "warn",
    ])

    raw_tree = json.loads((WORK / "tree_raw.json").read_text(encoding="utf-8"))
    raw_tree["meta"]["title"] = DATASET_TITLE
    raw_tree["meta"]["updated"] = "2026-05-14"
    raw_tree["meta"]["display_defaults"] = {
        "color_by": "clade_membership",
        "distance_measure": "div",
        "layout": "radial",
        "branch_label": "clade",
        "map_triplicate": False,
        "transmission_lines": False,
    }
    raw_tree["meta"]["genome_annotations"] = {
        "S": {"start": 1, "end": len(reference_sequence), "strand": "+", "type": "CDS"},
        "nuc": {"start": 1, "end": len(reference_sequence), "strand": "+", "type": "source"},
    }
    raw_tree["meta"]["colorings"] = [
        {"key": "clade_membership", "title": "Clade", "type": "categorical", "scale": [[k, v] for k, v in CLADE_COLORS.items()]},
        {"key": "clade_display", "title": "Clade label", "type": "categorical", "scale": [[k, v] for k, v in CLADE_COLORS.items()]},
        {"key": "pedv_genotype", "title": "PEDV genotype", "type": "categorical", "scale": [[k, v] for k, v in CLADE_COLORS.items()]},
        {"key": "num_date", "title": "Sampling date", "type": "continuous"},
        {"key": "collection_date", "title": "Collection date", "type": "categorical"},
        {"key": "host", "title": "Host", "type": "categorical"},
    ]
    raw_tree["meta"]["filters"] = ["clade_membership", "clade_display", "pedv_genotype", "collection_date", "host"]
    raw_tree["meta"]["panels"] = ["tree", "entropy"]

    old_tip_attrs = load_old_tip_attrs()
    stats = annotate_tree(raw_tree, clade_by_accession, old_tip_attrs)

    if DATASET.exists():
        shutil.rmtree(DATASET)
    DATASET.mkdir(parents=True)
    if SUPPLEMENTARY.exists():
        shutil.rmtree(SUPPLEMENTARY)
    SUPPLEMENTARY.mkdir(parents=True)

    write_fasta(DATASET / "reference.fasta", [(REFERENCE_NAME, reference_sequence)])
    (DATASET / "genome_annotation.gff3").write_text(gff, encoding="utf-8", newline="\n")
    (DATASET / "tree.json").write_text(json.dumps(raw_tree, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    pathogen = {
        "schemaVersion": "3.0.0",
        "attributes": {
            "name": DATASET_TITLE,
            "reference name": REFERENCE_NAME,
            "biological reference": f"{REFERENCE_ACCESSION} {REFERENCE_STRAIN} spike",
            "gene": "S",
            "organism": "Porcine epidemic diarrhea virus",
            "dataset source": "China GenBank PEDV S isolates",
        },
        "cdsOrderPreference": ["S"],
        "files": {
            "reference": "reference.fasta",
            "pathogenJson": "pathogen.json",
            "genomeAnnotation": "genome_annotation.gff3",
            "treeJson": "tree.json",
        },
        "qc": {
            "missingData": {"enabled": True, "missingDataThreshold": 300.0, "scoreBias": 10.0},
            "mixedSites": {"enabled": True, "mixedSitesThreshold": 20, "scoreBias": 5.0},
            "privateMutations": {
                "enabled": True,
                "typical": 80.0,
                "cutoff": 160.0,
                "weightReversionSubstitutions": 1.0,
                "weightLabeledSubstitutions": 1.0,
                "weightUnlabeledSubstitutions": 1.0,
            },
            "snpClusters": {"enabled": False},
            "frameShifts": {"enabled": True, "scoreBias": 20.0},
            "stopCodons": {"enabled": True, "scoreBias": 75.0},
        },
        "alignmentParams": {"alignmentPreset": "default", "minLength": 3000},
    }
    (DATASET / "pathogen.json").write_text(json.dumps(pathogen, ensure_ascii=False, indent=2), encoding="utf-8")
    example_records = read_fasta(WORK / "sequences_unaligned.fasta")[:3]
    examples_dir = REPO / "examples"
    examples_dir.mkdir(exist_ok=True)
    write_fasta(examples_dir / "PEDV_S_example_queries.fasta", example_records)

    shutil.copy2(WORK / "metadata.tsv", SUPPLEMENTARY / "metadata.tsv")
    shutil.copy2(WORK / "source_clade_labels.tsv", SUPPLEMENTARY / "source_clade_labels.tsv")
    shutil.copy2(WORK / "tree.nwk", SUPPLEMENTARY / "tree.nwk")
    shutil.copy2(WORK / "alignment_refcoords.fasta", SUPPLEMENTARY / "alignment_refcoords_AJ1102.fasta")
    shutil.copy2(WORK / "reference_aj1102.fasta", SUPPLEMENTARY / "reference_AJ1102.fasta")
    shutil.copy2(WORK / "aa_muts.json", SUPPLEMENTARY / "aa_muts_AJ1102.json")
    shutil.copy2(WORK / "nt_muts.json", SUPPLEMENTARY / "nt_muts_AJ1102.json")
    write_tsv(SUPPLEMENTARY / "clade_assignments.tsv", old_metadata, ["strain", "accession", "clade"])
    root_counts = [summarize_child_clades(child) for child in raw_tree["tree"].get("children", [])]
    summary = {
        "reference_accession": REFERENCE_ACCESSION,
        "reference_strain": REFERENCE_STRAIN,
        "reference_header": reference_header,
        "reference_coordinate_length": len(reference_sequence),
        "source_alignment_length": len(reference_aligned),
        "removed_reference_gap_columns": len(reference_aligned) - len(reference_sequence),
        "filtered_sequence_records": len(old_metadata),
        "clade_counts": dict(Counter(row["clade"] for row in old_metadata)),
        "root_child_clade_counts": root_counts,
        **stats,
    }
    (SUPPLEMENTARY / "build_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    (SUPPLEMENTARY / "README.md").write_text(
        "# Supplementary files\n\n"
        "This directory contains clade assignments, the AJ1102-coordinate alignment, and Augur node-data files used to build the dataset.\n",
        encoding="utf-8",
        newline="\n",
    )

    for zip_path in REPO.glob("nextclade_dataset*.zip"):
        zip_path.unlink()
    zip_path = REPO / "nextclade_dataset_pedv_s_genbank_china_isolates.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in DATASET.rglob("*"):
            archive.write(path, path.relative_to(DATASET.parent))

    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
