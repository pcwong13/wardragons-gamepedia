#!/usr/bin/env python
import csv
import riderdata
import requests
import wikilogin

# -----------------------------------------------------------------------------
# Main processing loop
# -----------------------------------------------------------------------------

#
# rider skills tree
#
for info in riderdata.info_data:
    f = open('output/'+info['name']+'.tree.txt', 'w+')
    print info['name']

    root = info['rootSkillIdentifier'][:-3]

    tree_string = '==Tree==\n'
    tree_string += '{| class="wikitable" style="text-align: center;"\n'
    tree_string += '    |-\n'
    tree_string += '        !\n'
    for num in range(1,11):
        tree_string += '        !Col<br/>{:}\n'.format(num)

    row6 = []
    row4 = []
    row2 = []
    for row in riderdata.skilltree_data:
        if root in row['identifier']:
            #print row['riderGearIdentifier']
            gear_data = riderdata.getRiderGearData(row['riderGearIdentifier'])
            # Column
            col_num = row['position'].split("~")[0]
            # Row
            row_num = row['position'].split("~")[1]
            # Image
            img = gear_data['iconFilename']
            if row_num == '6':
                row6.append({col_num:'[[Image:'+img+'|32px]]'})
            if row_num == '4':
                row4.append({col_num:'[[Image:'+img+'|32px]]'})
            if row_num == '2':
                row2.append({col_num:'[[Image:'+img+'|32px]]'})

    # Row6
    tree_string += '    |-\n'
    tree_string += '        ||Row=6\n'
    for idx in range (1,11):
        if len(row6):
            if int(row6[0].keys()[0]) == idx:
                tree_string += '        ||{:<48}'.format(row6[0][row6[0].keys()[0]]) + '<!--{:}-->\n'.format(idx)
                row6.pop(0)
            else:
                tree_string += '        ||{:<48}'.format('') + '<!--{:}-->\n'.format(idx)
        else:
            tree_string += '        ||{:<48}'.format('') + '<!--{:}-->\n'.format(idx)
    ### empty row
    tree_string += '    |-\n'
    tree_string += '        ||Row=5 '
    for num in range(1,11):
        tree_string += '|| '
    tree_string += '\n'

    # Row4
    tree_string += '    |-\n'
    tree_string += '        ||Row=4\n'
    for idx in range (1,11):
        if len(row4):
            if int(row4[0].keys()[0]) == idx:
                tree_string += '        ||{:<48}'.format(row4[0][row4[0].keys()[0]]) + '<!--{:}-->\n'.format(idx)
                row4.pop(0)
            else:
                tree_string += '        ||{:<48}'.format('') + '<!--{:}-->\n'.format(idx)
        else:
            tree_string += '        ||{:<48}'.format('') + '<!--{:}-->\n'.format(idx)
    ### empty row
    tree_string += '    |-\n'
    tree_string += '        ||Row=3 '
    for num in range(1,11):
        tree_string += '|| '
    tree_string += '\n'

    # Row2
    tree_string += '    |-\n'
    tree_string += '        ||Row=2\n'
    for idx in range (1,11):
        if len(row2):
            if int(row2[0].keys()[0]) == idx:
                tree_string += '        ||{:<48}'.format(row2[0][row2[0].keys()[0]]) + '<!--{:}-->\n'.format(idx)
                row2.pop(0)
            else:
                tree_string += '        ||{:<48}'.format('') + '<!--{:}-->\n'.format(idx)
        else:
            tree_string += '        ||{:<48}'.format('') + '<!--{:}-->\n'.format(idx)
    ### empty row
    tree_string += '    |-\n'
    tree_string += '        ||Row=1 '
    for num in range(1,11):
        tree_string += '|| '
    tree_string += '\n'

    tree_string += '|}\n'

    f.write(tree_string)
    f.close()

    upload = 1
    title = info['name']
    section = '2'
    text = tree_string

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

