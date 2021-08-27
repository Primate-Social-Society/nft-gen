import os
import json

f = open('./data.json',) 
data = json.load(f)

RUN_NAME = data['runName']

try:
  os.makedirs(f'./build/{RUN_NAME}/metadata')
except: 
  print('RUN_NAME metadata directory already exists')

IMAGES_BASE_URI = data['baseUrl']
PROJECT_NAME = data['projectName']

#### Generate Metadata for each Image    
f = open(f'./build/{RUN_NAME}/all-traits.json',) 
metadata = json.load(f)

def getAttribute(key, value):
  return {
    "trait_type": key,
    "value": value
  }
    
for i in metadata:
  token_id = i['tokenId']

  token = {
    "image": IMAGES_BASE_URI + str(token_id) + '.png',
    "tokenId": token_id,
    "name": PROJECT_NAME + ' #' + str(token_id),
    "attributes": []
  }

  for layer in data['layers']:
    token["attributes"].append(getAttribute(layer, i[layer]))

  with open(f'./build/{RUN_NAME}/metadata/{str(token_id)}', 'w') as outfile:
    json.dump(token, outfile, indent=4)
    
f.close()