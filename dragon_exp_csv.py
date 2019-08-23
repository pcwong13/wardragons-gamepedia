#!/usr/bin/env python

import sys
import re
import csv
import den
import storage
import dragon

# DragonClass.csv
dragonClassMultiplier = {
    'hunter' : '2',
    'sorcerer' : '2.25',
    'warrior'  : '10',
    'invoker'  : '2'
}


for dragon_name in dragon.dragon_upgrade_filename_by_name:
    if dragon.dragon_show_in_stable_by_name[dragon_name] == '0':
        continue
    filename = 'wd/assets/'+dragon.dragon_upgrade_filename_by_name[dragon_name]
    print filename

    f = open('output/'+dragon_name+'.upgrade.txt', 'w+')

    #shift xp by 1 row
    previous_xp = '0'
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        f.write('{| class="wikitable" style="text-align: center;"\n')
        f.write('    |-\n')
        f.write('        !DRAGON<br />LEVEL\n')
        f.write('        !HP\n')
        f.write('        !D/SEC\n')
        f.write('        !ATTACK<br />POWER\n')
        f.write('        !PLAYER<br />REQUIREMENTS\n')
        f.write('        !UPGADE<br />XP\n')
        f.write('        !UPGADE<br />COST\n')
        previous_storage = ''
        for num,row in enumerate(reader):
            #skip data type row that follows header row
            if num == 0:
                continue
            f.write('    |-\n')
            #level
            f.write('        ||{:<16}'.format(row['level']))
            #hp
            hp_str = '{:,}'.format(int(row['HP']))
            f.write('||{:<16}'.format(hp_str))
            #dps
            damage = float(row['attackPower']) * float(dragonClassMultiplier[dragon.dragon_class_by_name[dragon_name]])
            dps = '{:,}'.format(int(round(damage)))
            f.write('||{:<16}'.format(dps))
            #AP
            ap = '{:,}'.format(int(row['powerLevel']))
            f.write('||{:<16}'.format(ap))
            #player
            stable = row['requiredStableLevel']
            req_str = den.get_player(stable)
            req_str += '{{Icon|player level}} '
            #den
            req_str += stable
            req_str += '{{Icon|dragons den}} '
            #storage
            upgrade_cost = row['upgradeCost']
            if upgrade_cost != '':
                upgrade_fields = upgrade_cost.split(":")
                if upgrade_fields[0] == 'food':
                    previous_storage = storage.get_storage(upgrade_fields[1])
                    req_str += storage.get_storage(upgrade_fields[1])
                    req_str += '{{Icon|storage hut}}'
                if 'Stone' in upgrade_fields[0]:
                    req_str += previous_storage
                    req_str += '{{Icon|storage hut}}'
            f.write('||{:<80}'.format(req_str))
            #xp
            xp_str = '{:,}'.format(int(previous_xp))
            previous_xp = row['upgradeXP']
            xp_str += '{{Icon|xp}}'
            f.write('||{:<28}'.format(xp_str))
            #rss
            if 'Stone' in upgrade_fields[0]:
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
            else:
                if upgrade_cost != '':
                    rss_str = '{:,}'.format(int(upgrade_fields[1]))
                    if upgrade_fields[0] == 'food':
                        rss_str += '{{Icon|food}}'
            f.write('||{:}\n'.format(rss_str))
        f.write('|}\n')
    f.close()

