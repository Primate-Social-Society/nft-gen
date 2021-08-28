nft-gen

### Setup
`pip install -r requirements.txt` 

### Updates weights.xlsx with current images in traits

`python3 ./update-weights.py` - Fast
* This will create a default weights.xlsx if you don't have one. 
* You can just delete a row and if the image still exists it will repopulate that row with the `defaultWeight` defined in data.json. 
* If a row exists but not the image, a note will be added, but the row will remain.
* A backup is generated each run in the backups folder. Number in file name is `Year Month Day - Hour Minute Second`.
* If an exception is thrown while regenerating it, the backup will be restored.

### Creates list of nfts to generate

`python3 ./generate-traits.py` - Fast
* Will create build folder based on `runName` in data.json
* Randiomizes traits for all nfts desired.
* Generates amount based on `numToGenerate` in data.json
* Uses weights.xlsx and `defaultWeight` from data.json
* Only uses `layers` defined in data.json
* Uses order that `layers` are defined in data.json
* Removes any trait images found that match name found in `exempt` in data.json
* Creates `build/{runName}/all-traits.json` with all generated trait combonations
* Creates `build/{runName}/stats.json` with stats and data on run
* Creates `build/{runName}/stats.xlsx` with stats and data on run

### Creates images that were setup in generate-traits.py

`python3 ./create-images.py` - Really Slow
* Will create build image folder based on `runName` in data.json
* Parses `build/{runName}/all-traits.json` and generates `build/{runName}/images/{tokenId}.png` file for each
* Generates file resolution based on `outputSize` in data.json

### Splits nft data for OpenSea use that were setup in generate-traits.py

`python3 ./split-metadata.py` - Fastish
* Will create build metadata folder based on `runName` in data.json
* Parses `build/{runName}/all-traits.json` and generates `build/{runName}/metadata/{tokenId}` file for each
