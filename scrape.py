#!./env/bin/python
import requests
import time
import json
import argparse

time_between_interactions = 1


def fetch_image_ids(query: str, start: int, end: int, max_links_to_fetch: int):
    # Query Format
    search_url = "https://images-api.nasa.gov/search?q={query}&page={page}&media_type=image&year_start={start}&year_end={end}"

    # Starting page
    page = 1

    ids = []

    last_ids_len = -1

    # Goes until has more than max requested, or until there are no more ids
    while len(ids) < max_links_to_fetch and len(ids) != last_ids_len:
        last_ids_len = len(ids)

        # Gather page of ids from nasa
        response = requests.get(
            search_url.format(query=query, page=page, start=start, end=end))
        time.sleep(time_between_interactions)

        # Ensure data actually there
        if response.status_code == 200:
            response_json = response.json()

            for item in response_json["collection"]["items"]:
                nasa_id = item["data"][0]["nasa_id"]
                ids.append(nasa_id)

            # Ensure no duplicates
            ids = list(set(ids))

            page = page + 1
            print(len(ids))

            # Put ids in file
            with open('nasa_ids', 'w') as f:
                for item in ids:
                    f.write("%s\n" % item)

        else:
            print('oof')
            raise Exception


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
args = parser.parse_args()
fetch_image_ids(args.query, args.start, args.end, args.number_of_ids)
