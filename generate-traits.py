import os
from PIL import Image
import random
import json
import pandas as pd

from exceptions import should_exclude_image

f = open(
    "./data.json",
)
data = json.load(f)

if "fileTypes" not in data:
    data["fileTypes"] = [".png"]

RUN_NAME = data["runName"]

try:
    os.makedirs(f"./build/{RUN_NAME}")
except:
    print("RUN_NAME build directory already exists")

prevWeights = {}

for layer in data["layers"]:
    try:
        prevWeights[layer] = pd.read_excel(
            "./weights.xlsx", sheet_name=layer, index_col=0, engine="openpyxl"
        ).to_dict()
    except:
        prevWeights[layer] = {}

    if "Weights" not in prevWeights[layer]:
        prevWeights[layer]["Weights"] = {}

# Load run specific data
runData = {}

for layer in data["layers"]:
    runData[layer] = {"images": [], "counts": {"Total": 0}, "percents": {"Total": 1.0}}

    runData[layer]["weights"] = prevWeights[layer]["Weights"]

    for imagefile in os.listdir(f"./traits/{layer}"):
        imageName = os.path.splitext(imagefile)[0]
        fileType = os.path.splitext(imagefile)[1]

        if fileType not in data["fileTypes"] or imageName in data["exempt"]:
            continue

        runData[layer]["images"].append(imageName)
        runData[layer]["counts"][imageName] = 0

# A recursive function to generate unique image combinations
def create_new_image():
    new_image = {}  #

    # For each trait category, select a random trait based on the weightings
    for layer in data["layers"]:
        if len(runData[layer]) == 0:
            continue

        weights = []
        images = []

        for image in runData[layer]["images"]:
            if should_exclude_image(data["exceptions"], new_image, layer, image):
                continue

            images.append(image)
            if image in runData[layer]["weights"]:
                weights.append(float(runData[layer]["weights"][image]))
            else:
                runData[layer]["weights"][image] = data["defaultWeight"]
                weights.append(float(data["defaultWeight"]))

        runData[layer]["weights"]["Total"] = sum(weights)

        new_image[layer] = random.choices(images, weights)[0]

    if new_image in all_images:
        return create_new_image()
    else:
        return new_image


all_images = []

# Generate the unique combinations based on trait weightings
for i in range(data["numToGenerate"]):
    new_image = create_new_image()
    new_image["tokenId"] = i
    all_images.append(new_image)

#### Generate Stats for all Traits
for image in all_images:
    for layer in data["layers"]:
        runData[layer]["counts"][image[layer]] += 1
        runData[layer]["counts"]["Total"] += 1

for layer in data["layers"]:
    total = runData[layer]["counts"]["Total"]
    for image in runData[layer]["counts"]:
        if image != "Total":
            runData[layer]["percents"][image] = runData[layer]["counts"][image] / total

with open(f"./build/{RUN_NAME}/stats.json", "w") as outfile:
    json.dump(runData, outfile, indent=4)

writer = pd.ExcelWriter(f"./build/{RUN_NAME}/stats.xlsx", engine="xlsxwriter")

countFormat = writer.book.add_format({"num_format": "#,##0"})
percentFormat = writer.book.add_format({"num_format": "0%"})
weightFormat = writer.book.add_format({"num_format": "#,##0.00"})

sheet = writer.book.add_worksheet("Stats")
writer.sheets["Stats"] = sheet

sheet.set_column("A:A", 20, None)
sheet.set_column("B:B", 10, countFormat)
sheet.set_column("C:C", 10, percentFormat)
sheet.set_column("D:D", 10, weightFormat)

rows = 1

for layer in data["layers"]:
    sheet.write(f"A{rows}", layer)
    df = pd.DataFrame(
        {
            "Counts": runData[layer]["counts"],
            "Percents": runData[layer]["percents"],
            "Weights": runData[layer]["weights"],
        }
    )
    df.to_excel(writer, sheet_name="Stats", startrow=rows, startcol=0)
    rows += len(runData[layer]["counts"]) + 3

writer.save()

#### Generate Metadata for all Traits
with open(f"./build/{RUN_NAME}/all-traits.json", "w") as outfile:
    json.dump(all_images, outfile, indent=4)
