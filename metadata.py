#!./env/bin/python
import coloredlogs
import piexif
import os
import json
import logging
import argparse
from dateutil.parser import parse
from PIL import Image
from datetime import datetime
from enum import Enum

coloredlogs.install(level=logging.ERROR)


class EXIF(Enum):
    IMAGE_DESCRIPTION = 270
    DOCUMENT_NAME = 269
    DATE_TIME_ORIGINAL = 36867


def zip_metadata(metadata_dir: str, image_dir: str):
    """From images in directory, checks metadata directory and updates image files with NASA metadata.

    Args:
        metadata_dir (str): metadata_dir Directory to gather metadata from 
        image_dir (str): image_dir Directory to gather images from
    """
    for image_file in os.listdir(image_dir):
        if '.' in image_file:
            logging.info(
                "Updating metadata for {file}".format(file=image_file))
            nasa_id = os.path.splitext(image_file)[0]

            image_filepath = '{dir}/{file}'.format(dir=image_dir,
                                                   file=image_file)
            image = Image.open(image_filepath)
            try:
                image_exif = piexif.load(image.info['exif'])
                logging.debug(
                    'Loaded {file} exif data'.format(file=image_file))
            except KeyError:
                logging.warning(
                    "Image {file} missing exif data, creating".format(
                        file=image_file))

                # Create empty exif
                image_exif = {}
                image_exif['0th'] = {}
                image_exif['Exif'] = {}

            # Read in metadata
            try:
                with open('{dir}/{nasa_id}.json'.format(
                        dir=metadata_dir, nasa_id=nasa_id)) as metadata_json:
                    metadata_data = json.load(metadata_json)
            except Exception:
                logging.error(
                    'Metadata missing for {file}'.format(file=image_file))
                metadata_data = {}

            for key, value in metadata_data.items():

                # Filter for only standard AVAIL keys
                if key.startswith('AVAIL'):
                    #logging.debug('Checking tag {tag}'.format(tag=key))
                    key = key.split(':')[-1]

                    # Description tag
                    if key == 'Description':
                        logging.debug('Updating tag Description')
                        add_exif_data(image_exif, '0th',
                                      EXIF.IMAGE_DESCRIPTION,
                                      value.encode('utf-8'))
                    if key == 'Title':
                        logging.debug('Updating tag Title')
                        add_exif_data(image_exif, '0th', EXIF.DOCUMENT_NAME,
                                      value.encode('utf-8'))
                    if key == 'DateCreated':
                        logging.debug('Updating tag DateCreated')
                        try:
                            date = datetime.strptime(value, '%Y:%m:%d')
                        except Exception:
                            date = parse(value, fuzzy=True)
                        new_date = date.strftime("%Y:%m:%d %H:%M:%S")
                        add_exif_data(image_exif, 'Exif',
                                      EXIF.DATE_TIME_ORIGINAL,
                                      new_date.encode('utf-8'))

            exif_dump = piexif.dump(image_exif)
            try:
                piexif.insert(
                    exif_dump, '{dir}/{file}'.format(dir=image_dir,
                                                     file=image_file))
            except piexif._exceptions.InvalidImageDataError:
                logging.error('oof no like you')


def add_exif_data(exif_data: str, exif_type: str, exif_key: EXIF, new_data):
    logging.debug('New data to add:\n' + str(new_data))
    # If description is not there, add it
    if exif_key.value not in exif_data[exif_type].keys():
        exif_data[exif_type][exif_key.value] = new_data
        logging.info('New {data} added'.format(data=exif_key))
    else:
        # Check if description there is the same
        if exif_data[exif_type][exif_key.value] == new_data:
            logging.info('{data} already correct'.format(data=exif_key))
        else:
            logging.warning(
                '{data} already there, skipping'.format(data=exif_key))


parser = argparse.ArgumentParser(
    description=
    'Add titles, descriptions, and original dates to image metadatas')
parser.add_argument('-i',
                    '--image-folder',
                    help="Directory with image files",
                    type=str,
                    default='./images')
parser.add_argument('-j',
                    '--json-folder',
                    help="Folder to read json metadata from",
                    type=str,
                    default='./images/json')
args = parser.parse_args()
zip_metadata(args.json_folder, args.image_folder)
