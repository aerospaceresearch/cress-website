#!/bin/bash

# MODIFY for production
BASE="cress/media"
EXPORT_FOLDER=`pwd`/export

for i in $(ls -1 export/*.list); do
    echo "$i"
    cycle=`echo $i | cut -d'_' -f2`
    echo $cycle
    (cd $BASE/photo/c$cycle; zip ${EXPORT_FOLDER}/cycle_${cycle}_images.zip *.jpeg)
done
