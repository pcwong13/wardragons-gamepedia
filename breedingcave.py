#!/usr/bin/env python
import csv

cave_by_level = {}
incubator_by_level = {}

with open('wd/assets/BreedingUpgrades.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for num,row in enumerate(reader):
        if num == 0:
            continue
        if row['levelRequired'] == '':
            cave_by_level.update({row['level']:'1'})
        else:
            cave_by_level.update({row['level']:row['levelRequired']})

with open('wd/assets/IncubatorUpgrades.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for num,row in enumerate(reader):
        if num == 0:
            continue
        if row['levelRequired'] == '':
            incubator_by_level.update({row['level']:'0'})
        else:
            incubator_by_level.update({row['level']:row['levelRequired']})
