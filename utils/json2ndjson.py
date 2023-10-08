import json

with open('./data/origins/train_en_ko.json', 'r') as f:
    dat = json.load(f)

lst = dat['data']

with open('./data/train/train_en_ko.ndjson', 'w') as f:
    for record in lst:
        f.write(json.dumps(record) + '\n')