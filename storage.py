#!/usr/bin/env python
import csv

storage_by_level = {}

def get_storage(rss):
    for idx,key in enumerate(storage_by_level):
        lvl = idx+1
        if int(rss) <= int(storage_by_level[str(lvl)]):
            return str(lvl)

with open('wd/assets/StorageUpgrades.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for num,row in enumerate(reader):
        if num == 0:
            continue
        storage = row['maxStorageData']
        rss_type = storage.split("|")
        rss_max = rss_type[0].split(":")
        storage_by_level.update({row['level']:rss_max[1]})
