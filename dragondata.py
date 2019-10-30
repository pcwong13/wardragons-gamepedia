#!/usr/bin/env python
import csv

# list of [rows as dict]
class_data = []
# dicts
class_multiplier_by_id = {}
class_name_by_id = {}
with open('wd/assets/DragonClass.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for num,row in enumerate(reader):
        if num == 0:
            continue
        class_data.append(row)
        class_multiplier_by_id.update({row['identifier']:row['classMultiplier']})
        class_name_by_id.update({row['identifier']:row['displayName']})

# list of [rows as dict]
element_data = []
# dicts
element_name_by_id = {}
with open('wd/assets/Element.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for num,row in enumerate(reader):
        if num == 0:
            continue
        element_data.append(row)
        element_name_by_id.update({row['identifier']:row['displayName'].capitalize()})


# list of [rows as dict]
tier_data = []
# dicts
tier_name_by_id = {}
with open('wd/assets/DragonTier.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for num,row in enumerate(reader):
        if num == 0:
            continue
        tier_data.append(row)
        tier_name_by_id.update({row['identifier']:row['displayName']})

# list of [rows as dict]
rarity_data = []
# dicts
rarity_name_by_id = {}
with open('wd/assets/DragonRarityDescription.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for num,row in enumerate(reader):
        if num == 0:
            continue
        rarity_data.append(row)
        rarity_name_by_id.update({row['identifier']:row['displayName']})




# list of [rows as dict]
dragon_data = []
# dicts
dragon_identifier_by_name = {}
dragon_class_by_name = {}
dragon_type_by_name = {}
dragon_rarity_by_name = {}
dragon_element_by_name = {}
dragon_description_by_name = {}
dragon_upgrade_filename_by_name = {}
dragon_breeding_level_by_name = {}
dragon_breeding_cave_level_by_name = {}
dragon_incubation_time_by_name = {}
dragon_incubator_level_by_name = {}
dragon_max_level_by_name = {}
dragon_egg_currency_by_name = {}
dragon_tier_by_name = {}
dragon_fragments_by_name = {}
dragon_show_in_stable_by_name = {}
dragon_evolvable_by_name = {}
dragon_icon_by_name = {}
dragon_unbreedable_by_name = {}

with open('wd/assets/Dragon.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for num,row in enumerate(reader):
        if num == 0:
            continue
        if row['showInStable'] == '0':
            continue
        dragon_data.append(row)
        dragon_identifier_by_name.update({row['displayName']:row['identifier']})
        dragon_class_by_name.update({row['displayName']:row['dragonClass']})
        dragon_type_by_name.update({row['displayName']:row['dragonType']})
        dragon_rarity_by_name.update({row['displayName']:row['defaultRarity']})
        dragon_element_by_name.update({row['displayName']:row['elementIdentifier']})
        dragon_description_by_name.update({row['displayName']:row['displayDescription']})
        dragon_upgrade_filename_by_name.update({row['displayName']:row['upgradeCSVFileName']})
        dragon_breeding_level_by_name.update({row['displayName']:row['minDragonLevelForBreeding']})
        dragon_breeding_cave_level_by_name.update({row['displayName']:row['minBreedingCaveBuildingLevelToBreed']})
        dragon_incubation_time_by_name.update({row['displayName']:row['incubatingTime']})
        dragon_incubator_level_by_name.update({row['displayName']:row['incubationBuildingLevelRequirement']})
        dragon_max_level_by_name.update({row['displayName']:row['defaultMaxLevel']})
        dragon_egg_currency_by_name.update({row['displayName']:row['eggCurrencyType']})
        dragon_tier_by_name.update({row['displayName']:row['defaultTierNumber']})
        dragon_fragments_by_name.update({row['displayName']:row['numberOfFragmentsNeeded']})
        dragon_show_in_stable_by_name.update({row['displayName']:row['showInStable']})
        dragon_evolvable_by_name.update({row['displayName']:row['isEvolveDragon']})
        dragon_icon_by_name.update({row['displayName']:row['defaultIconFilename']})
        dragon_unbreedable_by_name.update({row['displayName']:row['isUnbreedableDragon']})
