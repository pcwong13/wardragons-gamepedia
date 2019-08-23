#!/usr/bin/env python
import csv

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
