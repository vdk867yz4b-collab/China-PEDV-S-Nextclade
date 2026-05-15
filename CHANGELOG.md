# Changelog

## v1.2.0 - 2026-05-15

Added Nextstrain/Auspice genotype dynamics support.

Changes:

- added `auspice/china_pedv_s_genbank_tip-frequencies.json` for the Auspice frequency-over-time panel;
- added `auspice/china_pedv_s_genbank.json` as the Nextstrain/Auspice display copy;
- added genotype-level `pedv_genotype` stream labels for streamtree visualization;
- updated the default Auspice view to rectangular time layout colored by PEDV genotype, without automatically enabling streamtree;
- enabled `tree`, `frequencies`, and `entropy` panels in `tree.json`;
- added reproducible frequency/streamtree helper script and metadata table.

## v1.1.0 - 2026-05-14

Updated the dataset reference sequence from the G1 reference `JN547228.1` to the G2 reference `JX188454.1`(AJ1102).

Changes:

- rebuilt the reference coordinate system from AJ1102 non-gap columns(4158nt);
- retained G1a,G1b,S-INDEL,G2a,G2b,and G2c in the reference tree;
- rooted the tree so the G2 branch is separated from G1/S-INDEL branches;
- regenerated nucleotide and S amino acid branch mutations with Augur;
- removed undeclared example files from the dataset directory and moved examples to `examples/`;
- validated the dataset with `nextstrain/nextclade:3.16.0`.

Dataset summary:

- 2011 curated GenBank China PEDV S sequences;
- biological reference `JX188454.1`(AJ1102);
- clades G1a,G1b,G2a,G2b,G2c,and S-INDEL;
- zero blank clade calls in the reference tree.

## v1.0.0 - 2026-05-07

Initial curated GitHub release for the China PEDV S Nextclade dataset.

Added repository-level documentation and supplementary materials without modifying the existing core dataset files:

- expanded `README.md`;
- added `METHODS.md`;
- added `QC_SUMMARY.md`;
- added `CITATION.cff`;
- added dataset-specific `README.md`;
- added example query FASTA;
- added supplementary metadata, clade assignments, source clade labels, Newick tree, and build summaries.

Dataset summary:

- 2011 curated GenBank China PEDV S sequences;
- biological reference `JN547228.1`;
- clades G1a,G1b,G2a,G2b,G2c,and S-INDEL;
- zero blank clade calls and zero mismatches against curated source labels.
