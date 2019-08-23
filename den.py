#!/usr/bin/env python
import csv

den_by_level = {}

def get_player(den_level):
    for idx,key in enumerate(den_by_level):
        if key == den_level:
            return den_by_level[key]

with open('wd/assets/StableUpgrades.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for num,row in enumerate(reader):
        if num == 0:
            continue
        den = row['levelRequired']
        if den == '':
            den = '1'
        den_by_level.update({row['level']:den})
