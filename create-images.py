import progressbar
import os
from PIL import Image 
import random
import json
# from multiprocessing.pool import ThreadPool as Pool
from multiprocessing import Pool

pool_size = 10  # your "parallelness"
RUN_NAME = "1"

try:
  os.makedirs(f'./build/{RUN_NAME}/images')
except: 
  print('RUN_NAME images directory already exists')

f = open('./data.json',) 
data = json.load(f)

f = open(f'./build/{RUN_NAME}/all-traits.json',) 
all_images = json.load(f)

bar = progressbar.ProgressBar(maxval=len(all_images), \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
bar.start()

def worker(item, i):
  file_path = f'./build/{RUN_NAME}/images/{item["tokenId"]}.png'

  if os.path.exists(file_path):
    bar.update(i)
    return

  nft = Image.open('./traits/base.png')

  for layer in data['layers']:
    img = Image.open(f'./traits/{layer}/{item[layer]}.png')
    nft.paste(img, (0,0), img)

  nft.save(file_path)

  bar.update(i)

pool = Pool(pool_size)

i = 0
#### Generate Images    
for item in all_images:
  i = i + 1
  pool.apply_async(worker, (item,i,))

pool.close()
pool.join()

bar.finish()