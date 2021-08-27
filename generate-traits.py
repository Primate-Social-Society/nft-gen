import os
from PIL import Image 
import random
import json

RUN_NAME = "1"

try:
  os.makedirs(f'./build/{RUN_NAME}')
except: 
  print('RUN_NAME build directory already exists')

f = open('./data.json',) 
data = json.load(f)

if 'weights' not in data:
  data['weights'] = {}

runData = {}

all_images = [] 

for layer in data['layers']:
  if layer not in data['weights']:
    data['weights'][layer] = {}

  runData[layer] = []
  
  for imagefile in os.listdir(f'./traits/{layer}'):
    runData[layer].append(os.path.splitext(imagefile)[0])
      
# A recursive function to generate unique image combinations
def create_new_image():
  new_image = {} #

  # For each trait category, select a random trait based on the weightings 
  for layer in data['layers']:
    if len(runData[layer]) == 0:
      continue

    weights = []

    for image in runData[layer]:
      if image in data['weights'][layer]:
        weights.append(float(data['weights'][layer][image]))
      else:
        weights.append(float(data['defaultWeight']))

    new_image [layer] = random.choices(runData[layer], weights)[0]
  
  if new_image in all_images:
    return create_new_image()
  else:
    return new_image
    
# Generate the unique combinations based on trait weightings
for i in range(data['numToGenerate']): 
  new_image = create_new_image()
  all_images.append(new_image)

# Returns true if all images are unique
def all_images_unique(all_images):
  seen = list()
  return not any(i in seen or seen.append(i) for i in all_images)

print("Are all images unique?", all_images_unique(all_images))

# Add token Id to each image
i = 0
for item in all_images:
  item["tokenId"] = i
  i = i + 1

# # Get Trait Counts
# background_count = {}
# for item in background:
#   background_count[item] = 0
    
# circle_count = {}
# for item in circle:
#   circle_count[item] = 0

# square_count = {}
# for item in square:
#   square_count[item] = 0

# for image in all_images:
#   background_count[image["Background"]] += 1
#   circle_count[image["Circle"]] += 1
#   square_count[image["Square"]] += 1
    
# print(background_count)
# print(circle_count)
# print(square_count)

#### Generate Metadata for all Traits 
with open(f'./build/{RUN_NAME}/all-traits.json', 'w') as outfile:
  json.dump(all_images, outfile, indent=4)