#!./env/bin/python
import requests
import time
import json
import glob
import logging
import argparse

logging.basicConfig(level=logging.DEBUG)

time_between_interactions = 1

def pull_images(id_file: str, image_folder: str, json_folder: str):
    with open(id_file) as fp:
        for nasa_id in fp:
            # Remove new line character from id
            nasa_id = nasa_id.strip()

            # Url formats for gathering photo info
            asset_url = "https://images-api.nasa.gov/asset/{nasa_id}".format(
                nasa_id=nasa_id)
            metadata_url = "https://images-assets.nasa.gov/image/{nasa_id}/metadata.json".format(
                nasa_id=nasa_id)

            # Check that files doesn't already exist
            image_exists = bool(
                glob.glob('{image_folder}/{id}.*'.format(
                    image_folder=image_folder, id=nasa_id)))
            json_exists = bool(
                glob.glob('{json_folder}/{id}.json'.format(
                    json_folder=json_folder, id=nasa_id)))

            logging.debug("Checking {nasa_id}".format(nasa_id=nasa_id))

            # Start by gathering metadata
            if not json_exists:
                metadata = requests.get(metadata_url)

                metadata_filepath = "{json_folder}/{nasa_id}.json".format(
                    json_folder=json_folder,nasa_id=nasa_id)

                if metadata.status_code == 200:
                    metadata_file = open(metadata_filepath, "wb")
                    metadata_file.write(metadata.content)
                    metadata_file.close()
                    logging.info(
                        "{nasa_id} json gathered".format(nasa_id=nasa_id))
                    time.sleep(time_between_interactions)
                else:
                    logging.error(
                        "Failed to download metadata for id {id}, received status code {code}"
                        .format(id=nasa_id, code=asset.status_code))
                    raise Exception

                with open(metadata_filepath) as f:
                    metadata_json = json.load(f)
            else:
                logging.info(
                    "{nasa_id} json already downloaded, skipping".format(
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
                    logging.error(
                        "Failed to download asset for id {id}, received status code {code}"
                        .format(id=nasa_id, code=asset.status_code))
                    raise Exception

                # Get extension from url for when image is saved
                ext = image_url.split('.')[-1]

                image_filepath = "{image_folder}/{nasa_id}.{extension}".format(
                    image_folder=image_folder,nasa_id=nasa_id, extension=ext)

                # Get and save the original size photo
                response = requests.get(image_url.format(extension=ext))
                if response.status_code == 200:
                    logging.debug(
                        "{nasa_id} download started".format(nasa_id=nasa_id))
                    image_file = open(image_filepath, "wb")
                    image_file.write(response.content)
                    image_file.close()
                    logging.info(
                        "{nasa_id} image gathered".format(nasa_id=nasa_id))
                    time.sleep(time_between_interactions)
                else:
                    logging.error(
                        "Failed to download image for id {id}, received status code {code}"
                        .format(id=nasa_id, code=asset.status_code))
                    raise Exception
            else:
                logging.info(
                    "{nasa_id} image already downloaded, skipping".format(
                        nasa_id=nasa_id))


parser = argparse.ArgumentParser(
    description='Pull images from NASA based on list of NASA id')
parser.add_argument('id_file', help="File to pull NASA ids from", type=str)
parser.add_argument('-i',
                    '--image-folder',
                    help="Folder to store images in",
                    type=str,
                    default='./images')
parser.add_argument('-j',
                    '--json-folder',
                    help="Folder to store json metadata in",
                    type=str,
                    default='./images/json')
args = parser.parse_args()
pull_images(args.id_file, args.image_folder, args.json_folder)
