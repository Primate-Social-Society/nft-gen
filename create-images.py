import progressbar
import os
from PIL import Image
import random
import json

from multiprocessing.pool import ThreadPool as Pool
# from multiprocessing import Pool

pool_size = 10  # your "parallelness"

f = open(
    "./data.json",
)
data = json.load(f)

RUN_NAME = data["runName"]

try:
    os.makedirs(f"./build/{RUN_NAME}/images")
except:
    print("RUN_NAME images directory already exists")

f = open(
    f"./build/{RUN_NAME}/all-traits.json",
)
all_images = json.load(f)

bar = progressbar.ProgressBar(
    maxval=len(all_images),
    widgets=[progressbar.Bar("=", "[", "]"), " ", progressbar.Percentage()],
)
bar.start()


def worker(item, size, i):
    file_path = f'./build/{RUN_NAME}/images/{item["tokenId"]}.png'

    if os.path.exists(file_path):
        bar.update(i)
        return

    nft = Image.open("./traits/base.png")
    nft = nft.resize((size, size))

    for layer in data["layers"]:
        img_path = f"./traits/{layer}/{item[layer]}.png"

        if os.path.exists(img_path):
            img = Image.open(img_path)

            if "convert" in data and data["convert"] != "":
                img = img.convert(data["convert"])

            img = img.resize((size, size))
            nft.paste(img, (0, 0), img)

    nft.save(file_path)

    bar.update(i)


pool = Pool(pool_size)

i = 0
#### Generate Images
for item in all_images:
    i = i + 1
    pool.apply_async(
        worker,
        (
            item,
            data["outputSize"],
            i,
        ),
    )

pool.close()
pool.join()

bar.finish()
