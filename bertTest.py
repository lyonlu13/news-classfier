
from transformers import BertTokenizer
from opencc import OpenCC

cc = OpenCC('t2s')# 繁轉簡
tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')

print(tokenizer(cc.convert("北漂族月花1.6萬PO記帳表 網揪一亮點大讚「這筆2000元」"), 
                                padding='max_length', 
                                max_length = 512, 
                                truncation=True,
                                return_tensors="pt") )
                     