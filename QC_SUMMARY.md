# Quality Control Summary

## Current Version

| Field | Value |
| --- | --- |
| Dataset name | China PEDV S Nextclade Dataset |
| Dataset directory | `nextclade_dataset_pedv_s_genbank_china_isolates` |
| Source | GenBank China PEDV S isolate sequences |
| Final reference set | 2011 sequences |
| Biological reference | `JX188454.1`(AJ1102) |
| Dataset reference name | `PEDV_S_AJ1102` |
| Reference coordinate length | 4158 nt |
| Gene annotation | S |
| Rooting | Root placed so G2 is separated from G1/S-INDEL |

## Clade Counts

| Clade | Count |
| --- | ---: |
| G1a | 5 |
| G1b | 23 |
| G2a | 533 |
| G2b | 263 |
| G2c | 1073 |
| S-INDEL | 114 |
| Total | 2011 |

## Validation

| Check | Result |
| --- | --- |
| Tree tips | 2011 |
| Filtered sequence records | 2011 |
| Blank clade calls | 0 |
| Mismatches versus curated labels | 0 |
| S amino acid mutation data | Present |
| Entropy panel support | Present |
| Amino acid site coloring support | Present |
| Nextclade CLI validation | Passed with `nextstrain/nextclade:3.16.0` |

## Recommended Checks After Each Update

- Confirm that `pathogen.json`, `reference.fasta`, `genome_annotation.gff3`, and `tree.json` load in Nextclade Web.
- Upload `examples/PEDV_S_example_queries.fasta` and confirm that analysis completes.
- Confirm that the tree panel is visible.
- Confirm that nucleotide mutations and S amino acid mutations are displayed.
- Confirm that entropy is available for nucleotide and S amino acid sites.
- Confirm that clade, date, host, and genotype coloring options work.
- Recalculate clade counts and compare them against source labels.
- Inspect newly added sequences for recombination, long deletions, ambiguous bases, frameshifts, and stop codons.
