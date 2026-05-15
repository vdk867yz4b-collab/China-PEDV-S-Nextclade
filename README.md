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

## Use in Nextstrain Auspice

The same tree can be viewed in Nextstrain/Auspice with genotype streamtree and genotype frequency-over-time panels:

<https://nextstrain.org/fetch/raw.githubusercontent.com/Chengyan611/China-PEDV-S-Nextclade/main/auspice/china_pedv_s_genbank.json?c=pedv_genotype&streamLabel=pedv_genotype>

The frequency panel is provided by the sidecar file:

```text
auspice/china_pedv_s_genbank_tip-frequencies.json
```

This sidecar filename intentionally matches the main Auspice tree filename. When the main file is `china_pedv_s_genbank.json`, Auspice looks for `china_pedv_s_genbank_tip-frequencies.json` in the same directory.

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

The Auspice display files are in:

```text
auspice/
```

It contains:

- `china_pedv_s_genbank.json`: Auspice v2 tree configured for genotype streamtree and frequency display.
- `china_pedv_s_genbank_tip-frequencies.json`: Auspice sidecar file for genotype frequency-over-time display.

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
| Biological reference | JX188454.1 AJ1102 spike |
| Dataset reference name | PEDV_S_AJ1102 |
| Reference coordinate length | 4158 nt |
| Rooting strategy | Root placed so the G2 branch is separated from G1/S-INDEL branches |
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
- exploratory genotype frequency-over-time visualization in Nextstrain/Auspice;
- streamtree visualization of PEDV S genotype structure;
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
