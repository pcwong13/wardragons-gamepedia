#!/usr/bin/env python
import csv
import riderdata
import requests
import wikilogin

# -----------------------------------------------------------------------------
# Main processing loop
# -----------------------------------------------------------------------------

#
# Skills TEMPLATE ---- not uploadable. use copy/paste
#
f = open('output/TEMPLATE_RiderSkill.txt', 'w+')

f.write('{{#switch: {{{1|{{{Name|}}}}}}\n')
for row in riderdata.gear_data:
    if row['slot'] == 'skill':
        f.write('|{:} = [[Image:'.format(row['identifier']))
        f.write('{:}|32px]]'.format(row['iconFilename']))
        f.write(' {:}\n'.format(row['displayName']))
f.write('|#default = UNKNOWN\n}}<noinclude>{{Doc}}[[Category:Formatting templates]]</noinclude>')
f.close

#
# rider skills table
#
for info in riderdata.info_data:
    f = open('output/'+info['name']+'.skills.txt', 'w+')
    print info['name']

    root = info['rootSkillIdentifier'][:-3]

    skill_string = '==Details==\n'
    skill_string += '{| class="wikitable" style="text-align: center;"\n'
    skill_string += '    |-\n'
    skill_string += '        !ID\n'
    skill_string += '        !Column\n'
    skill_string += '        !Row\n'
    skill_string += '        !Name\n'
    skill_string += '        !Max<br />Levels\n'
    skill_string += '        !Buff<br />Amount<br />Per Level\n'
    skill_string += '        !Skill<br />Points<br />Per Level\n'
    skill_string += '        !Build<br />Skill<br />Level<br />Allocation\n'

    ID = 1
    for row in riderdata.skilltree_data:
        if root in row['identifier']:
            #print row['riderGearIdentifier']
            skill_string += '    |-\n'
            # ID
            skill_string += '        ||{:<4}'.format(str(ID).zfill(2))
            # Column
            skill_string += '||{:<4}'.format(row['position'].split("~")[0])
            # Row
            skill_string += '||{:<4}'.format(row['position'].split("~")[1])
            # Name
            skill_string += '||{{RiderSkill|'+'{:<48}'.format(row['riderGearIdentifier'])+'}} '
            # Max Level
            gear_data = riderdata.getRiderGearData(row['riderGearIdentifier'])
            skill_string += '||{:<4}'.format(gear_data['maxLevel'])
            maxLevel = gear_data['maxLevel']
            # Buff
            buff = '{:+}'.format(float(gear_data['buff1Base']))
            if int(maxLevel) > 1:
                for num in range(1,int(maxLevel)):
                    buff += ', {:+}'.format(float(gear_data['buff1Base']) + (num * float(gear_data['buff1PerLvl'])))
            skill_string += '||{:<40}'.format(buff)
            # Skill Points
            skill_string += '||{:<8}'.format(gear_data['craftingCost'].split(":")[1])
            # Build
            skill_string += '<td id="{:}"></td>\n'.format(ID)
            ID += 1
    skill_string += '|}\n'
    f.write(skill_string)
    f.close()

    upload = 1
    title = info['name']
    section = '4'
    text = skill_string

    # -------------------------------------------------------------------------
    # Wiki Auto-Upload
    # -------------------------------------------------------------------------
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
            "section": section,
            "bot": "true",
            "token": CSRF_TOKEN,
            "format": "json",
            "text": text
        }

        R = S.post(URL, data=PARAMS_3)
        DATA = R.json()

        print(DATA)

