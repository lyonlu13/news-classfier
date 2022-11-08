import torch
from Dataset import Dataset
import pandas as pd
import torch
from transformers import BertTokenizer
from opencc import OpenCC

model_name = input("請輸入希望使用的判斷模型(未輸入則預設使用head_5)：")
model_name = "head_5" if(model_name=="") else model_name
model = torch.load(f"./model/{model_name}.pt")
cc = OpenCC('t2s')# 繁轉簡
tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')


types = ['財經(finance)', '國際(global)', '娛樂(star)', '體育(sport)', '社會(society)']


use_cuda = torch.cuda.is_available()
device = torch.device("cuda" if use_cuda else "cpu")
if use_cuda:
    model = model.cuda()

while(1):
    text = input("請輸入希望判斷的新聞：")
    test_input = tokenizer(cc.convert(text), 
                                    padding='max_length', 
                                    max_length = 512, 
                                    truncation=True,
                                    return_tensors="pt") 
    mask = test_input['attention_mask'].to(device)
    input_id = test_input['input_ids'].squeeze(1).to(device)
    output = model(input_id, mask)
    acc = output.argmax(dim=1).int()
    print(types[acc])