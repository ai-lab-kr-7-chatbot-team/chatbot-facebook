# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 20:16:08 2020

@author: UNIMAX
"""

# argparse 
import argparse
import torch
import pandas as pd
import numpy as np
import re
import torch.nn as nn
import os
#import torchtext
from kogpt2.pytorch_kogpt2 import get_pytorch_kogpt2_model
from gluonnlp.data import SentencepieceTokenizer
from kogpt2.utils import get_tokenizer

from flask import Flask,request


class Config(dict):
    __setattr__=dict.__setitem__
    __getattr__=dict.__getitem__
# 인자값을 받을 수 있는 인스턴스 생성
parser = argparse.ArgumentParser(description = 'chatbot & music')

class my_kogpt2_model(nn.Module):
    def __init__(self, config, model):
        super().__init__()
        self.config = config
        self.model = model
        self.classification = nn.Linear(self.config.n_vocab, self.config.cls)

    def inference(self,
               input_ids,
               ):
        pred=self.model.generate(input_ids=input_ids,eos_token_id=vocab['</s>'],bos_token_id = vocab['<usr>'], pad_token_id = config.padding_idx, decoder_start_token_id=vocab['<sys>'],do_sample=True, max_length=64, top_p=0.92, top_k=50, temperature=0.6, no_repeat_ngram_size=None, num_return_sequences=1, early_stopping=False)
        # input ids : 1, seq_len
        with torch.no_grad():
            model.eval()
            cls_position = input_ids.squeeze(0).tolist().index(config.cls_idx)
            output = self.model.forward(input_ids=input_ids)[0]
            cls_output = self.classification.forward(output[:,cls_position,:])
        return pred.squeeze().tolist(),cls_output.argmax(-1).item()

    def forward(self,data):
        input_ids = data[0]
        cls_position = data[1]
        #lm_label = data[-1]
        # batch size, seq len, n_vocab
        output = self.model.forward(input_ids=input_ids)[0]
        e=torch.cat([output[_,j,:].unsqueeze(0) for _,j in enumerate(cls_position.tolist())],0)
        cls_output = self.classification.forward(e)
        return output, cls_output


tok_path = get_tokenizer()
model, vocab = get_pytorch_kogpt2_model()
tokenizer = SentencepieceTokenizer(tok_path,  num_best=0, alpha=0)
config=Config({'cls':3,'unk_idx':vocab[vocab.unknown_token],'bos_idx':vocab[vocab.bos_token],'eos_idx':vocab[vocab.eos_token],'cls_idx':vocab['<unused0>'],'usr_idx':vocab['<usr>'],'sys_idx':vocab['<sys>'],'padding_idx':vocab[vocab.padding_token],'n_vocab':len(vocab), 'batch_size':2, 'max_len':64})
device='cpu'#'cuda' if torch.cuda.is_available() else 'cpu'
Model = my_kogpt2_model(config, model)
Model.to(device)
Model.load_state_dict(torch.load('./chatbot1_epoch_13',map_location=device))

# 입력 받을 인자 값 등록
'''
required True면 필수적으로 입력해야 됨. help 는 설명임
'''
parser.add_argument('--input',required=True, help = '말씀해주세요') 


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/bot')
def hello_world_bot():

    input_sentence = request.args.get('chat')
    #print(input_sentence)
    #print(tokenizer('안녕하세요'))
    toked = tokenizer(input_sentence)
    #print(toked)
    input_ids = torch.LongTensor([[vocab['<usr>']]+vocab[toked]+[vocab['<unused0>']]])
    pred, cls_output = Model.inference(input_ids.to(device))
    result=''
    start = pred.index(config.cls_idx)
    for i in pred[start+1:]:
        k = vocab.to_tokens(i)
        if k == '</s>':
            break
        result+=k.replace('▁',' ')
    print(result)

    return result



# 입력 받은 인자 값을 args에 저장
if __name__ == '__main__':
    args = parser.parse_args()
    input_sentence = args.input
    #print(input_sentence)
    #print(tokenizer('안녕하세요'))
    toked = tokenizer(input_sentence)
    #print(toked)
    input_ids = torch.LongTensor([[vocab['<usr>']]+vocab[toked]+[vocab['<unused0>']]])
    pred, cls_output = Model.inference(input_ids.to(device))
    result=''
    start = pred.index(config.cls_idx)
    for i in pred[start+1:]:
        k = vocab.to_tokens(i)
        if k == '</s>':
            break
        result+=k.replace('▁',' ')
    print(result)
#    if cls_output != 0:
#        playlist=pd.read_pickle('./play_list')
#        import random
#        r = random.choice(list(range(len(playlist))))
#        print('이런 노래 들으시면 어떨까요? %s'%(playlist.loc[r,cls_output]))
    
# 입력 받은 인자 값을 출력
