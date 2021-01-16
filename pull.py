#!./env/bin/python
import requests
import time
import json
import os.path
from os import path

time_between_interactions = 1

filepath = 'nasa_ids'
with open(filepath) as fp:
    for nasa_id in fp:
        # Remove new line character from id
        nasa_id = nasa_id.strip()

        # Url formats for gathering photo info
        asset_url = "https://images-api.nasa.gov/asset/{nasa_id}".format(
            nasa_id=nasa_id)
        metadata_url = "https://images-assets.nasa.gov/image/{nasa_id}/metadata.json".format(
            nasa_id=nasa_id)

        # Check that files doesn't already exist
        image_exists = False
        for file_name in os.listdir('./images'):
            if file_name.startswith(nasa_id):
                image_exists = True
        json_exists = False
        for file_name in os.listdir('./images/json'):
            if file_name.startswith(nasa_id):
                json_exists = True

        print("Checking {nasa_id}".format(nasa_id=nasa_id))

        # Start by gathering metadata
        if not json_exists:
            metadata = requests.get(metadata_url)

            metadata_filepath = "images/json/{nasa_id}.json".format(
                nasa_id=nasa_id)

            if metadata.status_code == 200:
                metadata_file = open(metadata_filepath, "wb")
                metadata_file.write(metadata.content)
                metadata_file.close()
                print("{nasa_id} json gathered".format(nasa_id=nasa_id))
                time.sleep(time_between_interactions)
            else:
                print(metadata.status_code)
                raise Exception

            with open(metadata_filepath) as f:
                metadata_json = json.load(f)

        else:
            print("{nasa_id} json already downloaded, skipping".format(
                nasa_id=nasa_id))

        # Gather image
        if not image_exists:
            # First gets information on image url
            asset = requests.get(asset_url)

            if asset.status_code == 200:
                asset_json = asset.json()
                # Grab original size url
                image_url = asset_json["collection"]["items"][0]["href"]
                time.sleep(time_between_interactions)
            else:
                print(asset.status_code)
                raise Exception

            # Get extension from url for when image is saved
            ext = image_url.split('.')[-1]

            image_filepath = "images/{nasa_id}.{extension}".format(
                nasa_id=nasa_id, extension=ext)

            response = requests.get(image_url.format(extension=ext))
            if response.status_code == 200:
                print("{nasa_id} download started".format(nasa_id=nasa_id))
                image_file = open(image_filepath, "wb")
                image_file.write(response.content)
                image_file.close()
                print("{nasa_id} image gathered".format(nasa_id=nasa_id))
                time.sleep(time_between_interactions)
            else:
                print(response.status_code)
                raise Exception
        else:
            print("{nasa_id} image already downloaded, skipping".format(
                nasa_id=nasa_id))
