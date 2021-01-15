#!./env/bin/python
import requests
import time
import json

def fetch_image_ids(query:str, start:int, end:int, max_links_to_fetch:int):
    # build the query
    search_url =    "https://images-api.nasa.gov/search?q={query}&page={page}&media_type=image&year_start={start}&year_end={end}"

    page =1

    ids=[]
    done = False

    last_ids_len = -1

    while len(ids)<max_links_to_fetch and len(ids)!=last_ids_len:
        last_ids_len = len(ids)
        response=requests.get(search_url.format(query=query,page=page,start=start,end=end))
        time.sleep(.5)
        if response.status_code==200:
            response_json = response.json()

            for item in response_json["collection"]["items"]:
                nasa_id=item["data"][0]["nasa_id"]
                ids.append(nasa_id)

            ids=list(set(ids))
            page=page+1
            print(len(ids))

            with open('nasa_ids', 'w') as f:
                for item in ids:
                    f.write("%s\n" % item)
        else:
            print('oof')
            raise Exception

fetch_image_ids("apollo",1960,1975,10000)
