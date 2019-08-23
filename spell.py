#!/usr/bin/env python
import csv

text_by_id = {}
spell_name_by_id = {}
spell_desc_by_id = {}
spell_type_by_id = {}
resist_name_by_id = {}
resist_desc_by_id = {}

with open('wd/assets/FlavorText.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for num,row in enumerate(reader):
        if num == 0:
            continue
        text_by_id.update({row['identifier']:row['text']})

with open('wd/assets/SpellCommon.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for num,row in enumerate(reader):
        if num == 0:
            continue
        spell_name_by_id.update({row['identifier']:text_by_id[row['spellNameIdentifier']]})
        spell_desc_by_id.update({row['identifier']:text_by_id[row['spellDescriptionIdentifier']]})
        spell_type_by_id.update({row['identifier']:row['spellTypes']})

with open('wd/assets/ResistAbility.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for num,row in enumerate(reader):
        if num == 0:
            continue
        resist_name_by_id.update({row['identifier']:text_by_id[row['spellNameIdentifier']]})
        resist_desc_by_id.update({row['identifier']:text_by_id[row['spellDescriptionIdentifier']]})

spell_filename = {
'AbsorbMagicSpell.csv',            'DesiccatingSandSpell.csv',        'HeatBlastShieldSpell.csv',        'SacrificeSpell.csv',
'AdaptiveBreathSpell.csv',         'DevourHopeSpell.csv',             'HeatedPiercingBreathSpell.csv',   'SeekerShotsSpell.csv',
'AdaptiveResistSpell.csv',         'DissipateSpell.csv',              'HoverSpell.csv',                  'SeethingSparkSpell.csv',
'AlterFateSpell.csv',              'DodgeSpell.csv',                  'HurricaneSpell.csv',              'ShadowApophetSpell.csv',
'AoeSpell.csv',                    'DreadfulRoarSpell.csv',           'IncreaseRageGenerationSpell.csv', 'ShattershardSpell.csv',
'BattlecrySpell.csv',              'ElementalBarrierSpell.csv',       'InstantKillSpell.csv',            'ShieldAssaultSpell.csv',
'BerserkSpell.csv',                'EnergySyphonSpell.csv',           'IntimidatingRoarSpell.csv',       'ShortCircuitSpell.csv',
'BloodFurySpell.csv',              'ExplosiveAegisSpell.csv',         'InvertSpell.csv',                 'SouthernCrossSpell.csv',
'BorrowTimeSpell.csv',             'FerociousBarrierSpell.csv',       'InvincibleSpell.csv',             'SpeedBoostSpell.csv',
'CelestialDanceSpell.csv',         'FluxSpell.csv',                   'IsolationSpell.csv',              'StarburnSpell.csv',
'ChainLightningSpell.csv',         'FreezeAttackSpell.csv',           'KamikazeSpell.csv',               'StealEssenceSpell.csv',
'ChargedShieldSpell.csv',          'FrenzySpell.csv',                 'LightSpeedSpell.csv',             'StoneskinSpell.csv',
'CloakSpell.csv',                  'FrostbiteSpell.csv',              'LockdownSpell.csv',               'SummonAIBattleDragonSpell.csv',
'ConsumeSpell.csv',                'FrozenTombSpell.csv',             'MaleficBreathSpell.csv',          'TeleportSpell.csv',
'CosmicEnergySpell.csv',           'FuryOfTheWastesSpell.csv',        'NightfallSpell.csv',              'ThunderstormSpell.csv',
'CrumbleToDustSpell.csv',          'GalvanicOverloadSpell.csv',       'NocturnalFissureSpell.csv',       'TimeShiftSpell.csv',
'CrystallineShieldSpell.csv',      'GloomAndDoomSpell.csv',           'NorthernLightsSpell.csv',         'UmbralSpikeSpell.csv',
'CurePoisonSpell.csv',             'HealDragonSpell.csv',             'NovaSpell.csv',                   'UndyingWillSpell.csv',
'DaybreakSpell.csv',               'HealingMarkSpell.csv',            'RadianceSpell.csv',
'DeflectingGaleSpell.csv',         'HealthRageDeathMarkSpell.csv',    'RisingPhoenixSpell.csv'
}

for filename in spell_filename:
    #print filename
    with open('wd/assets/'+filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for num,row in enumerate(reader):
            # skip header
            if num == 0:
                continue
            # skip consumables
            if row['identifier'].endswith('Con'):
                continue
            # skip tutorial
            if row['identifier'].endswith('Tut'):
                continue
            # ??? defense???
            if row['identifier'].endswith('Def'):
                continue
            # has column 'commonIdentifier'
            try:
                if row['commonIdentifier'] == '':
                    try:
                        spell_name_by_id.update({row['identifier']:spell_name_by_id[row['identifier']]})
                    except:
                        # rename summonDragon to summonAIDragon
                        if row['identifier'].startswith('summonDragon'):
                            spell_name_by_id.update({row['identifier']:spell_name_by_id['summonAIDragon']})
                        # rename selfDestruct to kamikaze
                        elif row['identifier'].startswith('selfDestruct'):
                            spell_name_by_id.update({row['identifier']:spell_name_by_id['kamikaze']})
                        # take the filename instead of xxx1
                        elif row['identifier'].endswith(('0','1','2','3','4','5','6','7','8','9')):
                            # remove Spell.csv
                            filename_mod1 = filename[:-9]
                            filename_mod2 = filename_mod1[0].lower() + filename_mod1[1:]
                            # rename freezeAttack to freezeSpell
                            if filename_mod2 == 'freezeAttack':
                                filename_mod2 = 'freeze'
                            # rename increaseRageGeneration to increaseRage
                            if filename_mod2 == 'increaseRageGeneration':
                                filename_mod2 = 'increaseRage'
                            try:
                                spell_name_by_id.update({row['identifier']:spell_name_by_id[filename_mod2]})
                            except:
                                filename_mod3= filename_mod2 + 'Spell'
                                spell_name_by_id.update({row['identifier']:spell_name_by_id[filename_mod3]})

                else:
                    #print spell_name_by_id[row['commonIdentifier']]
                    spell_name_by_id.update({row['identifier']:spell_name_by_id[row['commonIdentifier']]})
            # does not has column 'commonIdentifier'
            except:
                    try:
                        spell_name_by_id.update({row['identifier']:spell_name_by_id[row['identifier']]})
                    except:
                        # rename summonDragon to summonAIDragon
                        if row['identifier'].startswith('summonDragon'):
                            spell_name_by_id.update({row['identifier']:spell_name_by_id['summonAIDragon']})
                        # rename selfDestruct to kamikaze
                        elif row['identifier'].startswith('selfDestruct'):
                            spell_name_by_id.update({row['identifier']:spell_name_by_id['kamikaze']})
                        # take the filename instead of xxx1
                        elif row['identifier'].endswith(('0','1','2','3','4','5','6','7','8','9')):
                            # remove Spell.csv
                            filename_mod1 = filename[:-9]
                            filename_mod2 = filename_mod1[0].lower() + filename_mod1[1:]
                            # rename freezeAttack to freezeSpell
                            if filename_mod2 == 'freezeAttack':
                                filename_mod2 = 'freeze'
                            # rename increaseRageGeneration to increaseRage
                            if filename_mod2 == 'increaseRageGeneration':
                                filename_mod2 = 'increaseRage'
                            try:
                                spell_name_by_id.update({row['identifier']:spell_name_by_id[filename_mod2]})
                            except:
                                filename_mod3= filename_mod2 + 'Spell'
                                spell_name_by_id.update({row['identifier']:spell_name_by_id[filename_mod3]})

