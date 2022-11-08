import torch
import numpy as np
from transformers import BertTokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
from opencc import OpenCC

cc = OpenCC('t2s')# 繁轉簡

types = {'finance':0, 'global':1, 'star':2, 'sport':3, 'society':4}

class Dataset(torch.utils.data.Dataset):
    def __init__(self, data):
        self.labels = [types[label] for label in data['type']]
        self.texts = [tokenizer(cc.convert(text), 
                                padding='max_length', 
                                max_length = 512, 
                                truncation=True,
                                return_tensors="pt") 
                      for text in data['text']]

    def classes(self):
        return self.labels

    def __len__(self):
        return len(self.labels)

    def get_batch_labels(self, idx):
        # Fetch a batch of labels
        return np.array(self.labels[idx])

    def get_batch_texts(self, idx):
        # Fetch a batch of inputs
        return self.texts[idx]

    def __getitem__(self, idx):
        batch_texts = self.get_batch_texts(idx)
        batch_y = self.get_batch_labels(idx)
        return batch_texts, batch_y