# PEDV S Nextclade dataset

This repository contains a custom Nextclade dataset for PEDV spike (S) sequences.

The dataset is built from a 2011-sequence filtered PEDV S reference set. The filtered set was derived from the 2406-sequence source set after removing recombinant sequences and sequences with unclear sampling information. Clade labels are:

- G1a
- G1b
- G2a
- G2b
- G2c
- S-INDEL

## Use in Nextclade Web

After this repository is uploaded to GitHub, open:

```text
https://clades.nextstrain.org/?dataset-url=gh:OWNER/REPOSITORY@main@/nextclade_dataset_pedv_s_2011_clades
```

Replace `OWNER/REPOSITORY` with the GitHub repository path, for example:

```text
https://clades.nextstrain.org/?dataset-url=gh:your-name/PEDV-S-nextclade@main@/nextclade_dataset_pedv_s_2011_clades
```

Then upload unknown PEDV S sequences in FASTA format as query sequences.

## Dataset files

```text
nextclade_dataset_pedv_s_2011_clades/
  pathogen.json
  reference.fasta
  genome_annotation.gff3
  tree.json
```

## Notes

This dataset is intended for PEDV S sequences that are complete or near complete. Very short fragments, recombinant sequences, or sequences far outside the reference diversity may receive uncertain placements and should be interpreted together with QC metrics and tree position.
