#!/usr/bin/env python
import csv

def get_level(xp):
    for key in sorted(xp_by_id):
        if int(xp) < int(xp_by_id[key]):
            return key
    return '999'

# list of [rows as dict]
level_data = []
xp_by_id = {}

with open('wd/assets/Level.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for num,row in enumerate(reader):
        if num == 0:
            continue
        level_data.append(row)
        xp_by_id.update({row['identifier']:row['requiredXp']})

