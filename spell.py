#!/usr/bin/env python
import spelldata

spell_name_by_id = {}
spell_desc_by_id = {}
spell_type_by_id = {}
spell_color_by_id = {}
spell_icon_by_id = {}
spell_rage_by_id = {}
resist_name_by_id = {}
resist_desc_by_id = {}
resist_icon_by_id = {}

for r_row in spelldata.resist_data:
    resist_name_by_id.update({r_row['identifier']:spelldata.text_by_id[r_row['spellNameIdentifier']]})
    resist_desc_by_id.update({r_row['identifier']:spelldata.text_by_id[r_row['spellDescriptionIdentifier']]})
    resist_icon_by_id.update({r_row['identifier']:r_row['icon']})

for spell_family in spelldata.spells:
    for num,row in enumerate(spell_family[spell_family.keys()[0]]):
        spell_id = ''
        if 'level' in row:
            if not (row['level'] == '1' or row['level'] == '') :
                if row['identifier'] != 'miasmicBreath1':
                    #print 'Skipping %s level %s' % (row['identifier'], row['level'])
                    continue
        if 'commonIdentifier' in row:
            if row['commonIdentifier'] != '':
                spell_id = row['commonIdentifier']
            else:
                spell_id = row['identifier']
        else:
            spell_id = row['identifier']
        name_found = False
        # Lookup by commonIdentifier or identifier
        for c_row in spelldata.common_data:
            if spell_id == c_row['identifier']:
                #print spell_id, spelldata.text_by_id[c_row['spellNameIdentifier']]
                spell_name_by_id.update({row['identifier']:spelldata.text_by_id[c_row['spellNameIdentifier']]})
                spell_desc_by_id.update({row['identifier']:spelldata.text_by_id[c_row['spellDescriptionIdentifier']]})
                spell_type_by_id.update({row['identifier']:c_row['spellTypes']})
                types = c_row['spellTypes'].split("|")
                if types[0] == 'passive':
                    spell_color_by_id.update({row['identifier']:'yellow'})
                    spell_rage_by_id.update({row['identifier']:'passive'})
                else:
                    spell_color_by_id.update({row['identifier']:types[0]})
                    if 'ragePoints' in row:
                        spell_rage_by_id.update({row['identifier']:str(int(row['ragePoints'])/100)})
                    elif 'rageDrainRate':
                        rage_str = str(float(row['rageDrainRate'])/100) + ' Rage per Second'
                        spell_rage_by_id.update({row['identifier']:rage_str})
                    else:
                        spell_rage_by_id.update({row['identifier']:'0'})
                        print row['identifier'], 'no rage found'
                spell_icon_by_id.update({row['identifier']:c_row['icon']})
                name_found = True
                continue
        # Lookup by family or overrides
        if not name_found:
            modified_name = spell_family.keys()[0][:-5]
            modified_name = modified_name[0].lower() + modified_name[1:]
            # overrides
            if modified_name == 'aoe':
                modified_name = 'aoeSpell'
            if modified_name == 'freezeAttack':
                modified_name = 'freezeSpell'
            if modified_name == 'increaseRageGeneration':
                modified_name = 'increaseRage'
            if modified_name == 'frenzy':
                modified_name = 'frenzySpell'
            if modified_name == 'invert':
                modified_name = 'invertSpell'
            if modified_name == 'flux':
                modified_name = 'fluxSpell'
            if modified_name == 'invincible':
                modified_name = 'invincibleSpell'
            if modified_name == 'galvanicOverload':
                modified_name = 'galvanicOverloadSpell'
            if spell_id.startswith('summonDragon'):
                modified_name = 'summonAIDragon'

            for c_row in spelldata.common_data:
                if modified_name == c_row['identifier']:
                    #print spell_id, spelldata.text_by_id[c_row['spellNameIdentifier']]
                    spell_name_by_id.update({row['identifier']:spelldata.text_by_id[c_row['spellNameIdentifier']]})
                    spell_desc_by_id.update({row['identifier']:spelldata.text_by_id[c_row['spellDescriptionIdentifier']]})
                    spell_type_by_id.update({row['identifier']:c_row['spellTypes']})
                    types = c_row['spellTypes'].split("|")
                    if types[0] == 'passive':
                        spell_color_by_id.update({row['identifier']:'yellow'})
                        spell_rage_by_id.update({row['identifier']:'passive'})
                    else:
                        spell_color_by_id.update({row['identifier']:types[0]})
                        if 'ragePoints' in row:
                            spell_rage_by_id.update({row['identifier']:str(int(row['ragePoints'])/100)})
                        elif 'rageDrainRate':
                            rage_str = str(float(row['rageDrainRate'])/100) + ' Rage per Second'
                            spell_rage_by_id.update({row['identifier']:rage_str})
                        else:
                            spell_rage_by_id.update({row['identifier']:'0'})
                            print row['identifier'], 'no rage found'
                    spell_icon_by_id.update({row['identifier']:c_row['icon']})
                    name_found = True
                    continue

#for id in spell_icon_by_id:
#    print "%s: %s" % (id, spell_icon_by_id[id])
#for id in spell_rage_by_id:
#    print "%s: %s" % (id, spell_rage_by_id[id])
#for id in resist_name_by_id:
#    print "%s: %s" % (id, resist_name_by_id[id])

