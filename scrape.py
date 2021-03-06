#!./env/bin/python
import requests
import time
import json
import argparse
import logging
import coloredlogs

coloredlogs.install()
time_between_interactions = 0.5

logging.basicConfig(level=logging.INFO)


def fetch_image_ids(query: str, start: int, end: int, min_links_to_fetch: int,
                    output_file: str):
    """Grab NASA ids from images.nasa.gov and save to file based on query.

    Args:
        query (str): query Query to search images for
        start (int): start Lower bound of year image was taken (inclusive)
        end (int): end Upper bound of year image was taken (inclusive)
        min_links_to_fetch (int): min_links_to_fetch Minimum links to grab. Will get at least this many, or how ever many images are in query.
        output_file (str): output_file Text file to put NASA ids into.
    """
    # Query Format
    search_url = "https://images-api.nasa.gov/search?q={query}&page={page}&media_type=image&year_start={start}&year_end={end}"

    # Starting page
    page = 1

    ids = []

    last_ids_len = -1

    # Goes until has more than max requested, or until there are no more ids
    while len(ids) < min_links_to_fetch and len(ids) != last_ids_len:
        last_ids_len = len(ids)

        # Gather page of ids from nasa
        response = requests.get(
            search_url.format(query=query, page=page, start=start, end=end))
        time.sleep(time_between_interactions)

        # Ensure data actually there
        if response.status_code == 200:
            response_json = response.json()

            if last_ids_len == 0:
                logging.info("Total hits: {hits}".format(
                    hits=response_json['collection']['metadata']
                    ['total_hits']))

            for item in response_json["collection"]["items"]:
                nasa_id = item["data"][0]["nasa_id"]
                ids.append(nasa_id)

            # Ensure no duplicates
            ids = list(set(ids))

            page = page + 1
            logging.info("{ids} collected.".format(ids=len(ids)))

        else:
            logging.error(
                'Failed to get page {page}. Received status {code}'.format(
                    page=page, code=response.status_code))
            raise Exception

    # Put ids in file
    with open(output_file, 'a') as f:
        for item in ids:
            f.write("%s\n" % item)


parser = argparse.ArgumentParser(
    description='Gather ids of NASA images based on query')
parser.add_argument('query', help="Query to search images with", type=str)
parser.add_argument('-n',
                    '--number-of-ids',
                    help="Max number of ids to retrieve",
                    type=int,
                    default=10000)
parser.add_argument('-s', '--start', help="Start year", type=int, default=1900)
parser.add_argument('-e', '--end', help="End Year", type=int, default=2050)
parser.add_argument('-o',
                    '--output',
                    help="Output file",
                    type=str,
                    default='nasa_id')
args = parser.parse_args()
fetch_image_ids(args.query, args.start, args.end, args.number_of_ids,
                args.output)
