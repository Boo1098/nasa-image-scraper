#!./env/bin/python
import requests
import time
import json

def fetch_image_ids(query:str, start:int, end:int, max_links_to_fetch:int):
    # build the query
    search_url =    "https://images-api.nasa.gov/search?q={query}&page={page}&media_type=image&year_start={start}&year_end={end}"

    page =1

    # load the page
    #scroll_to_end(wd)

    ids=[]
    done = False

    while len(ids)<max_links_to_fetch and not done:
        print(search_url.format(query=query,page=page,start=start,end=end))
        response=requests.get(search_url.format(query=query,page=page,start=start,end=end))
        time.sleep(3)
        if response.status_code==200:
            response_json = response.json()

            for key,value in response_json:
                if key == "nasa_id":
                    nasa_id = value
                    print(nasa_id)
                    ids.append(nasa_id)

            ids=list(set(ids))
            page=page+1
            print(len(ids))

            with open('nasa_ids', 'w') as f:
                for item in ids:
                    f.write("%s\n" % item)
        else:
            print('oo')

fetch_image_ids("apollo",1960,1975,2000)
