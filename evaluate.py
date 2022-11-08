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

    total_acc_test = 0
    with torch.no_grad():
        for test_input, test_label in test_dataloader:
              test_label = test_label.to(device)
              mask = test_input['attention_mask'].to(device)
              input_id = test_input['input_ids'].squeeze(1).to(device)
              output = model(input_id, mask)
              acc = (output.argmax(dim=1) == test_label).sum().item()
              total_acc_test += acc   
    print(f'Test Accuracy: {total_acc_test / len(test_data): .3f}')



if __name__ == "__main__":
    con = sqlite3.connect('articles.db')
    cursorObj = con.cursor()
    def getData(query):
        data=cursorObj.execute(query) 
        res = data.fetchall()
        labels, texts = zip(*res)
        return pd.DataFrame({'type':labels, 'text':texts})

    print("Loading test dataset... ")
    title5 = getData("select type, title from test")
    head5 = getData("select type, head from test")
    title4 = getData("select type, title from test where not type = 'society'")
    head4 = getData("select type, head from test where not type = 'society'")
   
    print("Load Model title_5...")
    model = torch.load('./model/title_5.pt')
    print("Testing title_5...")
    test(model, title5)
    del model

    print("Load Model head_5...")
    model = torch.load('./model/head_5.pt')
    print("Testing head_5...")
    test(model, head5)
    del model

    print("Load Model title_4...")
    model = torch.load('./model/title_4.pt')
    print("Testing title4...")
    test(model, title4)
    del model

    print("Load Model head_4...")
    model = torch.load('./model/head_4.pt')
    print("Testing head_4...")
    test(model, head4)
    del model