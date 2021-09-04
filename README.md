# nft-gen

### Setup

`pip install -r requirements.txt`

### Updates weights.xlsx with current images in traits

`python3 ./update-weights.py` - Fast

- v0.1 - This will create a default weights.xlsx if you don't have one.
- v0.1 - You can just delete a row and if the image still exists it will repopulate that row with the `defaultWeight` defined in data.json.
- v0.1 - If a row exists but not the image, a note will be added, but the row will remain.
- v0.1 - A backup is generated each run in the backups folder. Number in file name is `Year Month Day - Hour Minute Second`.
- v0.1 - If an exception is thrown while regenerating it, the backup will be restored.

### Creates list of nfts to generate

`python3 ./generate-traits.py` - Fast

- v0.1 - Will create build folder based on `runName` in data.json
- v0.1 - Randiomizes traits for all nfts desired.
- v0.1 - Generates amount based on `numToGenerate` in data.json
- v0.1 - Uses weights.xlsx and `defaultWeight` from data.json
- v0.1 - Only uses `layers` defined in data.json
- v0.1 - Uses order that `layers` are defined in data.json
- v0.1 - Removes any trait images found that match name found in `exempt` in data.json
- v0.1 - Creates `build/{runName}/all-traits.json` with all generated trait combonations
- v0.1 - Creates `build/{runName}/stats.json` with stats and data on run
- v0.1 - Creates `build/{runName}/stats.xlsx` with stats and data on run
- v0.2 - Removes any trait images not found with one of the `fileTypes` in data.json (if this does not exist it defaults to only `.png` files). Must include the `.` with the extension fileType.

### Creates images that were setup in generate-traits.py

`python3 ./create-images.py` - Really Slow

- v0.1 - Will create build image folder based on `runName` in data.json
- v0.1 - Parses `build/{runName}/all-traits.json` and generates `build/{runName}/images/{tokenId}.png` file for each
- v0.1 - Generates file resolution based on `outputSize` in data.json
- v0.1 - Requires a `traits/base.png` file that is the same dimeninsions as the other files to work correctly. This is the very first layer of all images built.

### Splits nft data for OpenSea use that were setup in generate-traits.py

`python3 ./split-metadata.py` - Fastish

- v0.1 - Will create build metadata folder based on `runName` in data.json
- v0.1 - Parses `build/{runName}/all-traits.json` and generates `build/{runName}/metadata/{tokenId}` file for each
