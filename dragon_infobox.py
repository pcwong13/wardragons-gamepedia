#!/usr/bin/env python
import csv
import buildingdata
import dragondata
from math import floor
import requests
import wikilogin

seasonKey = {
    'E17Q4' : 'Wintertide',
    'E18Q1' : 'Springveil',
    'E18Q2' : 'Summerflare',
    'E18Q3' : 'Duskfall',
    'E18Q4' : 'Winterjol',
    'E19Q1' : 'Springblossom',
    'E19Q2' : 'Summerkai',
    'E19Q3' : 'Withermoon',
    'E19Q4' : 'Frostwreath',
    'E20Q1' : 'Lotusbloom',
}

def format_time(sec):
    timeleft = int(sec)
    string = ''
    if timeleft >= (60*60*24):
        days = int(floor(float(timeleft)/60/60/24))
        string += '{:}d'.format(days)
        timeleft -= (days*60*60*24)
    if timeleft >= (60*60):
        hours = int(floor(float(timeleft)/60/60))
        string += '{:}h'.format(hours)
        timeleft -= (hours*60*60)
    if timeleft >= (60):
        mins = int(floor(float(timeleft)/60))
        string += '{:}m'.format(mins)
        timeleft -= (mins*60)
    if timeleft > (0):
        sec = timeleft
        string += '{:}s'.format(sec)
    return string

replace_dict = {
        'dreadfulRoar137':'dreadfulRoar1', #ursa
        'dreadfulRoar142':'dreadfulRoar1', #gloomclaw
        'maleficBreath142':'maleficBreath1', #gloomclaw
        'whiteDreadfulRoar153':'whiteDreadfulRoar1', #algor
        'ectoplasmicBreath219':'ectoplasmicBreath1', #somnnus
        'heatstroke209':'heatstroke1',# Cuauhtli
}

# Upload options
upload = 1

if upload == 1:
    # UPLOAD TO WIKI
    S = requests.Session()

    URL = "https://wardragons.gamepedia.com/api.php"

    # Step 1: GET Request to fetch login token
    PARAMS_0 = {
        "action": "query",
        "meta": "tokens",
        "type": "login",
        "format": "json"
    }

    R = S.get(url=URL, params=PARAMS_0)
    DATA = R.json()

    LOGIN_TOKEN = DATA['query']['tokens']['logintoken']

    # Step 2: POST Request to log in. Use of main account for login is not
    # supported. Obtain credentials via Special:BotPasswords
    # (https://www.mediawiki.org/wiki/Special:BotPasswords) for lgname & lgpassword
    PARAMS_1 = {
        "action": "login",
        "lgname": wikilogin.lgname,
        "lgpassword": wikilogin.lgpassword,
        "lgtoken": LOGIN_TOKEN,
        "format": "json"
    }

    R = S.post(URL, data=PARAMS_1)

    # Step 3: GET request to fetch CSRF token
    PARAMS_2 = {
        "action": "query",
        "meta": "tokens",
        "format": "json"
    }

    R = S.get(url=URL, params=PARAMS_2)
    DATA = R.json()

    CSRF_TOKEN = DATA['query']['tokens']['csrftoken']

