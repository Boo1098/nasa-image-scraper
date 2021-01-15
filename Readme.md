# Overview

Two scripts are provided that scrape images.nasa.gov to gather images and metadata from a query.

## scrape.py

This generates a file called ```nasa\_ids``` that contains all the NASA ids for a specific query. It requires the query, and optionally the start and end years as well as the max number of ids to gather.

## pull.py

This fills the directory ```./images``` and ```./images/json``` with the images and json metadata respectively for all ids in the ```nasa_ids``` file
