import traceback
import math
import os
import json
import pandas as pd
import time
from shutil import copyfile

f = open(
    "./data.json",
)
data = json.load(f)

if "fileTypes" not in data:
    data["fileTypes"] = [".png"]

backupTime = time.strftime("%Y%m%d-%H%M%S")

prevWeights = {}

if os.path.exists("./weights.xlsx"):
    copyfile("./weights.xlsx", f"./backups/weights-{backupTime}.xlsx")

try:
    for layer in data["layers"]:
        try:
            prevWeights[layer] = pd.read_excel(
                "./weights.xlsx", sheet_name=layer, index_col=0, engine="openpyxl"
            ).to_dict()
        except:
            prevWeights[layer] = {}

        if "Weights" not in prevWeights[layer]:
            prevWeights[layer]["Weights"] = {}

        if "Notes" not in prevWeights[layer]:
            prevWeights[layer]["Notes"] = {}

            for imagefile in prevWeights[layer]["Weights"]:
                prevWeights[layer]["Notes"][imagefile] = ""

    writer = pd.ExcelWriter("./weights.xlsx", engine="xlsxwriter")

    countFormat = writer.book.add_format({"num_format": "#,##0.00"})

    for layer in data["layers"]:
        weights = {}
        for imagefile in os.listdir(f"./traits/{layer}"):
            imageName = os.path.splitext(imagefile)[0]
            fileType = os.path.splitext(imagefile)[1]

            if fileType not in data["fileTypes"] or imageName in data["exempt"]:
                continue

            if imageName in prevWeights[layer]["Weights"]:
                weights[imageName] = float(prevWeights[layer]["Weights"][imageName])
            else:
                weights[imageName] = float(data["defaultWeight"])

        notes = {}

        for imagefile in prevWeights[layer]["Notes"]:
            if not imagefile or pd.isna(imagefile) or pd.isnull(imagefile):
                continue

            if imagefile not in weights:
                notes[imagefile] = "Not Found"
                weights[imagefile] = prevWeights[layer]["Weights"][imagefile]
            else:
                notes[imagefile] = prevWeights[layer]["Notes"][imagefile]

        df = pd.DataFrame({"Weights": weights, "Notes": notes})
        df.to_excel(writer, sheet_name=layer)

        sheet = writer.sheets[layer]

        sheet.set_column("A:A", 20, None)
        sheet.set_column("B:B", 10, countFormat)
        sheet.set_column("C:C", 30, None)

    writer.save()
except Exception:
    traceback.print_exc()
    copyfile(f"./backups/weights-{backupTime}.xlsx", "./weights.xlsx")
