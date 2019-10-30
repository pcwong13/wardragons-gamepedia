#!/usr/bin/env python
import csv

def getRiderUpgradeData(name):
    for rider in riderupgrades:
        if rider.keys()[0] == name:
            return rider[name]

def getRiderGearData(name):
    for gear in gear_data:
        if gear['identifier'] == name:
            return gear

# list of [rows as dict]
info_data = []
with open('wd/assets/Rider.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for num,row in enumerate(reader):
        if num == 0:
            continue
        info_data.append(row)


# riderupgrades = [ {RiderlName: List of row data}, {RiderName: List of row data} ]
riderupgrades = []
# dict {RiderName : list}
riderupgrade_dict = {}
# list of [rows as dict]
riderupgrade_data = []

for inforow in info_data:
    filename = inforow['upgradeCSVFileName']
    #print filename
    with open('wd/assets/'+filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for num,row in enumerate(reader):
            # skip header
            if num == 0:
                continue
            riderupgrade_data.append(row)
    riderupgrade_dict.update({inforow['name']:riderupgrade_data})
    riderupgrades.append(riderupgrade_dict)

    riderupgrade_dict = {}
    riderupgrade_data = []

# list of [rows as dict]
skilltree_data = []
with open('wd/assets/RiderSkillTree.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for num,row in enumerate(reader):
        if num == 0:
            continue
        skilltree_data.append(row)
#sort the list by position
skilltree_data = sorted(skilltree_data, key=lambda k: (k['identifier'][:-3], int(k['position'].split("~")[0]), -int(k['position'].split("~")[1])))
#for row in skilltree_data:
#    print row

# list of [rows as dict]
gear_data = []
with open('wd/assets/RiderGear.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for num,row in enumerate(reader):
        if num == 0:
            continue
        gear_data.append(row)



