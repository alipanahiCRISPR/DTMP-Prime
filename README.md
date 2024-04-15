# DTMP-Prime
#### We introduce DTMP-Prime (Deep Transformer-based Model for Predicting Prime Editing Efficiency), a tool designed to predict PegRNA activity and PE efficiency.DTMP-Prime,based on the BERT, is a Bi-directional Transformer based model with multi-head attention layers.
#### Furthermore, we designed a novel encoding algorithm to encode PegRNA-DNA pairs.By incorporating a model with multi-head attention architecture in the embedding layer of DTMP-Prime, we are able to achieve the following aims: 
#####        1) Capture features related to the type and position of each nucleotide and K-mer separately in PegRNA or DNA sequences.
#####        2) Understand the relationship and correlation between each nucleotide and k-mer with other nucleotides and K-mers within the PegRNA or DNA sequences.
#####        3) Examine the relationship and correlation between each nucleotide and K-mer with other nucleotides and K-mers within the PegRNA and DNA sequences.
### The combination of these features with the new encoding strategy has significantly enhanced the efficiency of DTMP-Prime in predicting off-target sites. Furthermore, the utilization of multi-head attention architecture has enabled our pre-trained model to be adaptable for various PE models and cell lines.

