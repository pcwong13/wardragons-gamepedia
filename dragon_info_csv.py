#!/usr/bin/env python

import sys
import re
import csv
import den
import storage
import dragon
import spell
import breedingcave

# DragonClass.csv
dragonClassMultiplier = {
    'hunter' : '2',
    'sorcerer' : '2.25',
    'warrior'  : '10',
    'invoker'  : '2'
}

# DragonRarityDescription.csv
dragonRarity = {
    '0' : 'Common',
    '1' : 'UNKNOWN',
    '2' : 'Veteran',
    '3' : 'Rare',
    '4' : 'Epic',
    '5' : 'Legendary',
    '6' : 'Mythic',
    '7' : 'Elite',
    '8' : 'Mythic'
}

# Element.csv
dragonElement = {
        'iceElement' : 'Ice',
        'fireElement' : 'Fire',
        'earthElement' : 'Earth',
        'windElement' : 'Wind',
        'darkElement' : 'Dark',
}

# DragonClass.csv
dragonClass = {
    'hunter' : 'Hunter',
    'sorcerer' : 'Sorcerer',
    'warrior'  : 'Warrior',
    'invoker'  : 'Invoker'
}

tierNum = {
    '1' : 'Red',
    '2' : 'Purple',
    '3'  : 'Blue',
    '4'  : 'Orange',
    '5'  : 'Green',
    '6'  : 'Gold',
    '7'  : 'Platinum',
    '8'  : 'Sapphire',
    '9'  : 'Garnet',
    '10'  : 'Emerald',
    '11'  : 'Obsidian',
    '12'  : 'Harbinger',
    '13'  : 'Vanguard',
    '14'  : 'Empyrean',
    '15'  : 'Abyssal'
}

seasonKey = {
    'E17Q4' : 'Wintertide',
    'E18Q1' : 'Springveil',
    'E18Q2' : 'Summerflare',
    'E18Q3' : 'Duskfall',
    'E18Q4' : 'Winterjol',
    'E19Q1' : 'Springblossom',
    'E19Q2' : 'Summerkai',
}

def time2str(sec):
    timeleft = sec
    days = 0
    hours = 0
    mins = 0
    secs = 0
    time_str = ''
    if timeleft >= 86400:
        days = timeleft/86400
        timeleft = timeleft - days*86400
    if timeleft >= 3600:
        hours = timeleft/3600
        timeleft = timeleft - hours*3600
    if timeleft >= 60:
        mins = timeleft/60
        timeleft = timeleft - mins*60
    secs = timeleft
    if int(days) > 0:
        time_str += '{:}days'.format(str(days))
    if int(hours) > 0:
        time_str += '{:}hr'.format(str(hours))
    if int(mins) > 0:
        time_str += '{:}min'.format(str(mins))
    if int(secs) > 0:
        time_str += '{:}sec'.format(str(secs))
    return time_str

