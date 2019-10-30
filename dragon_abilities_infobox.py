#!/usr/bin/env python

import spell
import requests
import wikilogin

#
# ABILITIES TEMPLATE ---- not uploadable. use copy/paste
#
f = open('output/TEMPLATE_Abilities.txt', 'w+')

f.write('{{#switch: {{{1|{{{Ability}}}}}}\n')
f.write('|fireball = [[Image:Fireball-attack.png|32px]] [[Fireball Attack]]\n')
f.write('|flamethrower = [[Image:Flamethrower-attack.png|32px]] [[Flamethrower Attack]]\n')
f.write('|lockon = [[Image:Lock-on-attack.png|32px]] [[Lock on Attack]]\n')
f.write('|unisonCharge = [[Image:Fireball-attack.png|32px]] [[Unison Charge]]\n')

skip_list = ['adaptiveBreath2',
        'alterFate2',
        'bloodEssenceConsume1',
        'chainLightning3',
        'chargedShieldSuper',
        'chainLightningSuper',
        'spectralForm2','spectralForm3','spectralForm4','spectralForm_warrior1',
        'superHeal',
        'superDeathGaze',
        'whiteSummonDragon1',
        'heatBlastShield2',
]

modify_dict = {'whiteDreadfulRoar1':'White Dreadful Roar',
        'rampageSorcerer1':'Rampage Sorcerer',
        'whiteSacrifice1':'White Sacrifice',
        'stormShieldWhite1':'Storm Shield White',
        'whiteSuperRejuvenate1':'White Super Rejuvenate',
        'umbralSpikeWhite1':'Umbral Spike White',
        'chargedShield2':'Explosive Shield 2',
        'summonDragon1d':'Summon Warrior d',
        'summonDragon2':'Summon Warrior 2',
        'chainLightning2':'Chain Lightning 2',
        'heatBlastShield2':'Heat Shield 2',
}

ability_list = []

for identifier in spell.spell_icon_by_id:
    string = '|{:} = [[Image:'.format(identifier)
    if spell.spell_name_by_id[identifier] == 'Northern Lights (Dark)':
        string +='{:}|32px'.format('icon_northernLights_dark.png')
    else:
        string +='{:}|32px'.format(spell.spell_icon_by_id[identifier])
    string +='|class={:}-ability]]'.format(spell.spell_color_by_id[identifier])
    if identifier in modify_dict:
        string +='[[{:}]]\n'.format(modify_dict[identifier])
    else:
        string +='[[{:}]]\n'.format(spell.spell_name_by_id[identifier])
    ability_list.append(string)

for identifier in spell.resist_icon_by_id:
    string ='|{:} = [[Image:'.format(identifier)
    string +='{:}|32px]]'.format(spell.resist_icon_by_id[identifier])
    string +='[[{:}]]\n'.format(spell.resist_name_by_id[identifier])
    ability_list.append(string)

for string in sorted(ability_list):
    f.write(string)

f.write('|#default = {{{1|{{{Ability}}}}}}\n')
f.write('}}<noinclude>{{Doc}}[[Category:Formatting templates]]</noinclude>\n')
f.close()
 

#
# ABILITY INFOBOX ------ auto uplaod
#
upload = 1

f = open('output/ABILITIES_Description.txt', 'w+')
text = ''
for identifier in sorted(spell.spell_name_by_id.keys()):
    text = ''
    if 'Resist' in identifier and not 'adaptive' in identifier:
        title = spell.resist_name_by_id[identifier]
        text += '<!--{:}-->\n'.format(spell.resist_name_by_id[identifier])
        text += '<!--{:}-->\n'.format(identifier)
        text += '{{AbilityInfobox\n'
        text += '|Identifier={:}\n'.format(identifier)
        text += '|Color={:}\n'.format('Yellow')
        text += '|Cost={:}\n'.format('Passive')
        text += '|Description={:}\n'.format(spell.resist_name_by_id[identifier])
        text += '}}\n\n'
    else:
        if identifier in skip_list:
            continue
        if identifier in modify_dict:
            title = modify_dict[identifier]
        else:
            title = spell.spell_name_by_id[identifier]
        #print title
        text += '<!--{:}-->\n'.format(title)
        text += '<!--{:}-->\n'.format(identifier)
        text += '{{AbilityInfobox\n'
        text += '|Identifier={:}\n'.format(identifier)
        color = spell.spell_color_by_id[identifier]
        color = color[0].upper() + color[1:]
        text += '|Color={:}\n'.format(color)
        if spell.spell_rage_by_id[identifier] == 'passive':
            text += '|Cost={:}\n'.format('Passive')
        else:
            text += '|Cost={:}\n'.format(spell.spell_rage_by_id[identifier])
        text += '|Description={:}\n'.format(spell.spell_desc_by_id[identifier])
        text += '}}\n\n'
    f.write(text)


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
            "section": "0",
            "bot": "true",
            "token": CSRF_TOKEN,
            "format": "json",
            "text": text
        }

        R = S.post(URL, data=PARAMS_3)
        DATA = R.json()

        print(DATA)

f.close()


