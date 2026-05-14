# Methods

## Source Data

The dataset was prepared from GenBank PEDV S gene sequences annotated as China isolates. The working reference set contains 2011 sequences after removal of recombinant sequences and records with unclear sampling information.

The biological reference sequence is GenBank `JX188454.1`, corresponding to the PEDV AJ1102 spike sequence. The dataset reference sequence is named `PEDV_S_AJ1102` in `reference.fasta`.

## Inclusion and Exclusion Criteria

Sequences were retained when they met the following criteria:

- PEDV spike(S)gene sequence;
- China isolate/source record;
- interpretable collection date;
- sequence suitable for S-gene alignment and downstream phylogenetic placement;
- not classified as recombinant in the working curation.

Sequences were excluded when they had unclear sampling information, known or suspected recombination, severe quality problems, or insufficient information for time-aware dataset construction.

## Alignment and Phylogenetic Processing

The curated sequences were aligned as PEDV S coding sequences. The reference coordinate system was rebuilt from the non-gap columns of `JX188454.1`(AJ1102), producing a 4158nt S reference coordinate. A reference tree was generated for the 2011-sequence reference set and rooted so that the G2 branch is separated from the G1/S-INDEL branches while retaining G1a,G1b,and S-INDEL in the tree.

The exported `tree.json` includes:

- tip metadata for clade and date visualization;
- nucleotide branch mutations;
- S amino acid branch mutations;
- S-gene annotation for amino acid mutation display and entropy visualization.

## Clade Curation

The dataset uses the curated PEDV S genotype labels:

- G1a
- G1b
- G2a
- G2b
- G2c
- S-INDEL

Clade labels were checked against the curated source assignment table. The current validation showed zero blank clade calls and zero mismatches against the source clade labels.

## Dataset Files

The Nextclade dataset directory contains the standard files needed by Nextclade Web:

- `pathogen.json`
- `reference.fasta`
- `genome_annotation.gff3`
- `tree.json`

Additional curation outputs are stored in `supplementary/`.

## Reproducibility

The repository stores the final dataset files, the supplementary curation tables, and the update script used to rebuild the AJ1102-reference dataset. The current build was generated with Docker image `nextstrain/base` using Augur 32.0.0 and validated with `nextstrain/nextclade:3.16.0`.
