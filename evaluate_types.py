import torch
from Dataset import Dataset
import sqlite3
import pandas as pd
import torch

def test(model, test_data):
    test = Dataset(test_data)
    test_dataloader = torch.utils.data.DataLoader(test, batch_size=1)
    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda" if use_cuda else "cpu")
    if use_cuda:
        model = model.cuda()
    total_acc = 0
    with torch.no_grad():
        for test_input, test_label in test_dataloader:
              test_label = test_label.to(device)
              mask = test_input['attention_mask'].to(device)
              input_id = test_input['input_ids'].squeeze(1).to(device)
              output = model(input_id, mask)
              acc = (output.argmax(dim=1) == test_label).sum().item()
              total_acc += acc   
    print(f"{total_acc}/{len(test_data)} {total_acc / len(test_data)}")

con = sqlite3.connect('articles.db')
cursorObj = con.cursor()
def getData(query):
   data=cursorObj.execute(query) 
   res = data.fetchall()
   labels, texts = zip(*res)
   return pd.DataFrame({'type':labels, 'text':texts})
print("Loading test dataset... ")


finance_d = getData("select type, head from test where type='finance'")
global_d = getData("select type, head from test where type='global'")
star_d = getData("select type, head from test where type='star'")
sport_d = getData("select type, head from test where type='sport'")
society_d = getData("select type, head from test where type='society'")


print("Load Model head_5...")
model = torch.load('./model/head_5.pt')
print("Testing Finance:")
test(model, finance_d)
print("Testing Global:")
test(model, global_d)
print("Testing Star:")
test(model, star_d)
print("Testing Sport:")
test(model, sport_d)
print("Testing Society:")
test(model, society_d)

del model