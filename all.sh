#!/bin/bash

for i in {1986..2022}
do
	echo $i
	./scrape.py '' -s $i -e $i -n 100000 -o all_ids
done
