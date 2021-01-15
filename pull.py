#!./env/bin/python
import requests
import time
import json
import os.path
from os import path

filepath = 'nasa_ids'
with open(filepath) as fp:
    for cnt, line in enumerate(fp):
        line =line.strip()
        asset_url = "https://images-api.nasa.gov/asset/{id}".format(id=line)
        metadata_url = "https://images-assets.nasa.gov/image/{id}/metadata.json".format(id=line)

        # Check that file doesn't already exist
        image_exists = False
        for file_name in os.listdir('./images'):
            if file_name.startswith(line):
                image_exists = True
        json_exists = False
        for file_name in os.listdir('./images/json'):
            if file_name.startswith(line):
                json_exists = True

        print("Checking {id}".format(id=line))

        if not json_exists:
            metadata = requests.get(metadata_url)

            metadata_filepath = "images/json/{id}.json".format(id=line)
            if metadata.status_code==200:
                metadata_file = open(metadata_filepath,"wb")
                metadata_file.write(metadata.content)
                metadata_file.close()
                time.sleep(1)
            else:
                print(metadata.status_code)
                raise Exception

            with open(metadata_filepath) as f:
                metadata_json = json.load(f)
        else:
            print("{id} json already downloaded, skipping".format(id=line))

        if not image_exists:
            asset = requests.get(asset_url)

            if asset.status_code==200:
                asset_json = asset.json()
                image_url = asset_json["collection"]["items"][0]["href"]
                time.sleep(1)
            else:
                print(asset.status_code)
                raise Exception

            ext = image_url.split('.')[-1]

            image_filepath = "images/{id}.{extension}".format(id=line,extension="{extension}")

            if not path.exists(image_filepath.format(extension=ext)):
                response = requests.get(image_url.format(extension=ext))
                if response.status_code==200:
                        image_file=open(image_filepath.format(extension=ext),"wb")
                        image_file.write(response.content)
                        image_file.close()
                        time.sleep(3)
                else:
                    print(response.status_code)
                    raise Exception
            else:
                print("File already downloaded")
        else:
            print("{id} image already downloaded, skipping".format(id=line))

