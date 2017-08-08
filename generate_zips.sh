#!/bin/bash

# MODIFY for production
BASE="cress/media"
BASE="/home/cress/data/media"
EXPORT_FOLDER=`pwd`/export

for i in $(ls -1 export/*.list); do
    cycle=`echo $i | cut -d'_' -f2`
    # get box and box_cycle from csv file
    box=`tail $i -n +2 | tail -1 | cut -d';' -f2`
    box_cycle=`tail $i -n +2 | tail -1 | cut -d';' -f3`
    zipfile="${EXPORT_FOLDER}/cycle_pk${cycle}_box${box}_${box_cycle}_images.zip"
    if [ ! -f $zipfile ]; then
        (cd $BASE/photo/c$cycle; zip $zipfile *.jpeg)
    fi
done
