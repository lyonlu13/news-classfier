import torch
from torch import nn
from torch.optim import Adam
from tqdm import tqdm
from Dataset import Dataset
import os
os.environ['CUDA_LAUNCH_BLOCKING'] = "1"
import sqlite3
import pandas as pd
import numpy as np
from BertClassifier import BertClassifier

def train(model, train_data, val_data, learning_rate=1e-6, epochs=5):
    train, val = Dataset(train_data), Dataset(val_data)
    train_dataloader = torch.utils.data.DataLoader(train, shuffle=True)
    val_dataloader = torch.utils.data.DataLoader(val)
    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda" if use_cuda else "cpu")
    print("Use Cuda" if use_cuda else"Don't use Cuda")
    criterion = nn.CrossEntropyLoss()
    optimizer = Adam(model.parameters(), lr=learning_rate)

    if use_cuda:
      model = model.cuda()
      criterion = criterion.cuda()
    for epoch in range(epochs):
      total_acc = 0
      total_loss = 0
      count = 0
      for train_input, train_label in tqdm(train_dataloader):
        count+=1
        train_label = train_label.to(device)
        mask = train_input['attention_mask'].to(device)
        input_id = train_input['input_ids'].squeeze(1).to(device)
        output = model(input_id, mask)
        train_label = train_label.long()
        batch_loss = criterion(output, train_label)
        total_loss += batch_loss.item()
        acc = (output.argmax(dim=1) == train_label).sum().item()
        total_acc += acc
        model.zero_grad()
        batch_loss.backward()
        optimizer.step()

      total_acc = 0
      total_loss = 0
      with torch.no_grad():
        for val_input, val_label in val_dataloader:
          val_label = val_label.to(device)
          mask = val_input['attention_mask'].to(device)
          input_id = val_input['input_ids'].squeeze(1).to(device)
  
          output = model(input_id, mask)
          val_label = val_label.long()
          batch_loss = criterion(output, val_label)
          total_loss += batch_loss.item()
          
          acc = (output.argmax(dim=1) == val_label).sum().item()
          total_acc += acc
      
      print(
          f'''Epochs: {epoch + 1} {count}
        | Train Loss:  {total_loss / (len(train_data)): .3f} 
        | Train Accuracy:  {total_acc /  (len(train_data)): .3f} 
        | Val Loss:  {total_loss / (len(val_data)): .3f} 
        | Val Accuracy:  {total_acc / (len(val_data)): .3f}''')


if __name__ == "__main__":
    con = sqlite3.connect('articles.db')
    cursorObj = con.cursor()
    def getData(query):
        check=cursorObj.execute(query) 
        res = check.fetchall()
        labels, texts = zip(*res)
        df = pd.DataFrame({'type':labels, 'text':texts})
        return np.split(df.sample(frac=1, random_state=42), [int(.8*len(df))])
    print("Loading train dataset... ")
    title5_t, title5_v = getData("select type, title from train")
    head5_t, head5_v = getData("select type, head from train")
    title4_t, title4_v = getData("select type, title from train where not type = 'society'")
    head4_t, head4_v = getData("select type, head from train where not type = 'society'")

    print("Train classifier title_5...")
    model = BertClassifier(5)
    train(model, title5_t, title5_v)
    torch.save(model, "./model/title_5.pt")
    del model

    print("Train classifier head_5...")
    model = BertClassifier(5)
    train(model, head5_t, head5_v)
    torch.save(model, "./model/head_5.pt")
    del model

    print("Train classifier title_4...")
    model = BertClassifier(4)
    train(model, title4_t, title4_v)
    torch.save(model, "./model/title_4.pt")
    del model

    print("Train classifier head_4...")
    model = BertClassifier(4)
    train(model, head4_t, head4_v)
    torch.save(model, "./model/head_4.pt")
    del model