# DTMP-Prime 🧬

Welcome to the DTMP-Prime repository! This repository contains the implementation of DTMP-Prime (Deep Transformer-based Model for Predicting Prime Editing Efficiency), a cutting-edge tool designed to predict PegRNA activity and PE efficiency.

DTMP-Prime leverages the power of BERT, a Bi-directional Transformer-based model with multi-head attention layers. If you use our models or codes, please cite our paper. As the repository is still under active development, we appreciate any reports of issues you encounter.

### Architecture 🧱

![architecture](/Figures/graphical%20abstract%202-2.jpg)

### Steps 🪜

![Steps to achieve the accuracy](/Figures/2-2.jpg)

### Novel Encoding Algorithm 🚀

We have designed an innovative encoding algorithm to encode PegRNA-DNA pairs. This, combined with our multi-head attention architecture in the embedding layer of DTMP-Prime, achieves the following:

1. **Capture Features:** Identifies the type and position of each nucleotide and K-mer in PegRNA or DNA sequences.
2. **Understand Relationships:** Analyzes the relationships and correlations between nucleotides and K-mers within PegRNA or DNA sequences.
3. **Examine Correlations:** Studies the interactions between nucleotides and K-mers within both PegRNA and DNA sequences.

These features, alongside our new encoding strategy, significantly enhance DTMP-Prime's efficiency in predicting off-target sites. Moreover, the multi-head attention architecture allows our pre-trained model to adapt to various PE models and cell lines.

## Resources Provided 📦

This package includes:

- Source codes of the DTMP-Prime model
- Data processing tools
- Training and evaluation scripts for different deep models
- Visualization tools

Please note that this package is still under development, with more features being added gradually.

---

## Environment Setup 🛠️

We recommend setting up a Python virtual environment using Anaconda. Then, download DNABERT (k_mere=6) or its lighter version, DistilBert. See the embedding section in our repository for more details.

---

## Data Processing 📊

We fine-tune DNABERT with our data. To use DTMP-Prime, please process your data into the same format as DNABERT. Note that sequences are in kmer format, so you will need to convert your sequences accordingly and then use our encoding function.

### Input 📥

Default values are:

```yaml
genome_fasta: /path/to/genome.fa
scaffold: GTTTTAGAGCTAGAAATAGCAAGTTAAAATAAGGCTAGTCCGTTATCAACTTGAAAAAGTGGCACCGAGTCGGTGC
debug: 0
n_jobs: 4
min_PBS_length: 8
max_PBS_length: 17
min_RTT_length: 10
max_RTT_length: 25
min_distance_RTT5: 3
max_ngRNA_distance: 100
max_target_to_sgRNA: 10
sgRNA_length: 20
offset: -3
PAM: NGG
```

### Output 📤

The top candidates are provided in `topX_pegRNAs.csv`. The output folder contains:

- `topX_pegRNAs.csv`

---

## Prediction 🔮

Once the model is fine-tuned, you can obtain predictions by running the PE score.

---

## Visualization 📈

Visualization of DTMP-Prime consists of three steps:

1. Calculate PE-efficiency score
2. Calculate attention scores
3. Generate plots

---

We hope you find DTMP-Prime useful for your research. If you have any questions or encounter any issues, please don't hesitate to contact us.
