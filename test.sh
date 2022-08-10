#!/bin/bash

for (( i=0; i<=2; i=i+1 ))
do
	python3 test-plots.py
	sleep 3
	echo $i
	rm -r scream/*.png
done

