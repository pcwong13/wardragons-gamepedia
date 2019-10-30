#!/usr/bin/env python
import csv

def getUpgradeData(name):
    for building in building_upgrade:
        if building.keys()[0] == name:
            return building[name]

def getHarvestRateLevel(rate):
    woodFarm = getUpgradeData('woodFarm')
    for row in woodFarm:
        deltaAmt = row['harvestAmount'].split(":")[1]
        deltaTime = row['harvestTimeInSeconds']
        harvestRateHr = float(deltaAmt) / (float(deltaTime)/60/60)
        if float(rate) < harvestRateHr:
            return row['level']

def get_den_player_requirement(den_level):
    for idx,key in enumerate(den_by_level):
        if key == den_level:
            return den_by_level[key]


# list of [rows as dict]
building_data = []
name_by_id = {}

with open('wd/assets/Building.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for num,row in enumerate(reader):
        if num == 0:
            continue
        building_data.append(row)
        name_by_id.update({row['identifier']:row['displayName']})

building_upgrade = []
# dict {ID : list}
upgrade_dict = {}
# list of [rows as dict]
upgrade_data = []
for buildings in building_data:
    with open('wd/assets/'+buildings['upgradeCSVFileName']) as csvfile:
        reader = csv.DictReader(csvfile)
        for num,row in enumerate(reader):
            if num == 0:
                continue
            upgrade_data.append(row)
    upgrade_dict.update({buildings['identifier']:upgrade_data})
    building_upgrade.append(upgrade_dict)

    upgrade_dict = {}
    upgrade_data = []


breedingGround = getUpgradeData('breedingGround')
incubator = getUpgradeData('incubator')
cave_by_level = {}
incubator_by_level = {}

for row in breedingGround:
    if row['levelRequired'] == '':
        cave_by_level.update({row['level']:'1'})
    else:
        cave_by_level.update({row['level']:row['levelRequired']})

for row in incubator:
    if row['levelRequired'] == '':
        incubator_by_level.update({row['level']:'0'})
    else:
        incubator_by_level.update({row['level']:row['levelRequired']})


stable = getUpgradeData('stable')
den_by_level = {}

for row in stable:
    den = row['levelRequired']
    if den == '':
        den = '1'
    den_by_level.update({row['level']:den})