# -----------------------------------------------------------------------------
# Main processing loop
# -----------------------------------------------------------------------------
for dragon_name in dragondata.dragon_upgrade_filename_by_name:
    if dragondata.dragon_show_in_stable_by_name[dragon_name] == '0':
        continue
    #if 'E19Q3' in dragondata.dragon_upgrade_filename_by_name[dragon_name]:
    #    print 'Skipping: {:}'.format(dragondata.dragon_upgrade_filename_by_name[dragon_name])
    #    continue

    filename = 'wd/assets/'+dragondata.dragon_upgrade_filename_by_name[dragon_name]
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
        damage = float(lines[-1]['attackPower']) * float(dragondata.class_multiplier_by_id[dragondata.dragon_class_by_name[dragon_name]])
        dps = '{:,}'.format(int(round(damage)))
        health = '{:,}'.format(int(lines[-1]['HP']))
        ap = '{:,}'.format(int(lines[-1]['powerLevel']))
        heal = int(lines[-1]['fullHealDuration'])
        healtime = format_time(heal)
        if dragondata.dragon_evolvable_by_name[dragon_name] == '1':
            tier = '{:}'.format(dragondata.tier_name_by_id[lines[-1]['tierNumber']])
            rarity = '{:}'.format(dragondata.rarity_name_by_id[lines[-1]['rarity']])

    #Infobox
    infobox = ''
    infobox +='{{DragonInfobox\n'
    infobox +='|Name={{PAGENAME}}\n'
    infobox +='|Icon={:}\n'.format(dragondata.dragon_icon_by_name[dragon_name])
    infobox +='|Tagline={:}\n'.format(dragondata.dragon_type_by_name[dragon_name])
    infobox +='|Motto={:}\n'.format(dragondata.dragon_description_by_name[dragon_name])
    infobox +='|Class={:}\n'.format(dragondata.class_name_by_id[dragondata.dragon_class_by_name[dragon_name]])
    infobox +='|Element={:}\n'.format(dragondata.element_name_by_id[dragondata.dragon_element_by_name[dragon_name]])
    infobox +='|DPS={:}\n'.format(dps)
    infobox +='|Health={:}\n'.format(health)
    infobox +='|AP={:}\n'.format(ap)
    if dragondata.dragon_evolvable_by_name[dragon_name] == '1':
        infobox +='|Rarity={:}\n'.format(rarity)
        infobox +='|Tier={:}\n'.format(tier)
    else:
        infobox +='|Rarity={:}\n'.format(dragondata.rarity_name_by_id[dragondata.dragon_rarity_by_name[dragon_name]])
        infobox +='|Tier={:}\n'.format(dragondata.tier_name_by_id[dragondata.dragon_tier_by_name[dragon_name]])
    infobox +='|Heal={:}\n'.format(healtime)
    for key in seasonKey:
        if key in dragondata.dragon_upgrade_filename_by_name[dragon_name]:
            infobox +='|Season={:}\n'.format(seasonKey[key])
    infobox +='}}\n'
    f.write(infobox)

    #Abilities
    dragonability = ''
    dragonability +='\n==Abilities==\n'
    dragonability +='{{DragonAbilities\n'

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
                attack_string = '|Ability1={:}\n'.format(parse_ability[0])
                dragonability +=attack_string
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
            #if dragon_name == 'Skarr':
            #    print ident
            abi_num = x+2
            abi_str = '|Ability{:}='.format(abi_num)
            if ident in replace_dict:
                abi_str += replace_dict[ident] + '\n'
            else:
                abi_str += ident + '\n'
            abi_str += '|Unlock{:}='.format(abi_num)
            abi_str += unlockList[x] + '\n'
            dragonability +=abi_str
    dragonability +='}}\n'
    f.write(dragonability)

    #Breeding
    breeding = ''
    breeding +='\n==Breeding==\n'
    breeding +='{{DragonBreeding\n'
    breedable = ''
    if dragondata.dragon_unbreedable_by_name[dragon_name] == '1':
        breedable = 'No'
    else:
        breedable = 'Yes'
    breeding +='|Breedable={:}\n'.format(breedable)
    breeding +='|MinDragonLevelBreeding={:}\n'.format(dragondata.dragon_breeding_level_by_name[dragon_name])
    breeding +='|MinBreedingCave={:}\n'.format(dragondata.dragon_breeding_cave_level_by_name[dragon_name])
    breeding +='|IncubatorLevel={:}\n'.format(dragondata.dragon_incubator_level_by_name[dragon_name])
    incubator_time = format_time(int(dragondata.dragon_incubation_time_by_name[dragon_name]))
    breeding +='|IncubatorTime={:}\n'.format(incubator_time)
    cave_player_level = buildingdata.cave_by_level[dragondata.dragon_breeding_cave_level_by_name[dragon_name]]
    incubator_player_level = buildingdata.incubator_by_level[dragondata.dragon_breeding_cave_level_by_name[dragon_name]]
    if int(cave_player_level) > int(incubator_player_level):
        player_level = cave_player_level
    else:
        player_level = incubator_player_level
    breeding +='|PlayerLevel={:}\n'.format(player_level)
    breeding +='}}\n'
    f.write(breeding)
    f.write('\n==Stats==\n')
    f.write('{{')
    f.write('{:}Stats'.format(dragon_name))
    f.write('}}\n')
    f.close()

    title = dragon_name

    # -------------------------------------------------------------------------
    # Wiki Auto-Upload
    # -------------------------------------------------------------------------

    if upload == 1:
        # Step 4: POST request to edit a page
        PARAMS_3 = {
            "action": "edit",
            "title": title,
            "section": "0",
            "bot": "true",
            "token": CSRF_TOKEN,
            "format": "json",
            "text": infobox
        }

        R = S.post(URL, data=PARAMS_3)
        DATA = R.json()

        print(DATA)

        # Step 4: POST request to edit a page
        PARAMS_3 = {
            "action": "edit",
            "title": title,
            "section": "1",
            "bot": "true",
            "token": CSRF_TOKEN,
            "format": "json",
            "text": dragonability
        }

        R = S.post(URL, data=PARAMS_3)
        DATA = R.json()

        print(DATA)

        # Step 4: POST request to edit a page
        PARAMS_3 = {
            "action": "edit",
            "title": title,
            "section": "2",
            "bot": "true",
            "token": CSRF_TOKEN,
            "format": "json",
            "text": breeding
        }

        R = S.post(URL, data=PARAMS_3)
        DATA = R.json()

        print(DATA)

