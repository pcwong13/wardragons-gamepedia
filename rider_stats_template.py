#!/usr/bin/env python

import csv
import riderdata
import requests
import wikilogin

def convertCamel (camel_input):
    words = re.findall(r'[A-Z]?[a-z]+|[A-Z]{2,}(?=[A-Z][a-z]|\d|\W|$)|\d+', camel_input)
    return ' '.join(map(str.lower, words))

def resource_icon(name):
    #print name
    if name == 'redRiderShard':
        return '{{Icon|red rider shards}}'
    if name == 'blueRiderShard':
        return '{{Icon|blue rider shards}}'
    if name == 'purpleRiderShard':
        return '{{Icon|purple rider shards}}'
    return ' season shards'

# -----------------------------------------------------------------------------
# Main processing loop
# -----------------------------------------------------------------------------

#
# rider stats
#
for info in riderdata.info_data:
    f = open('output/'+info['name']+'.upgrade.txt', 'w+')
    print info['name']

    upgrade_data = riderdata.getRiderUpgradeData(info['name'])

    string = ''
    string += '{| class="wikitable" style="text-align: center;"\n'
    string += '    |-\n'
    string += '        !Rider<br />Level\n'
    string += '        !Combat<br />Level\n'
    string += '        !Upgrade<br />XP<br />For This Level\n'
    string += '        !Upgrade<br />Cost<br />For This Level\n'
    string += '        !Skill<br />Points<br />Gained<br />For This Level\n'
    for row in upgrade_data:
        string += '    |-\n'
        #level
        string += '        ||{:<8}'.format(row['level'])
        #combat
        combat = '{:,}'.format(int(row['combatLevel']))
        combat += '{{Icon|combat level}}'
        string += '||{:<32}'.format(combat)
        #xp
        if row['upgradeXP'] == '':
            xp_str = '0'
        else:
            xp_str = '{:,}'.format(int(row['upgradeXP']))
        xp_str += '{{Icon|glory}}'
        string += '||{:<28}'.format(xp_str)
        #rss
        upgrade_cost = row['upgradeCost']
        upgrade_fields = upgrade_cost.split(":")
        rss_str = '{:,}'.format(int(upgrade_fields[1])) + resource_icon(upgrade_fields[0])
        string += '||{:<40}'.format(rss_str)
        #skill pts
        string += '||{:,}\n'.format(int(row['skillPointsGain']))
    string += '|}\n'
    f.write(string)
    f.close()

    upload = 1
    title = 'Template:'+info['name']+'Stats'
    text = string

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