for dragon_name in dragon.dragon_upgrade_filename_by_name:
    if dragon.dragon_show_in_stable_by_name[dragon_name] == '0':
        continue
    filename = 'wd/assets/'+dragon.dragon_upgrade_filename_by_name[dragon_name]
    print filename, dragon_name
    f = open('output/'+dragon_name+'.main.txt', 'w+')

    dps = ''
    health = ''
    ap = ''
    healtime = ''
    tier = ''
    rarity = ''
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        lines = list(reader)
        damage = float(lines[-1]['attackPower']) * float(dragonClassMultiplier[dragon.dragon_class_by_name[dragon_name]])
        dps = '{:,}'.format(int(round(damage)))
        health = '{:,}'.format(int(lines[-1]['HP']))
        ap = '{:,}'.format(int(lines[-1]['powerLevel']))
        heal = int(lines[-1]['fullHealDuration'])
        healtime = time2str(heal)
        if dragon.dragon_evolvable_by_name[dragon_name] == '1':
            tier = '{:}'.format(tierNum[lines[-1]['tierNumber']])
            rarity = '{:}'.format(dragonRarity[lines[-1]['rarity']])

    #Infobox
    f.write('{{DragonInfobox\n')
    f.write('|Name={{PAGENAME}}\n')
    f.write('|Icon={:}\n'.format(dragon.dragon_icon_by_name[dragon_name]))
    f.write('|Tagline={:}\n'.format(dragon.dragon_type_by_name[dragon_name]))
    f.write('|Motto={:}\n'.format(dragon.dragon_description_by_name[dragon_name]))
    f.write('|Class={:}\n'.format(dragonClass[dragon.dragon_class_by_name[dragon_name]]))
    f.write('|Element={:}\n'.format(dragonElement[dragon.dragon_element_by_name[dragon_name]]))
    f.write('|DPS={:}\n'.format(dps))
    f.write('|Health={:}\n'.format(health))
    f.write('|AP={:}\n'.format(ap))
    if dragon.dragon_evolvable_by_name[dragon_name] == '1':
        f.write('|Rarity={:}\n'.format(rarity))
        f.write('|Tier={:}\n'.format(tier))
    else:
        f.write('|Rarity={:}\n'.format(dragonRarity[dragon.dragon_rarity_by_name[dragon_name]]))
        f.write('|Tier={:}\n'.format(tierNum[dragon.dragon_tier_by_name[dragon_name]]))
    f.write('|Heal={:}\n'.format(healtime))
    for key in seasonKey:
        if key in dragon.dragon_upgrade_filename_by_name[dragon_name]:
            f.write('|Season={:}\n'.format(seasonKey[key]))
    f.write('}}\n')

    #Abilities
    f.write('\n==Abilities==\n')
    f.write('{{DragonAbilities\n')

    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        unlockList = []
        identifierList = []
        previous_length = 0
        abilities = ''
        for num,row in enumerate(reader):
            if num == 0:
                continue
            #Grab the default attack
            if num == 1:
                abilities = row['attackType']
                parse_ability = abilities.split(":")
                if parse_ability[0] == "flamethrower":
                    f.write('|Ability1=Flamethrower Attack\n')
                if parse_ability[0] == "fireball":
                    f.write('|Ability1=Fireball Attack\n')
                if parse_ability[0] == "lockon":
                    f.write('|Ability1=Lock on Attack\n')
                if parse_ability[0] == "unisonCharge":
                    f.write('|Ability1=Unison Charge\n')
            #save abilities
            abilities = row['abilities']
            if abilities == '':
                length = 0
            else:
                length = len(abilities.split("|"))
                while length != previous_length:
                    #new ability
                    unlockList.append(row['level'])
                    previous_length += 1
        parse_ability = abilities.split("|")
        for abi in parse_ability:
            name = abi.split(":")
            identifierList.append(name[1])
        for x,ident in enumerate(identifierList):
            abi_num = x+2
            abi_str = '|Ability{:}='.format(abi_num)
            if 'Resist' in identifierList[x] and not 'adaptive' in identifierList[x]:
                abi_str += spell.resist_name_by_id[identifierList[x]] + '\n'
            else:
                abi_str += spell.spell_name_by_id[identifierList[x]] + '\n'
            abi_str += '|Unlock{:}='.format(abi_num)
            abi_str += unlockList[x] + '\n'
            f.write(abi_str)
    f.write('}}\n')
    #Breeding
    f.write('\n==Breeding==\n')
    f.write('{{DragonBreeding\n')
    breedable = ''
    if dragon.dragon_unbreedable_by_name[dragon_name] == '1':
        breedable = 'No'
    else:
        breedable = 'Yes'
    f.write('|Breedable={:}\n'.format(breedable))
    f.write('|MinDragonLevelBreeding={:}\n'.format(dragon.dragon_breeding_level_by_name[dragon_name]))
    f.write('|MinBreedingCave={:}\n'.format(dragon.dragon_breeding_cave_level_by_name[dragon_name]))
    f.write('|IncubatorLevel={:}\n'.format(dragon.dragon_incubator_level_by_name[dragon_name]))
    incubator_time = time2str(int(dragon.dragon_incubation_time_by_name[dragon_name]))
    f.write('|IncubatorTime={:}\n'.format(incubator_time))
    cave_player_level = breedingcave.cave_by_level[dragon.dragon_breeding_cave_level_by_name[dragon_name]]
    incubator_player_level = breedingcave.incubator_by_level[dragon.dragon_breeding_cave_level_by_name[dragon_name]]
    if int(cave_player_level) > int(incubator_player_level):
        player_level = cave_player_level
    else:
        player_level = incubator_player_level
    f.write('|PlayerLevel={:}\n'.format(player_level))
    f.write('}}\n')
    f.write('\n==Stats==\n')
    f.write('{{')
    f.write('{:}Stats'.format(dragon_name))
    f.write('}}\n')
    f.close()

