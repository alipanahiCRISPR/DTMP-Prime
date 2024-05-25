# DTMP-Prime
This repository includes the implementation of DTMP-Prime (Deep Transformer-based Model for Predicting Prime Editing Efficiency), a tool designed to predict PegRNA activity and PE efficiency. DTMP-Prime, based on the BERT, is a Bi-directional Transformer based model with multi-head attention layers. Please cite our paper if you use the models or codes. The repo is still actively under development, so please kindly report if there is any issue encountered.

Furthermore, we designed a novel encoding algorithm to encode PegRNA-DNA pairs. By incorporating a model with multi-head attention architecture in the embedding layer of DTMP-Prime, we can achieve the following aims: 

   1. Capture features related to the type and position of each nucleotide and K-mer separately in PegRNA or DNA sequences.
       
   2. Understand the relationship and correlation between each nucleotide and k-mer with other nucleotides and K-mers within the PegRNA or DNA sequences.
       
   3. Examine the relationship and correlation between each nucleotide and K-mer with other nucleotides and K-mers within the PegRNA and DNA sequences.
       
The combination of these features with the new encoding strategy has significantly enhanced the efficiency of DTMP-Prime in predicting off-target sites. Furthermore, the utilization of multi-head attention architecture has enabled our pre-trained model to be adaptable for various PE models and cell lines.

 In this package, we provide resources including source codes of the DTMP-Prime model, data process, train and evaluate different deep models, and visualization tools. This package is still under development, as more features will be included gradually.

## 1. Environment setup
We recommend you build a Python virtual environment with Anaconda. then download DNABERT (k_mere=6) or a light version of it named DistilBert. See the embedding section in our repo.

## 2. Data processing
we fine-tune DNABERT with our data, if you want to use DTMP-Prim, please process your data into the same format as DNABERT. Note that the sequences are in kmer format, so you will need to convert your sequences into that. Then use our encoding function. 

### 2.1 Input

Default values are:
```
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

### 2.2 Output

The top candidates are provided in topX_pegRNAs.csv. This is a rawX format file. The output folder contains:

    topX_pegRNAs.csv
    
## 3. Prediction
After the model is fine-tuned, you can get predictions by running PE score. 

## 4. Visualization
Visualization of DTMP-Prim consists of 3 steps. Calculate PE-efficiency score, attention scores, and Plot.


