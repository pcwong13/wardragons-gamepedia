#!/usr/bin/env python
import requests
import buildingdata
from math import floor
import wikilogin

def resource_icon(name):
    #print name
    if name == 'piercing':
        return '{{Icon|lumber}}'
    if name == 'food':
        return '{{Icon|food}}'
    if name == 'gold':
        return '{{Icon|gold}}'
    if name == 'blackPearl':
        return '{{Icon|black pearls}}'
    if name == 'iceShard':
        return '{{Icon|ice shards}}'
    if name == 'fireShard':
        return '{{Icon|fire shards}}'
    if name == 'elementalEmber':
        return '{{Icon|elemental embers}}'
    if name == 'electrumBar':
        return '{{Icon|electrum bar}}'
    if name == 'redEggCurrency':
        return '{{Icon|red egg}}'
    if name == 'purpleEggCurrency':
        return '{{Icon|purple egg}}'
    if name == 'blueEggCurrency':
        return '{{Icon|blue egg}}'
    if name == 'orangeEggCurrency':
        return '{{Icon|orange egg}}'
    if name == 'greenEggCurrency':
        return '{{Icon|green egg}}'
    if name == 'goldEggCurrency':
        return '{{Icon|gold egg}}'
    if name == 'platinumEggCurrency':
        return '{{Icon|platinum egg}}'
    if name == 'sapphireEggCurrency':
        return '{{Icon|sapphire egg}}'
    if name == 'garnetEggCurrency':
        return '{{Icon|garnet egg}}'
    if name == 'emeraldEggCurrency':
        return '{{Icon|emerald egg}}'
    if name == 'obsidianEggCurrency':
        return '{{Icon|obsidian egg}}'
    if name == 'atlasEggCurrency':
        return '{{Icon|harbinger egg}}'
    if name == 'vanguardEggCurrency':
        return '{{Icon|vanguard egg}}'
    if name == 'empyreanEggCurrency':
        return '{{Icon|empyrean egg}}'
    return 'ERROR: resource_icon()'

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

def getBuildingLevel(row):
    # building level
    string = '        '+'||{:,}<!--building level-->\n'.format(int(row['level']))
    return string

def getHP(row):
    # hp
    string = '        '+'||{:,}<!--hp-->\n'.format(int(row['HP']))
    return string

def getMaxStorage(row):
    # max storage
    string = '        '+'||'
    max_storage = row['maxStorageData'].split("|")
    for rss in max_storage:
        rss_amt = rss.split(":")
        string += '{:,}'.format(int(rss_amt[1]))
        string += resource_icon(rss_amt[0]) + '<br />'
    string += '<!--max storage-->\n'
    return string

def getRssProtected(row):
    # rss protected
    string = '        '+'||'
    protected = row['storageProtectionData'].split("|")
    for rss in protected:
        rss_amt = rss.split(":")
        string += '{:,}'.format(int(rss_amt[1]))
        string += resource_icon(rss_amt[0]) + '<br />'
    string += '<!--protected-->\n'
    return string

def getPlayerRequirementsStorage(row):
    # player reqirements
    string = '        '+'||'
    if row['levelRequired'] == '':
        string += '{:,}'.format(int('1')) + '{{Icon|player level}}'
    else:
        string += '{:,}'.format(int(row['levelRequired'])) + '{{Icon|player level}}'
    string += ' {:,}'.format(int(buildingdata.getHarvestRateLevel(row['minHourlyHarvestRate'].split("|")[0].split(":")[1]))) + '{{Icon|sheep farm}}'
    string += ' {:,}'.format(int(buildingdata.getHarvestRateLevel(row['minHourlyHarvestRate'].split("|")[0].split(":")[1]))) + '{{Icon|lumber mill}}<!--player requirements-->\n'
    return string

def getPlayerRequirements(row):
    # player reqirements
    string = '        '+'||'
    if row['levelRequired'] == '':
        string += '{:,}'.format(int('1')) + '{{Icon|player level}}'
    else:
        string += '{:,}'.format(int(row['levelRequired'])) + '{{Icon|player level}}'
    string += '<!--player requirements-->\n'
    return string

def getPlayerRequirementsAttackTower(row):
    # player reqirements
    string = '        '+'||'
    if row['levelRequired'] == '':
        string += '{:,}'.format(int('1')) + '{{Icon|player level}}'
    else:
        string += '{:,}'.format(int(row['levelRequired'])) + '{{Icon|player level}}'
    string += ' {:,}'.format(int(row['requiredBuilderLevel'])) + '{{Icon|builder hut}}'
    string += '<!--player requirements-->\n'
    return string

def getUpgradeCost(row):
    # upgrade cost
    string = '        '+'||'
    if row['upgradeCost'] == '':
        string += '<!--upgrade cost-->\n'
        return string
    rss = row['upgradeCost'].split("|")
    for resource in rss:
        cost = resource.split(":")
        if cost[1].isdigit():
            string += '{:,}'.format(int(cost[1])) + resource_icon(cost[0]) + ' '
        else:
            string += '{:,}'.format(int(cost[0])) + resource_icon(cost[1]) + ' '
    string += '<!--upgrade cost-->\n'
    return string

