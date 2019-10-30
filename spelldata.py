#!/usr/bin/env python
import csv
import glob

def getSpellData(name):
    for ability in spells:
        if ability.keys()[0] == name:
            return ability[name]

def getDebuffData(name):
    for debuff in debuffs:
        if debuff.keys()[0] == name:
            return debuff[name]

text_by_id = {}

with open('wd/assets/FlavorText.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for num,row in enumerate(reader):
        if num == 0:
            continue
        text_by_id.update({row['identifier']:row['text']})

spell_filename = []
for file in glob.glob('wd/assets/*Spell.csv'):
    spell_filename.append(file.split('/')[-1])


# spells = [ {SpellName: List of row data}, {SpellName: List of row data} ]
spells = []
# dict {SpellName : list}
spell_dict = {}
# list of [rows as dict]
spell_data = []

for filename in spell_filename:
    #print filename
    with open('wd/assets/'+filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for num,row in enumerate(reader):
            # skip header
            if num == 0:
                continue
            # skip consumables
            if row['identifier'].endswith('Cond'):
                continue
            if row['identifier'].endswith('Con'):
                continue
            # skip tutorial
            if row['identifier'].endswith('Tutd'):
                continue
            if row['identifier'].endswith('Tut'):
                continue
            # ??? defense???
            if row['identifier'].endswith('Def'):
                continue
            if row['identifier'].endswith('summonRuneDragon'):
                continue
            spell_data.append(row)
    spell_dict.update({filename[:-4]:spell_data})
    spells.append(spell_dict)

    spell_dict = {}
    spell_data = []


#list of rows as dict
common_data = []
with open('wd/assets/SpellCommon.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for num,row in enumerate(reader):
        # skip header
        if num == 0:
            continue
        common_data.append(row)

#list of rows as dict
resist_data = []
#print filename
with open('wd/assets/ResistAbility.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for num,row in enumerate(reader):
        # skip header
        if num == 0:
            continue
        resist_data.append(row)



debuffs = []
#
debuff_dict = {}
debuff_data = []
with open('wd/assets/FreezeEffect.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for num,row in enumerate(reader):
        # skip header
        if num == 0:
            continue
        debuff_data.append(row)
debuff_dict.update({'freeze':debuff_data})
debuffs.append(debuff_dict)
#
debuff_dict = {}
debuff_data = []
with open('wd/assets/GloomCloudSpellEffect.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for num,row in enumerate(reader):
        # skip header
        if num == 0:
            continue
        debuff_data.append(row)
debuff_dict.update({'gloomCloud':debuff_data})
debuffs.append(debuff_dict)

#dict
attack_type_name_by_id = {}
#print filename
with open('wd/assets/AttackType.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for num,row in enumerate(reader):
        # skip header
        if num == 0:
            continue
        attack_type_name_by_id.update({row['identifier']:row['displayName']})

