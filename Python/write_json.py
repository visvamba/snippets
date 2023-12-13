import json

data = {
    'key1': 'value1'
}

json_str = json.dumps(data)

with open('jsondata.json', 'w') as outfile:
    outfile.write(json_str)