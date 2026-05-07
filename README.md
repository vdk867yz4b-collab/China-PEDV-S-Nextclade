# China PEDV S Nextclade Dataset

This repository provides a community Nextclade dataset for genotyping porcine epidemic diarrhea virus(PEDV)spike(S)gene sequences from GenBank China isolates.

The current dataset was built from 2011 PEDV S sequences retained after removing recombinant sequences and records with unclear sampling information. It is intended for rapid placement of query PEDV S sequences into the reference tree and for assignment to the curated PEDV S genotypes used in this dataset.

## Use in Nextclade Web

Open this link:

<https://clades.nextstrain.org/?dataset-url=gh:Chengyan611/China-PEDV-S-Nextclade@main@/nextclade_dataset_pedv_s_genbank_china_isolates>

Or choose **Dataset URL** in Nextclade Web and enter:

```text
gh:Chengyan611/China-PEDV-S-Nextclade@main@/nextclade_dataset_pedv_s_genbank_china_isolates
```

Example query sequences are provided in:

```text
examples/PEDV_S_example_queries.fasta
```

## Dataset Contents

The Nextclade dataset is in:

```text
nextclade_dataset_pedv_s_genbank_china_isolates/
```

It contains:

- `pathogen.json`: Nextclade dataset configuration.
- `reference.fasta`: S-gene reference sequence used by the dataset.
- `genome_annotation.gff3`: S coding sequence annotation for amino acid translation and mutation display.
- `tree.json`: Auspice v2 tree with clade labels, date metadata, and nucleotide/S amino acid branch mutations.
- `sequences.fasta`: small example query FASTA file for testing the dataset.

Supplementary build and curation files are in:

```text
supplementary/
```

## Dataset Summary

| Item | Value |
| --- | --- |
| Virus | Porcine epidemic diarrhea virus |
| Gene | Spike(S) |
| Source | GenBank China PEDV S isolate sequences |
| Included sequences | 2011 |
| Biological reference | JN547228.1 CH/S spike |
| Dataset reference name | PEDV_S_ROOT |
| Rooting strategy | Internal branch containing G1a,G1b,and S-INDEL reference tips |
| Main clades | G1a,G1b,G2a,G2b,G2c,S-INDEL |

Validation against the curated source labels:

| Clade | Count |
| --- | ---: |
| G1a | 5 |
| G1b | 23 |
| G2a | 533 |
| G2b | 263 |
| G2c | 1073 |
| S-INDEL | 114 |
| Blank calls | 0 |
| Mismatches | 0 |

## Recommended Use

This dataset is suitable for:

- preliminary PEDV S genotype assignment;
- visual placement of query sequences in a curated PEDV S reference tree;
- inspection of nucleotide and S amino acid mutations;
- exploratory comparison of Chinese PEDV S sequences against the curated reference set.

This dataset is not a substitute for manual phylogenetic review when a query sequence is recombinant, incomplete, highly divergent, or contains extensive ambiguous bases or deletions.

## Maintenance Notes

When updating the dataset, maintain the same filtering rules unless a versioned release documents a change:

- include China PEDV S GenBank isolates with clear collection dates;
- remove known recombinant sequences;
- remove records with unclear sampling information;
- screen for sequence length, excessive ambiguous bases, frameshifts, and premature stop codons;
- recheck clade definitions after adding new sequences;
- verify that Nextclade Web displays the tree, nucleotide mutations, S amino acid mutations, entropy, clade coloring, and date coloring.

See `METHODS.md`, `QC_SUMMARY.md`, and `CHANGELOG.md` for reproducibility and version history.