def getUpgradeTime(row):
    # upgrade time
    string = '        '+'||{:}<!--upgrade time-->\n'.format(format_time(row['upgradeTimeInSeconds']))
    return string

def getUpgradeXpReward(row):
    # upgrade xp
    string = '        '+'||{:,}<!--upgrade xp-->\n'.format(int(row['upgradeReward'].split(":")[1]))
    return string

def getAchievementRequirements(row):
    # achievement requirements
    if 'level' in row['achievementRequirements']:
        req =int(row['achievementRequirements'][5:])
        string = '        '+'||{:,}'.format(req) + '{{Icon|player level}}<!--achievement requirements-->\n'
    else:
        string = '        '+'||{:}<!--achievement requirements-->\n'.format(row['achievementRequirements'])
    return string

def getAttackPower(row):
    # attack power
    string = '        '+'||{:,}<!--attack power-->\n'.format(int(row['attackPower']))
    return string

def getDPS(row):
    # attack power
    AP = float(row['attackPower'])
    APS = float(row['attacksPerSecond'])
    string = '        '+'||{:,}<!--DPS-->\n'.format(int(AP*APS))
    return string

def getSpecialAttackPower(row):
    # special attack power
    string = '        '+'||{:,}<!--special attack power-->\n'.format(int(row['specialAttackPower']))
    return string

def getFinalDestructionDamage(row):
    # final destruction damage
    string = '        '+'||{:,}<!--final destruction damage-->\n'.format(int(row['finalDestructionDamage']))
    return string

def getPowerLevel(row):
    # power level
    string = '        '+'||{:,}<!--power level-->\n'.format(int(row['powerLevel']))
    return string

def getDamageReduction(row):
    # damage reduction
    string = '        '+'||{:,}%<!--damage reduction-->\n'.format(int(row['damageReductionPercentage']))
    return string

def getHarvestRate(row):
    # harvest rate
    string = '        '+'||'
    deltaAmt = row['harvestAmount'].split(":")[1]
    deltaTime = row['harvestTimeInSeconds']
    harvestRateHr = float(deltaAmt) / (float(deltaTime)/60/60)
    string += ' {:,}'.format(int(harvestRateHr))
    if row['harvestAmount'].split(":")[0] == 'food':
        string += '{{Icon|food}}'
    else:
        string += '{{Icon|lumber}}'
    return string


storageTable = [
        {'Building<br />Level':getBuildingLevel},
        {'HP':getHP},
        {'Max<br />Storage':getMaxStorage},
        {'Protected':getRssProtected},
        {'Requirements<br />For This Level':getPlayerRequirementsStorage},
        {'Upgrade<br />Cost<br />For This Level':getUpgradeCost},
        {'Upgrade<br />Time<br />For This Level':getUpgradeTime},
        {'Upgrade<br />XP Reward<br /> For This Level':getUpgradeXpReward},
]

baseBuildingTable = [
        {'Building<br />Level':getBuildingLevel},
        {'HP':getHP},
        {'Requirements<br />For This Level':getPlayerRequirements},
        {'Upgrade<br />Cost<br />For This Level':getUpgradeCost},
        {'Upgrade<br />Time<br />For This Level':getUpgradeTime},
        {'Upgrade<br />XP Reward<br /> For This Level':getUpgradeXpReward},
]

guildTable = [
        {'Building<br />Level':getBuildingLevel},
        {'HP':getHP},
        {'Requirements<br />For This Level':getPlayerRequirements},
        {'Upgrade<br />Cost<br />For This Level':getUpgradeCost},
        {'Upgrade<br />Time<br />For This Level':getUpgradeTime},
]

monumentTable = [
        {'Building<br />Level':getBuildingLevel},
        {'HP':getHP},
        {'Achievement<br />Requirements':getAchievementRequirements},
]

runeTable = [
        {'Building<br />Level':getBuildingLevel},
        {'HP':getHP},
        {'Achievement<br />Requirements':getAchievementRequirements},
        {'Upgrade<br />Cost<br />For This Level':getUpgradeCost},
        {'Upgrade<br />Time<br />For This Level':getUpgradeTime},
]

atkTowerTable = [
        {'Building<br />Level':getBuildingLevel},
        {'HP':getHP},
        {'Attack':getAttackPower},
        {'DPS':getDPS},
        {'Special<br />Attack':getSpecialAttackPower},
        {'Power<br />Level':getPowerLevel},
        {'Requirements<br />For This Level':getPlayerRequirementsAttackTower},
        {'Upgrade<br />Cost<br />For This Level':getUpgradeCost},
        {'Upgrade<br />Time<br />For This Level':getUpgradeTime},
        {'Upgrade<br />XP Reward<br /> For This Level':getUpgradeXpReward},
]

