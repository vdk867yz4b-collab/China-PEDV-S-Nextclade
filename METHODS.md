# Methods

## Source Data

The dataset was prepared from GenBank PEDV S gene sequences annotated as China isolates. The working reference set contains 2011 sequences after removal of recombinant sequences and records with unclear sampling information.

The biological reference sequence is GenBank `JN547228.1`, corresponding to the PEDV CH/S spike sequence. The dataset reference sequence is named `PEDV_S_ROOT` in `reference.fasta`.

## Inclusion and Exclusion Criteria

Sequences were retained when they met the following criteria:

- PEDV spike(S)gene sequence;
- China isolate/source record;
- interpretable collection date;
- sequence suitable for S-gene alignment and downstream phylogenetic placement;
- not classified as recombinant in the working curation.

Sequences were excluded when they had unclear sampling information, known or suspected recombination, severe quality problems, or insufficient information for time-aware dataset construction.

## Alignment and Phylogenetic Processing

The curated sequences were aligned as PEDV S coding sequences. A reference tree was generated for the 2011-sequence reference set and rooted on the internal branch containing the G1a,G1b,and S-INDEL reference tips.

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
- `sequences.fasta`

Additional curation outputs are stored in `supplementary/`.

## Reproducibility

The repository stores the final dataset files and the supplementary curation tables used to document the build. For full reconstruction, rerun the local preparation and build scripts retained in the project workspace, then replace the versioned dataset directory in this repository.
