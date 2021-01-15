#!./env/bin/python
import requests
import pandas as pd
import selenium
import time
from selenium import webdriver
from bs4 import BeautifulSoup

wd = webdriver.Firefox()

def fetch_image_ids(query:str, start:int, end:int, max_links_to_fetch:int):
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0,document.body.scrollHeight);")

    # build the google query
    search_url = "https://images.nasa.gov/search-results?q={query}&page={page}&media=image&yearStart={start}&yearEnd={end}"

    page =1

    # load the page
    #scroll_to_end(wd)

    ids=[]

    while len(ids)<max_links_to_fetch:
        wd.get(search_url.format(query=query,start=start,end=end,page=page))
        time.sleep(2)

        soup = BeautifulSoup(wd.page_source,'html.parser')
        images = soup.find_all('img')

        # get all image thumbnail results
        thumbnail_results=wd.find_element_by_tag_name('img')
        
        for img in images:
            src = img.get('src')
            if 'images-assets.nasa.gov' in src:
                parts = src.split('/')
                nasa_id = parts[4]
                ids.append(nasa_id)

        ids=list(set(ids))
        page=page+1
        print(len(ids))

    with open('nasa_ids', 'w') as f:
        for item in ids:
            f.write("%s\n" % item)

fetch_image_ids("apollo",1960,1975,1000)
