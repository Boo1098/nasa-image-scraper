#!/bin/bash

for i in {1920..2022}
do
	echo $i
	./scrape.py '' -s $i -e $i -n 100000
done
