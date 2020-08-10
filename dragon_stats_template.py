#!/usr/bin/env python

import sys
import re
import csv
import dragondata
import buildingdata
import requests
import wikilogin

def convertCamel (camel_input):
    words = re.findall(r'[A-Z]?[a-z]+|[A-Z]{2,}(?=[A-Z][a-z]|\d|\W|$)|\d+', camel_input)
    return ' '.join(map(str.lower, words))

#upload options
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


for dragon_name in dragondata.dragon_upgrade_filename_by_name:
    if dragondata.dragon_show_in_stable_by_name[dragon_name] == '0':
        continue
    #if 'E19Q4Invoker' in dragondata.dragon_upgrade_filename_by_name[dragon_name]:
    #    print 'Skipping: {:}'.format(dragondata.dragon_upgrade_filename_by_name[dragon_name])
    #    continue

    filename = 'wd/assets/'+dragondata.dragon_upgrade_filename_by_name[dragon_name]
    print filename, dragon_name

    f = open('output/'+dragon_name+'.upgrade.txt', 'w+')

    #shift xp by 1 row
    previous_xp = '0'
    string = ''
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        string += '{| class="wikitable" style="text-align: center;"\n'
        string += '    |-\n'
        string += '        !Dragon<br />Level\n'
        string += '        !HP\n'
        string += '        !Attack\n'
        string += '        !DPS\n'
        string += '        !Attack<br />Power\n'
        string += '        !Battle<br />Cost\n'
        string += '        !Requirements<br />For This Level\n'
        if dragondata.dragon_evolvable_by_name[dragon_name] == '1':
            string += '        !Breeding<br />Requirements<br />For This Level\n'
        string += '        !Upgrade<br />XP<br />For This Level\n'
        string += '        !Upgrade<br />Cost<br />For This Level\n'
        previous_storage = ''
        for num,row in enumerate(reader):
            #skip data type row that follows header row
            if num == 0:
                continue
            string += '    |-\n'
            #level
            string += '        ||{:<16}'.format(row['level'])
            #hp
            hp_str = '{:,}'.format(int(row['HP']))
            string += '||{:<16}'.format(hp_str)
            #attack
            atk = '{:,}'.format(int(float(row['attackPower'])))
            string += '||{:<16}'.format(atk)
            #dps
            damage = float(row['attackPower']) * float(dragondata.class_multiplier_by_id[dragondata.dragon_class_by_name[dragon_name]])
            dps = '{:,}'.format(int(round(damage)))
            string += '||{:<16}'.format(dps)
            #AP
            ap = '{:,}'.format(int(row['powerLevel']))
            string += '||{:<16}'.format(ap)
            #battle cost
            battlecost = row['battleUseCost'].split(":")
            battlecost = '{:,}'.format(int(battlecost[1])) + '{{Icon|food}}'
            string += '||{:<32}'.format(battlecost)
            #player
            stable = row['requiredStableLevel']
            req_str = buildingdata.get_den_player_requirement(stable)
            req_str += '{{Icon|player level}} '
            #den
            req_str += stable
            req_str += '{{Icon|dragons den}} '
            string += '||{:<64}'.format(req_str)
            #breeding
            if dragondata.dragon_evolvable_by_name[dragon_name] == '1':
                breed = row['achievementRequirements']
                if breed == '':
                    string += '||{:<40}'.format('')
                else:
                    breeding = convertCamel(breed)
                    string += '||{:<40}'.format(breeding[4:])
            #xp
            xp_str = '{:,}'.format(int(previous_xp))
            previous_xp = row['upgradeXP']
            xp_str += '{{Icon|xp}}'
            string += '||{:<28}'.format(xp_str)
            #rss
            upgrade_cost = row['upgradeCost']
            upgrade_fields = upgrade_cost.split(":")
            if 'Stone' in upgrade_fields[0]:
                if 'PurpleStone' in upgrade_fields[0]:
                    rss_str = '{{Icon|purple stone}}'
                if 'GreenStone' in upgrade_fields[0]:
                    rss_str = '{{Icon|green stone}}'
                if 'GoldStone' in upgrade_fields[0]:
                    rss_str = '{{Icon|gold stone}}'
                if 'PlatinumStone' in upgrade_fields[0]:
                    rss_str = '{{Icon|platinum stone}}'
                if 'SapphireStone' in upgrade_fields[0]:
                    rss_str = '{{Icon|sapphire stone}}'
                if 'GarnetStone' in upgrade_fields[0]:
                    rss_str = '{{Icon|garnet stone}}'
                if 'EmeraldStone' in upgrade_fields[0]:
                    rss_str = '{{Icon|emerald stone}}'
                if 'ObsidianStone' in upgrade_fields[0]:
                    rss_str = '{{Icon|obsidian stone}}'
                if 'HarbingerStone' in upgrade_fields[0]:
                    rss_str = '{{Icon|harbinger stone}}'
                if 'VanguardStone' in upgrade_fields[0]:
                    rss_str = '{{Icon|vanguard stone}}'
                if 'EmpyreanStone' in upgrade_fields[0]:
                    rss_str = '{{Icon|empyrean stone}}'
                if 'AbyssalStone' in upgrade_fields[0]:
                    rss_str = '{{Icon|abyssal stone}}'
                if 'EldritchStone' in upgrade_fields[0]:
                    rss_str = '{{Icon|eldritch stone}}'
            else:
                if upgrade_cost != '':
                    rss_str = '{:,}'.format(int(upgrade_fields[1]))
                    if upgrade_fields[0] == 'food':
                        rss_str += '{{Icon|food}}'
            string += '||{:}\n'.format(rss_str)
        string += '|}\n'
        f.write(string)
    f.close()

    title = 'Template:'+dragon_name+'Stats'
    text = string

    if upload == 1:
        # Step 4: POST request to edit a page
        PARAMS_3 = {
            "action": "edit",
            "title": title,
            "bot": "true",
            "token": CSRF_TOKEN,
            "format": "json",
            "text": text
        }

        R = S.post(URL, data=PARAMS_3)
        DATA = R.json()

        print(DATA)

