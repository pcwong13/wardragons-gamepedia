#!/usr/bin/env python
import csv
import riderdata
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
}

def resource_icon(name):
    #print name
    if name == 'redRiderShard':
        return '{{Icon|red rider shards}}'
    if name == 'blueRiderShard':
        return '{{Icon|blue rider shards}}'
    if name == 'purpleRiderShard':
        return '{{Icon|purple rider shards}}'
    return ' season shards'

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

# -----------------------------------------------------------------------------
# Main processing loop
# -----------------------------------------------------------------------------
for info in riderdata.info_data:
    f = open('output/'+info['name']+'.main.txt', 'w+')
    print info['name']
    upgrade_data = riderdata.getRiderUpgradeData(info['name'])
    #Infobox
    infobox = ''
    infobox +='{{RiderInfobox\n'
    infobox +='|Name={{PAGENAME}}\n'
    infobox +='|Icon={:}\n'.format(info['halfBodyIconFile'])
    infobox +='|CurrencyToExchangeXP={:}\n'.format(info['currencyToExchangeXP'])
    infobox +='|CurrencyCostPerXP={:}\n'.format(info['currencyCostPerXP'])
    infobox +='|Defensive={:}\n'.format(info['isDefensive'])
    infobox +='|SkillResetCurrency={:}\n'.format(info['skillResetCurrency'])
    infobox +='|SkillResetCost={:,}\n'.format(int(info['skillResetCost']))
    found = 0
    for key in seasonKey:
        if key in info['upgradeCSVFileName']:
            infobox +='|Season={:}\n'.format(seasonKey[key])
            infobox +='|Atlas=No\n'
            found = 1
    if found == 0:
        if info['skillResetCurrency'] == 'diamond':
            infobox +='|Season=\n'
            infobox +='|Atlas=Yes\n'
        else:
            infobox +='|Season=Other\n'
            infobox +='|Atlas=No\n'
    hirecost = upgrade_data[0]['upgradeCost'].split(":")
    infobox +='|HireCost={:}'.format(hirecost[1]) + '{:}\n'.format(resource_icon(hirecost[0]))

    infobox +='}}\n'
    f.write(infobox)
    f.close()

    upload = 1
    title = info['name']
    section = '0'
    text = infobox

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