atkTowerFireFlakTable = [
        {'Building<br />Level':getBuildingLevel},
        {'HP':getHP},
        {'Attack':getAttackPower},
        {'DPS':getDPS},
        {'Special<br />Attack':getSpecialAttackPower},
        {'Final<br />Destruction<br />Damage':getFinalDestructionDamage},
        {'Power<br />Level':getPowerLevel},
        {'Requirements<br />For This Level':getPlayerRequirementsAttackTower},
        {'Upgrade<br />Cost<br />For This Level':getUpgradeCost},
        {'Upgrade<br />Time<br />For This Level':getUpgradeTime},
        {'Upgrade<br />XP Reward<br /> For This Level':getUpgradeXpReward},
]

mageTowerTable = [
        {'Building<br />Level':getBuildingLevel},
        {'HP':getHP},
        {'Special<br />Attack':getSpecialAttackPower},
        {'Power<br />Level':getPowerLevel},
        {'Requirements<br />For This Level':getPlayerRequirementsAttackTower},
        {'Upgrade<br />Cost<br />For This Level':getUpgradeCost},
        {'Upgrade<br />Time<br />For This Level':getUpgradeTime},
        {'Upgrade<br />XP Reward<br /> For This Level':getUpgradeXpReward},
]

totemTable = [
        {'Building<br />Level':getBuildingLevel},
        {'HP':getHP},
        {'Danage<br />Reduction':getDamageReduction},
        {'Requirements<br />For This Level':getPlayerRequirements},
        {'Upgrade<br />Cost<br />For This Level':getUpgradeCost},
        {'Upgrade<br />Time<br />For This Level':getUpgradeTime},
]

rssTable = [
        {'Building<br />Level':getBuildingLevel},
        {'HP':getHP},
        {'Production/Hour':getHarvestRate},
        {'Requirements<br />For This Level':getPlayerRequirementsAttackTower},
        {'Upgrade<br />Cost<br />For This Level':getUpgradeCost},
        {'Upgrade<br />Time<br />For This Level':getUpgradeTime},
        {'Upgrade<br />XP Reward<br /> For This Level':getUpgradeXpReward},
]

table_format = [
        {'storage':storageTable},
        {'builder':baseBuildingTable},
        {'breedingGround':baseBuildingTable},
        {'incubator':baseBuildingTable},
        {'forge':baseBuildingTable},
        {'stable':baseBuildingTable},
        {'research':baseBuildingTable},
        {'runeBuilding':runeTable},
        {'guild':guildTable},
        {'statues':monumentTable},
        {'lighthouse':monumentTable},
        {'waterGate':monumentTable},
        {'library':monumentTable},
        {'temple':monumentTable},
        {'mountDragon':monumentTable},
        {'tripleTowers':monumentTable},
        {'shrine':monumentTable},
        {'rubyMine':monumentTable},
        {'salvageDepot':monumentTable},
        {'perchIsland03':baseBuildingTable},
        {'perchIsland06':baseBuildingTable},
        {'perchIsland08':baseBuildingTable},
        #
        {'archerTower':atkTowerTable},
        {'cannonTower':atkTowerTable},
        {'stormTower':atkTowerTable},
        {'ballista':atkTowerTable},
        {'trebuchet':atkTowerTable},
        {'lightningTower':atkTowerTable},
        {'iceTurret':atkTowerTable},
        {'fireTurret':atkTowerTable},
        {'elementalFlakDark':atkTowerTable},
        {'elementalFlakFire':atkTowerFireFlakTable},
        {'elementalFlakIce':atkTowerTable},
        {'elementalFlakWind':atkTowerTable},
        {'elementalFlakEarth':atkTowerTable},
        {'crystalHowitzer':atkTowerTable},
        #
        {'mageTower':mageTowerTable},
        {'mageBlueTower':mageTowerTable},
        #
        {'windTotem':totemTable},
        {'earthTotem':totemTable},
        {'darkTotem':totemTable},
        {'fireTotem':totemTable},
        {'iceTotem':totemTable},
        #
        {'hogFarm':rssTable},
        {'woodFarm':rssTable},
]

#Upload options
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

for bld in table_format:
    bldId = bld.keys()[0]
    table_name = bld[bldId]
    print bldId
    upgrade_data = buildingdata.getUpgradeData(bldId)

    table_string = ''
    table_string += '{| class="wikitable" style="text-align: center;"\n'
    table_string += '    |-\n'
    for header in table_name:
        table_string += '        !'+header.keys()[0]+'\n'

    for row in upgrade_data:
        if row['level'] == '0':
            continue
        table_string += '    |-\n'
        for header in table_name:
            table_string += header[header.keys()[0]](row)
    table_string += '|}'

    f = open('output/BUILDING_'+bldId+'.txt', 'w+')
    f.write('<!--bldId-->\n')
    f.write(table_string)
    f.close()

    title = 'Template:'+bldId+'Stats'
    text = table_string

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

