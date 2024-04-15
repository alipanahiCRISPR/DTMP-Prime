!pip install virtualenv

!virtualenv vdnabert
!source /content/vdnabert/bin/activate
!source /content/vdnabert/bin/activate

!sudo apt-get update -y
!sudo apt-get install python3.6
# change alternatives
!sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1
# select python version
!sudo update-alternatives --config python3
# check python version
!python --version
# install pip for new python
!sudo apt-get install python3.6-distutils
!wget https://bootstrap.pypa.io/get-pip.py
!python get-pip.py
# upgrade pip
!sudo apt install python3-pip
!python -m pip install --upgrade pip
%cd /content/DNABERT/examples/vdnabert/bin/activate
!source /content/vdnabert/bin/activate
#!git clone https://github.com/jerryji1993/DNABERT
%cd DNABERT
!python3 -m pip install --editable .
%cd examples
!python3 -m pip install -r requirements.txt
!git clone https://github.com/NVIDIA/apex
%cd apex
!pip install -v --no-cache-dir --global-option="--cpp_ext" --global-option="--cuda_ext" ./
!git clone https://github.com/jerryji1993/DNABERT
!git clone https://github.com/woreom/dnabert
!git clone https://github.com/joanaapa/Distillation-DNABERT-Promoter
!pip install torch
!pip install pytorch
!pip install apex
!pip install biopy
!pip install transformers
!pip install scikit-learn
!pip install tensorboardX
!pip install transformers
!pip install tokenization_utils
!pip install pyfaidx
!pip install transformers
!pip install boto3
!pip install sentencepiece
!pip install neptune
!pip install sacremoses
!pip install decouple
%cd /content/dnabert/examples
!export KMER=6
!export MODEL_PATH=./ft/$KMER
!export DATA_PATH=sample_data/ft/$KMER
!export PREDICTION_PATH=./result/$KMER
!export MODEL_PATH=/content/dnabert/examples/6

!python my-finetune.py \
    --model_type dna \
    --tokenizer_name DNATokenizer \
    --model_name_or_path /content/dnabert/examples/6 \
    --task_name cola \
    --do_predict \
    --data_dir /content/dnabert/examples/sample_data/ft/6 \
    --max_seq_length 75 \
    --per_gpu_pred_batch_size=128   \
    --output_dir /content/dnabert/examples/6 \
    --predict_dir /content/dnabert/examples/sample_data/pre \
    --n_process 48
import torch
from transformers import BertModel, BertConfig

dir_to_pretrained_model = "xxx/xxx"

config = BertConfig.from_pretrained('https://raw.githubusercontent.com/jerryji1993/DNABERT/master/src/transformers/dnabert-config/bert-config-6/config.json')
tokenizer = DNATokenizer.from_pretrained('dna6')
model = BertModel.from_pretrained(dir_to_pretrained_model, config=config)

sequence = "AATCTA ATCTAG TCTAGC CTAGCA"
model_input = tokenizer.encode_plus(sequence, add_special_tokens=True, max_length=512)["input_ids"]
model_input = torch.tensor(model_input, dtype=torch.long)
model_input = model_input.unsqueeze(0)   # to generate a fake batch with batch size one

output = model(model_input)
%cd /content/Distillation-DNABERT-Promoter
import torch
from transformers import DistilBertForSequenceClassification

mymodel = DistilBertForSequenceClassification.from_pretrained('Peltarion/dnabert-distilbert')
!python run_distil.py \
    --train_data_file data/pretrain/sample_6_3k.txt \
    --output_dir models \
    --student_model_type distildna \
    --student_config_name src/transformers/dnabert-config/distilbert-config-6 \
    --teacher_name_or_path Path_to_pretrained_DNABERT \
    --mlm \
    --do_train \
    --alpha_ce 2 \
    --alpha_mlm 7 \
    --alpha_cos 1 \
    --per_gpu_train_batch_size 32 \
    --learning_rate 0.0004 \
    --logging_steps 500 \
    --save_steps 8000 \
    --num_train_epochs 2

!python run_finetune.py \
    --data_dir data/promoters/6mer \
    --output_dir models \
    --do_eval \
    --model_type minidnaprom \
    --model_name_or_path mymodel \
    --per_gpu_eval_batch_size 32
!python /content/Distillation-DNABERT-Promoter/run_distil.py\
      --output_dir models \
def init_student(teacher, student):

    prefix = "bert"

    s_params = dict(student.named_parameters())
    t_params = dict(teacher.named_parameters())

    for w in ["word_embeddings", "position_embeddings"]:
        s_params[f"distilbert.embeddings.{w}.weight"].data.copy_(t_params[f"{prefix}.embeddings.{w}.weight"].data)
    for w in ["weight", "bias"]:
        s_params[f"distilbert.embeddings.LayerNorm.{w}"].data.copy_(t_params[f"{prefix}.embeddings.LayerNorm.{w}"].data)

    std_idx = 0
    for teacher_idx in [0, 2, 4, 7, 9, 11]:
        for w in ["weight", "bias"]:
            s_params[f"distilbert.transformer.layer.{std_idx}.attention.q_lin.{w}"].data.copy_(t_params[
                f"{prefix}.encoder.layer.{teacher_idx}.attention.self.query.{w}"
            ].data)
            s_params[f"distilbert.transformer.layer.{std_idx}.attention.k_lin.{w}"].data.copy_(t_params[
                f"{prefix}.encoder.layer.{teacher_idx}.attention.self.key.{w}"
            ].data)
            s_params[f"distilbert.transformer.layer.{std_idx}.attention.v_lin.{w}"].data.copy_(t_params[
                f"{prefix}.encoder.layer.{teacher_idx}.attention.self.value.{w}"
            ].data)

            s_params[f"distilbert.transformer.layer.{std_idx}.attention.out_lin.{w}"].data.copy_(t_params[
                f"{prefix}.encoder.layer.{teacher_idx}.attention.output.dense.{w}"
            ].data)
            s_params[f"distilbert.transformer.layer.{std_idx}.sa_layer_norm.{w}"].data.copy_(t_params[
                f"{prefix}.encoder.layer.{teacher_idx}.attention.output.LayerNorm.{w}"
            ].data)

            s_params[f"distilbert.transformer.layer.{std_idx}.ffn.lin1.{w}"].data.copy_(t_params[
                f"{prefix}.encoder.layer.{teacher_idx}.intermediate.dense.{w}"
            ].data)
            s_params[f"distilbert.transformer.layer.{std_idx}.ffn.lin2.{w}"].data.copy_(t_params[
                f"{prefix}.encoder.layer.{teacher_idx}.output.dense.{w}"
            ].data)
            s_params[f"distilbert.transformer.layer.{std_idx}.output_layer_norm.{w}"].data.copy_(t_params[
                f"{prefix}.encoder.layer.{teacher_idx}.output.LayerNorm.{w}"
            ].data)
        std_idx += 1


mymodel
