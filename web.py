from flask import Flask, render_template, request
import torch
import torch
from transformers import BertTokenizer
from opencc import OpenCC

app = Flask(__name__)

model_name = "head_5"
model = torch.load(f"./models/{model_name}.pt", map_location=torch.device('cpu'))
cc = OpenCC('t2s')
tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
types = ['財經(finance)', '國際(global)', '娛樂(star)', '體育(sport)', '社會(society)']

@app.route("/")
def classify():
    return render_template("index.html")

@app.route("/api", methods=['POST'])
def hello():
    text = request.values['text']
    test_input = tokenizer(cc.convert(text), 
                                    padding='max_length', 
                                    max_length = 512, 
                                    truncation=True,
                                    return_tensors="pt") 
    mask = test_input['attention_mask']
    input_id = test_input['input_ids'].squeeze(1)
    output = model(input_id, mask)
    acc = output.argmax(dim=1).int()
    res = dict()
    res['all'] = output.tolist()
    res['msg'] = types[acc]
    return res

app.run(debug=True)