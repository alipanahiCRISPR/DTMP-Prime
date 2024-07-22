# Encoding
# Encoding step 2 - this is to understand the effect of my encoding method!
import numpy as np

class Encoder:
    def __init__(self, seq_wt, seq_et, with_category = False, label = None, with_reg_val = False, value = None):
        tlen = 24
        self.seq_wt = "-" *(tlen-len(seq_wt)) +  seq_wt
        self.seq_et = "-" *(tlen-len(seq_et)) + seq_et
        self.encoded_dict_indel = {'A': [1, 0, 0, 0, 0], 'T': [0, 1, 0, 0, 0],
                                   'G': [0, 0, 1, 0, 0], 'C': [0, 0, 0, 1, 0], '_': [0, 0, 0, 0, 1], '-': [0, 0, 0, 0, 0]}
        self.direction_dict = {'A':5, 'G':4, 'C':3, 'T':2, '_':1}
        if with_category:
            self.label = label
        if with_reg_val:
            self.value = value
        self.encode_wt_ed()

    def encode_seq_wt(self):
        code_list = []
        encoded_dict = self.encoded_dict_indel
        sgRNA_bases = list(self.seq_wt)
        for i in range(len(sgRNA_bases)):
            if sgRNA_bases[i] == "N":
                sgRNA_bases[i] = list(self.off_seq)[i]
            code_list.append(encoded_dict[sgRNA_bases[i]])
        self.sgRNA_code = np.array(code_list)

    def encode_seq_et(self):
        code_list = []
        encoded_dict = self.encoded_dict_indel
        off_bases = list(self.seq_et)
        for i in range(len(off_bases)):
            code_list.append(encoded_dict[off_bases[i]])
        self.off_code = np.array(code_list)

    def encode_wt_ed(self):
        self.encode_seq_wt()
        self.encode_seq_et()
        on_bases = list(self.seq_wt)
        off_bases = list(self.seq_et)
        on_off_dim7_codes = []
        for i in range(len(on_bases)):
            diff_code = np.bitwise_or(self.sgRNA_code[i], self.off_code[i])
            on_b = on_bases[i]
            off_b = off_bases[i]
            if on_b == "N":
                on_b = off_b

            dir_code = np.zeros(2)
            if on_b == "-" or off_b == "-" or self.direction_dict[on_b] == self.direction_dict[off_b]:
                pass
            else:
                if self.direction_dict[on_b] > self.direction_dict[off_b]:
                    dir_code[0] = 1
                else:
                    dir_code[1] = 1
            on_off_dim7_codes.append(np.concatenate((diff_code, dir_code)))
        self.on_off_code = np.array(on_off_dim7_codes)



# checking the encoding
e = Encoder(seq_wt="AGCTGATTTTA", seq_et="CG_GTTTTTTG")
print(e.on_off_code)