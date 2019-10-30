#!/usr/bin/env python
import csv
import glob
import buildingdata
import spell
import spelldata
import requests
import wikilogin


def createSwitchStatement(key):
    #print key
    string = '-->{{#vardefine:'+key+'\n|{{#switch: {{{1|{{{id}}}}}}\n'

    for row in spell_data:
        string += '|'+row['identifier']+' = '
        if key == 'absorbBattleBuildingIds':
            buildingId = row[key].split("|")
            for bId in buildingId:
                string += '[['+buildingdata.name_by_id[bId] + ']]<br />'
            string = string[:-6] + '\n'
        elif key in tower_id:
            spellId = row[key].split(":")
            string += '{{Abilities|Ability='+spellId[1]+'}}\n'
        elif key == 'spellIdentifiers':
            spellids = row[key].split("|")
            for spellItem in spellids:
                spellId = spellItem.split(":")
                string += '{{Abilities|Ability='+spellId[1]+'}}<br />'
            string = string[:-6] + '\n'
        elif key == 'protectedAttackTypes':
            attackTypes = row[key].split("|")
            for types in attackTypes:
                atkId = types.split(":")
                string += spelldata.attack_type_name_by_id[atkId[0]] + ' ' + atkId[1] + '%<br />'
            string += '\n'
        elif key == 'ragePoints':
            string += str(int(row[key])/100)+'\n'
        elif key == 'rageBonus':
            string += str(float(row[key])/100)+'\n'
        elif key == 'ragePointsBonus':
            string += str(float(row[key])/100)+'\n'
        elif key == 'ragePointsRestored':
            string += str(float(row[key])/100)+'\n'
        elif key == 'empoweredRageBonus':
            string += str(float(row[key])/100)+'\n'
        elif key == 'rageToRestore':
            string += str(float(row[key])/100)+'\n'
        elif key == 'damageAsPercentageOfMaxHP':
            if row[key] == '':
                string += '0\n'
            else:
                string += str(float(row[key])*100)+'\n'
        elif key == 'affectDamageAsPercentageOfMaxHP':
            if row[key] == '':
                string += '0\n'
            else:
                string += str(float(row[key])*100)+'\n'
        elif key == 'freezeDamagePercentOfMaxHP':
            string += str(float(row[key])*100)+'\n'
        elif key == 'shatterDamagePercentOfMaxHP':
            string += str(float(row[key])*100)+'\n'
        elif key == 'healAsPercentageOfMaxHP':
            if float(row['healAsPercentageOfMaxHP']) <= 1:
                string += str(float(row[key])*100)+'\n'
            else:
                string += row[key]+'\n'
        elif key == 'percentHPHeal':
            string += str(float(row[key])*100)+'\n'
        elif key == 'hpHealPercentage':
            string += str(float(row[key])*100)+'\n'
        elif key == 'rageDrainRate':
            string += str(float(row[key])/100)+'\n'
        elif key == 'speedMultiplier':
            string += str(float(row[key])*100)+'\n'
        elif key == 'canUseSpells':
            string += 'Yes' if row[key] == '1' else 'No' +'\n'
        elif key == 'canAttack':
            string += 'Yes' if row[key] == '1' else 'No' +'\n'
        elif key == 'alwaysHasCooldown':
            string += 'Yes' if row[key] == '1' else 'No' +'\n'
        elif key == 'shouldNormalDamageHitDisabledTowers':
            string += 'Yes' if row[key] == '1' else 'No' +'\n'
        elif key == 'usableDelayForEachSpell':
            string += row[key].replace('|',',') + '\n'
        elif key == 'attackPowerAsPercentOfDragonHP':
            string += str(float(row[key])*100)+'\n'
        elif key == 'hpAsPercentOfDragonHP':
            string += str(float(row[key])*100)+'\n'
        else:
            if row[key] == '':
                string += '0\n'
            else:
                string += row[key]+'\n'
    string += '|#default = error\n}} }}<!--\n'
    return string

def createSwitchStatementDebuff():
    string = ''
    debuff_data = spelldata.getDebuffData('gloomCloud')
    for debuff_key in debuff_data[0].keys():
        if debuff_key in skip_list:
            continue
        string += '-->{{#vardefine:'+debuff_key+'\n|{{#switch: {{#var:debuffEffectInfoIdentifier}}\n'

        for row in debuff_data:
            string += '|'+row['identifier']+' = '
            if debuff_key == 'damagePerSecond':
                string += str(float(row[debuff_key])*100)+'\n'
            else:
                if row[debuff_key] == '':
                    string += '0\n'
                else:
                    string += row[debuff_key]+'\n'
        string += '|#default = error\n}} }}<!--\n'
    debuff_data = spelldata.getDebuffData('freeze')
    for debuff_key in debuff_data[0].keys():
        if debuff_key in skip_list:
            continue
        string += '-->{{#vardefine:'+debuff_key+'\n|{{#switch: {{#var:debuffEffectInfoIdentifier}}\n'

        for row in debuff_data:
            string += '|'+row['identifier']+' = '
            if debuff_key == 'damagePerSecond':
                string += str(float(row[debuff_key])*100)+'\n'
            else:
                if row[debuff_key] == '':
                    string += '0\n'
                else:
                    string += row[debuff_key]+'\n'
        string += '|#default = error\n}} }}<!--\n'
    return string

def createAbilityMeta():
    metadata = '<!--'
    debuff = ''
    for key in spell_data[0].keys():
        if key in skip_list:
            continue
        metadata += createSwitchStatement(key)
        if key == 'debuffType':
            debuff += createSwitchStatementDebuff()
    metadata += debuff + '-->'
    return metadata

def getTableFormat(name):
    for spec in table_format:
        if spec.keys()[0] == name:
            return spec[name]

def createTable(name):
    table_string = ''
    table_string += '{| class="wikitable"\n'
    table_string += '    |-\n'
    table_string += '        !style="text-align: right"|Field\n'
    table_string += '        !style="text-align: left"|Description\n'
    table_string += '    |-\n'
    table_string += '        |style="text-align: right"|Ability Family\n'
    table_string += '        |style="text-align: left"|' + name + '\n'
    table_string += '    |-\n'
    table_string += '        |style="text-align: right"|Max # of Casts\n'
    table_string += '        |style="text-align: left"|{{#var:maxTimes}} times\n'
    for field in getTableFormat(name):
        key = field.keys()[0]
        table_string += '    |-\n'
        table_string += '        |style="text-align: right"|'+key+'\n'
        table_string += '        |style="text-align: left"|'+field[key]+'\n'
        if key == debuffType:
            table_string += '    |-\n'
            table_string += '        {{#ifeq:{{#var:debuffType}}|gloomCloud| {{!}}style="text-align: right"{{!}}Gloom Cloud ' + damagePerSecond + '}}\n'
            table_string += '        {{#ifeq:{{#var:debuffType}}|freeze| {{!}}style="text-align: right"{{!}}Freeze ' + frozenDuration + '}}\n'
            table_string += '        {{#ifeq:{{#var:debuffType}}|gloomCloud| {{!}}style="text-align: left"{{!}}{{#var:damagePerSecond}}%}}\n'
            table_string += '        {{#ifeq:{{#var:debuffType}}|freeze| {{!}}style="text-align: left"{{!}}{{#var:frozenDuration}} sec}}\n'
            table_string += '    |-\n'
            table_string += '        {{#ifeq:{{#var:debuffType}}|gloomCloud| {{!}}style="text-align: right"{{!}}Gloom Cloud ' + damageDuration + '}}\n'
            table_string += '        {{#ifeq:{{#var:debuffType}}|gloomCloud| {{!}}style="text-align: left"{{!}}{{#var:damageDuration}} sec}}\n'
    table_string += '|}\n'
    return table_string

def createFamily():
    string = '\n==Abilities in This Family==\n'
    for row in spell_data:
        if row['identifier'] in skip_family_list:
            continue
        try:
            if row['level'] != '':
                if not (int(row['level']) == 1):
                    continue
        except:
            pass
        string += '{{Abilities|' + row['identifier'] + '}}<br />\n'
    return string

#configuration
file_skip_list = ['SpeedBoostSpell.csv','HoverSpell.csv','TeleportSpell.csv','IncreaseRageGenerationSpell.csv']
skip_list = ['identifier', 'commonIdentifier', 'particleFlightDuration','projectileBlockedTextIdentifier',
    'distanceAhead','dragonType','dragonScale','h','battleTextIdentifier']
tower_id =  ['archerTower','cannonTower','ballista','stormTower','trebuchet','lightningTower','mageTower','mageBlueTower','iceTurret','fireTurret',
    'elementalFlakDark','elementalFlakFire','elementalFlakIce','elementalFlakWind','elementalFlakEarth',
    'darkTotem','fireTotem','iceTotem','windTotem','earthTotem','woodFarm','hogFarm','perchIsland03','perchIsland06','perchIsland08']
skip_family_list = ['adaptiveBreath2',
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

#Field text
duration = 'Duration'
damageReductionPercentage = 'Incoming Damage Reduction'
cooldown = 'Cooldown'
#
ragePoints = 'Rage Points'
rageDrainRate = 'Rage Points'
rageBonus = 'Rage Gain per Cast'
percentageIncrease = 'Increased Rage Generation'
ragePointsRestored = 'Rage Gain per Cast'
rageIncreasePercentage= 'Rage Increase'
rageToRestore = 'Rage Bonus per Building Destroyed'
rageReturnOnAttack = 'Rage Returned on Attack'
empoweredRageBonus = 'Empowered Rage Bonus'
rageRegenerationPercentage = 'Rage Regeneration % of Normal'
ragePointsBonus = 'Rage Gain per Cast'
ragePercentageIncrease = 'Rage Regeneration Increase'
#
range = 'Range'
splashRange = 'AOE Radius'
buildingAffectRange = 'AOE Radius'
damageRadius = 'AOE Radius'
abilityRadius = 'Ability Radius'
energyRadius = 'Energy Radius'
radius = 'AOE Radius'
explosionRadius = 'Explosion Radius'
chainRange = 'Range for Chain'
#
healAsPercentageOfMaxHP = 'Heal as % of Max HP'
percentHPHeal = 'Heal as % of Max HP'
hpHealPercentage = 'Heal as % of Max HP'
healthBonus = 'Health Gain per Cast'
maxPercentageCanBeHealed = 'Max Heal Amount'
healthReturnOnAttack = 'Health Returned on Attack'
healTime = 'Heal Time'
#
damageReducePercent = 'Tower Attack Reduced'
damageAsPercentageOfMaxHP = 'Damage Inflicted as % of Max HP'
attackBonusPercentage = 'Attack Bonus'
ammoCostReducedPercentage = 'Reduced Ammo Cost per [[Fireball Attack]]'
attackPowerReducedPercentage = 'Reduced Attack Power'
damageConvertToHPPercentage = 'Damage Inflicted Converted to HP'
protectedAttackTypes = 'Protection From Attack Types'
refreshInterval = 'Refresh Interval'
attackPowerPercentageCap = 'Attack Bonus % Cap'
attackPowerReductionPercentageFromTargetBuilding = 'Target Tower Attack Reduction'
attackPowerReductionPercentageFromOtherBuildings = 'Nearby Tower Attack Reduction'
archerTower = 'Spell Stolen From [[Archer Tower]]'
cannonTower = 'Spell Stolen From [[Cannon Tower]]'
ballista = 'Spell Stolen From [[Ballista]]'
stormTower = 'Spell Stolen From [[Storm Tower]]'
trebuchet = 'Spell Stolen From [[Trebuchet]]'
lightningTower = 'Spell Stolen From [[Lightning Tower]]'
mageTower = 'Spell Stolen From [[Red Mage Tower]]'
mageBlueTower = 'Spell Stolen From [[Blue Mage Tower]]'
iceTurret = 'Spell Stolen From [[Ice Turret]]'
fireTurret = 'Spell Stolen From [[Fire Turret]]'
elementalFlakDark = 'Spell Stolen From [[Dark Flak]]'
elementalFlakFire = 'Spell Stolen From [[Fire Flak]]'
elementalFlakIce = 'Spell Stolen From [[Ice Flak]]'
elementalFlakWind = 'Spell Stolen From [[Wind Flak]]'
elementalFlakEarth = 'Spell Stolen From [[Earth Flak]]'
darkTotem = 'Spell Stolen From All Totems'
woodFarm = 'Spell Stolen From [[Lumber Mill]]'
hogFarm = 'Spell Stolen From [[Sheep Farm]]'
perchIsland08 = 'Spell Stolen From All Perches'
reduceBuildingPowerPercent = 'Tower Attack Reduced'
increaseBuildingDamagePercent = 'Increase Building Damage Received'
rounds = 'Number of Rounds'
affectDamageAsPercentageOfMaxHP = 'AOE Damage as & of Max HP'
crystallineShardAmount = 'Number of Protective Shards'
beamDamagePercentOfNormalDamage = 'Tower Beam Damage Reduction'
damageIntervalSecond = 'Damage Interval'
ammoRechargePercentage = 'Ammo Recharge'
speedMultiplier = 'Flying Speed % of Normal'
dodgePercentage = 'Chance of Dodging Incoming Projectile and Supershots'
attackPowerAsPercentOfDragonHP = 'Summon Attack Power as % of Dragon HP'
hpAsPercentOfDragonHP = 'Summon HP as % of Dragon HP'
delayToActivateDragon = 'Summon Activation Delay'
timeIntervalBetweenBolts = 'Time Interval Between Bolts'
chains = 'Number of Towers Hit by Chain'
ammoRefundPerShard = 'Ammo Refund Per Shard'
hpSacrificedPercentage = 'HP Sacrified'
absorbBattleBuildingIds = 'Absorb Supershots<br /> to Gain 2 Rage From'
resistTypes = 'Resist Types'
spellActivationTriggerDragonHPPercentage = 'When HP is Below'
damagePercentageIncreaseModifier = 'Damage Done is Increased By'
immediateAttackMultiplier = 'Target Takes Multiplier of Dragon\'s Attack Power as Damage'
solarEnergyMaxEnergy = 'Solar Energy Needed to Transform'
solarEnergyPerTower = 'Solar Energy Gained Per Tower Destroyed'
attackPercentageModifier = 'Attack Bonus'
solarEnergyBonusPerTower = 'Solar Energy Bonus Gained Per Tower Destroyed'
empoweredDuration = 'Empowered Duration'
chargeTime = 'After'
shieldAsPercentageOfMaxHP = 'Shield as % of Max HP'
stunDuration = 'Stun Duration'
numberOfProjectiles = 'Number of Projectiles'
maxTargets = 'Max Number of Targets'
debuffType = 'Debuff Type'
damageScalingThreshold = 'Damage Scaling Threshold'
ammoRegenPercentage = 'Ammo Regeneration % of Normal'
durationPerShard = 'Duration Per Shard'
temporalShards = 'Number of Shards'
ammoConvertToHPPercentage = 'Ammo Converted to HP %'
increasedAmmoRegenRateMultiplier = 'Ammo Regen Multiplier'
consumedAmmoPercentage = 'Consumed Ammo %'
usableDelayForEachSpell = 'Usable Delay for Each Spell'
spellIdentifiers = 'Spell Rotation'
empoweredDamagePercentageApplied = 'Damage Infliced to Dragon'
solarEnergyBonusPerShot = 'Solar Energy Bonus Gained Per Shot'
percentageOfDamageAbsorbed = 'Summon Absorbs % of Incoming Damage'
frozenDuration = 'Frozen Duration'
freezeDamagePercentOfMaxHP = 'Freeze Damage % of Max HP'
shatterDamagePercentOfMaxHP = 'Shatter Damage % of Max HP'
allowDamageTime = 'Number of His Before Freeing'
damageAbsorbedPercentage = 'Damaged Absorbed %'
attackBonusCapPercentage = 'Attack Bonus Cap'
canUseSpells = 'Can Use Spells While Cloaked'
canAttack = 'Can Attack While Cloaked'
alwaysHasCooldown = 'Always Has A Cooldown'
percentageIncreasedDamage = 'Tower Damage Increase Taken'
damagePercentageApplied = 'Damage Infliced to Dragon'
shouldNormalDamageHitDisabledTowers = 'Damage Removes Disabled Tower Effect'
damagePerSecond = 'Damage Inflicted Per Second as % of Max HP'
damageDuration = 'Damage Duration'

AbsorbMagicTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {duration:'{{#var:duration}} sec'},
    {cooldown:'{{#var:cooldown}} sec'},
    {damageReductionPercentage:'{{#var:damageReductionPercentage}}%'},
    {absorbBattleBuildingIds:'{{#var:absorbBattleBuildingIds}}'},
    {'Shield Break':'Breakable by [[Ice Flak]]'},
]
IntimidatingRoarTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {cooldown:'{{#var:cooldown}} sec'},
    {damageAsPercentageOfMaxHP:'{{#var:damageAsPercentageOfMaxHP}}%'},
    {explosionRadius:'{{#var:explosionRadius}}'},
    {damageReducePercent:'{{#var:damageReducePercent}}%'},
]
AdaptiveResistTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {cooldown:'{{#var:cooldown}} sec'},
    {rageBonus:'{{#var:rageBonus}}'},
    {resistTypes:'{{#var:resistTypes}}'},
]
EnergySyphonTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {duration:'{{#var:duration}} sec'},
    {percentHPHeal:'{{#var:percentHPHeal}}%'},
    {rageToRestore:'{{#var:rageToRestore}}'},
]
FrenzyTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {duration:'{{#var:duration}} sec'},
    {attackBonusPercentage:'{{#var:attackBonusPercentage}}%'},
]
StarburnTable = [
    {spellActivationTriggerDragonHPPercentage:'{{#var:spellActivationTriggerDragonHPPercentage}}%'},
    {damagePercentageIncreaseModifier:'{{#var:damagePercentageIncreaseModifier}}%'},
]
ShieldAssaultTable = [
    {rageDrainRate:'{{#var:rageDrainRate}} per sec'},
    {attackBonusPercentage:'{{#var:attackBonusPercentage}}%'},
    {damageReductionPercentage:'{{#var:damageReductionPercentage}}%'},
]
LightSpeedTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {duration:'{{#var:duration}} sec'},
    {cooldown:'{{#var:cooldown}} sec'},
    {explosionRadius:'{{#var:explosionRadius}}'},
    {damageAsPercentageOfMaxHP:'{{#var:damageAsPercentageOfMaxHP}}%'},
    {ammoCostReducedPercentage:'{{#var:ammoCostReducedPercentage}}%'},
    {attackPowerReducedPercentage:'{{#var:attackPowerReducedPercentage}}%'},
]
ElementalBarrierTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {duration:'{{#var:duration}} sec'},
    {cooldown:'{{#var:cooldown}} sec'},
    {damageConvertToHPPercentage:'{{#var:damageConvertToHPPercentage}}%'},
    {maxPercentageCanBeHealed:'{{#var:maxPercentageCanBeHealed}}%'},
    {protectedAttackTypes:'{{#var:protectedAttackTypes}}'},
]
IncreaseRageGenerationTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {duration:'{{#var:duration}} sec'},
    {percentageIncrease:'{{#var:percentageIncrease}}%'},
]
FuryOfTheWastesTable = [
    {refreshInterval:'{{#var:refreshInterval}} sec'},
    {healAsPercentageOfMaxHP:'{{#var:healAsPercentageOfMaxHP}}%'},
    {attackBonusPercentage:'{{#var:attackBonusPercentage}}%'},
    {attackPowerPercentageCap:'{{#var:attackPowerPercentageCap}}%'},
]
IsolationTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {duration:'{{#var:duration}} sec'},
    {cooldown:'{{#var:cooldown}} sec'},
    {range:'{{#var:range}}'},
    {attackPowerReductionPercentageFromTargetBuilding:'{{#var:attackPowerReductionPercentageFromTargetBuilding}}%'},
    {attackPowerReductionPercentageFromOtherBuildings:'{{#var:attackPowerReductionPercentageFromOtherBuildings}}%'},
]
StealEssenceTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {cooldown:'{{#var:cooldown}} sec'},
    {rageBonus:'{{#var:rageBonus}}'},
    {healthBonus:'{{#var:healthBonus}}'},
]
CrumbleToDustTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {cooldown:'{{#var:cooldown}} sec'},
    {reduceBuildingPowerPercent:'{{#var:reduceBuildingPowerPercent}}'},
    {increaseBuildingDamagePercent:'{{#var:increaseBuildingDamagePercent}}'},
    {splashRange:'{{#var:splashRange}}'},
]
BattlecryTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {cooldown:'{{#var:cooldown}} sec'},
    {rounds:'{{#var:rounds}}'},
    {attackBonusPercentage:'{{#var:attackBonusPercentage}}%'},
]
InvertTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {duration:'{{#var:duration}} sec'},
    {attackBonusPercentage:'{{#var:attackBonusPercentage}}'},
]
HurricaneTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {duration:'{{#var:duration}} sec'},
]
FluxTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {cooldown:'{{#var:cooldown}} sec'},
    {range:'{{#var:range}}'},
    {damageAsPercentageOfMaxHP:'{{#var:damageAsPercentageOfMaxHP}}%'},
    {buildingAffectRange:'{{#var:buildingAffectRange}}'},
    {affectDamageAsPercentageOfMaxHP:'{{#var:affectDamageAsPercentageOfMaxHP}}%'},
    {healAsPercentageOfMaxHP:'{{#var:healAsPercentageOfMaxHP}}%'},
    {ragePointsRestored:'{{#var:ragePointsRestored}}'},
]
CrystallineShieldTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {duration:'{{#var:duration}} sec'},
    {cooldown:'{{#var:cooldown}} sec'},
    {crystallineShardAmount:'{{#var:crystallineShardAmount}}'},
    {beamDamagePercentOfNormalDamage:'{{#var:beamDamagePercentOfNormalDamage}}%'},
]
DeflectingGaleTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {duration:'{{#var:duration}} sec'},
    {cooldown:'{{#var:cooldown}} sec'},
    {damageAsPercentageOfMaxHP:'{{#var:damageAsPercentageOfMaxHP}}%'},
    {damageRadius:'{{#var:damageRadius}}'},
    {damageIntervalSecond:'{{#var:damageIntervalSecond}} sec'},
    {ammoRechargePercentage:'{{#var:ammoRechargePercentage}}%'},
    {speedMultiplier:'{{#var:speedMultiplier}}%'},
    {dodgePercentage:'{{#var:dodgePercentage}}%'},
]
SummonAIBattleDragonTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {delayToActivateDragon:'{{#var:delayToActivateDragon}} sec'},
    {attackPowerAsPercentOfDragonHP:'{{#var:attackPowerAsPercentOfDragonHP}}%'},
    {hpAsPercentOfDragonHP:'{{#var:hpAsPercentOfDragonHP}}%'},
]
RadianceTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {attackBonusPercentage:'{{#var:attackBonusPercentage}}%'},
    {healAsPercentageOfMaxHP:'{{#var:healAsPercentageOfMaxHP}}%'},
    {damageAsPercentageOfMaxHP:'{{#var:damageAsPercentageOfMaxHP}}%'},
    {explosionRadius:'{{#var:explosionRadius}}'},
]
ThunderstormTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {duration:'{{#var:duration}} sec'},
    {range:'{{#var:range}}'},
    {timeIntervalBetweenBolts:'{{#var:timeIntervalBetweenBolts}} sec'},
    {damageAsPercentageOfMaxHP:'{{#var:damageAsPercentageOfMaxHP}}%'},
]
ChainLightningTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {chains:'{{#var:chains}}'},
    {chainRange:'{{#var:chainRange}}'},
    {damageAsPercentageOfMaxHP:'{{#var:damageAsPercentageOfMaxHP}}%'},
]
ShattershardTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {damageAsPercentageOfMaxHP:'{{#var:damageAsPercentageOfMaxHP}}%'},
    {ammoRefundPerShard:'{{#var:ammoRefundPerShard}}'},
    {abilityRadius:'{{#var:abilityRadius}}'},
]
BerserkTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {duration:'{{#var:duration}} sec'},
    {cooldown:'{{#var:cooldown}} sec'},
    {attackBonusPercentage:'{{#var:attackBonusPercentage}}%'},
    {hpSacrificedPercentage:'{{#var:hpSacrificedPercentage}}%'},
    {healAsPercentageOfMaxHP:'{{#var:healAsPercentageOfMaxHP}}%'},
    {rageIncreasePercentage:'{{#var:rageIncreasePercentage}}%'}
]
UmbralSpikeTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {cooldown:'{{#var:cooldown}} sec'},
    {immediateAttackMultiplier:'{{#var:immediateAttackMultiplier}}x'},
    {healAsPercentageOfMaxHP:'{{#var:healAsPercentageOfMaxHP}}%'},
]
NightfallTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {attackBonusPercentage:'{{#var:attackBonusPercentage}}%'},
]
DaybreakTable = [
    {solarEnergyPerTower:'{{#var:solarEnergyPerTower}}'},
    {solarEnergyMaxEnergy:'{{#var:solarEnergyMaxEnergy}}'},
]
RisingPhoenixTable =[
    {ragePoints:'{{#var:ragePoints}}'},
    {duration:'{{#var:duration}} sec'},
    {cooldown:'{{#var:cooldown}} sec'},
    {damageAsPercentageOfMaxHP:'{{#var:damageAsPercentageOfMaxHP}}%'},
    {damageRadius:'{{#var:damageRadius}}'},
    {healAsPercentageOfMaxHP:'{{#var:healAsPercentageOfMaxHP}}%'},
]
CosmicEnergyTable = [
    {attackPercentageModifier:'{{#var:attackPercentageModifier}}%'},
    {healthReturnOnAttack:'{{#var:healthReturnOnAttack}}'},
    {rageReturnOnAttack:'{{#var:rageReturnOnAttack}}'},
]
DodgeTable =[
    {ragePoints:'{{#var:ragePoints}}'},
    {duration:'{{#var:duration}} sec'},
    {cooldown:'{{#var:cooldown}} sec'},
    {speedMultiplier:'{{#var:speedMultiplier}}%'},
    {dodgePercentage:'{{#var:dodgePercentage}}%'},
]
HealingMarkTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {healAsPercentageOfMaxHP:'{{#var:healAsPercentageOfMaxHP}}%'},
]
HeatedPiercingBreathTable =[
    {ragePoints:'{{#var:ragePoints}}'},
    {duration:'{{#var:duration}} sec'},
    {attackBonusPercentage:'{{#var:attackBonusPercentage}}%'},
    {solarEnergyBonusPerTower:'{{#var:solarEnergyBonusPerTower}}'},
]
ShortCircuitTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {duration:'{{#var:duration}} sec'},
]
AlterFateTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {duration:'{{#var:duration}} sec'},
    {cooldown:'{{#var:cooldown}} sec'},
    {chargeTime:'{{#var:chargeTime}} sec'},
    {empoweredDuration:'{{#var:empoweredDuration}} sec'},
    {shieldAsPercentageOfMaxHP:'{{#var:shieldAsPercentageOfMaxHP}}%'},
]
NovaTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {duration:'{{#var:duration}} sec'},
    {cooldown:'{{#var:cooldown}} sec'},
    {damageAsPercentageOfMaxHP:'{{#var:damageAsPercentageOfMaxHP}}%'},
    {healAsPercentageOfMaxHP:'{{#var:healAsPercentageOfMaxHP}}%'},
    {range:'{{#var:range}}'},
    {rageBonus:'{{#var:rageBonus}}'},
]
SeethingSparkTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {attackBonusPercentage:'{{#var:attackBonusPercentage}}%'},
    {damageAsPercentageOfMaxHP:'{{#var:damageAsPercentageOfMaxHP}}%'},
    {range:'{{#var:range}}'},
    {stunDuration:'{{#var:stunDuration}} sec'},
]
SeekerShotsTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {duration:'{{#var:duration}} sec'},
    {cooldown:'{{#var:cooldown}} sec'},
    {damageAsPercentageOfMaxHP:'{{#var:damageAsPercentageOfMaxHP}}%'},
    {numberOfProjectiles:'{{#var:numberOfProjectiles}}'},
    {maxTargets:'{{#var:maxTargets}}'},
]
MaleficBreathTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {duration:'{{#var:duration}} sec'},
    {cooldown:'{{#var:cooldown}} sec'},
    {attackBonusPercentage:'{{#var:attackBonusPercentage}}%'},
    {debuffType:'{{#var:debuffType}}'},
]
NocturnalFissureTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {duration:'{{#var:duration}} sec'},
    {cooldown:'{{#var:cooldown}} sec'},
    {damageScalingThreshold:'{{#var:damageScalingThreshold}}'},
    {healAsPercentageOfMaxHP:'{{#var:healAsPercentageOfMaxHP}}%'},
    {damageAsPercentageOfMaxHP:'{{#var:damageAsPercentageOfMaxHP}}%'},
    {explosionRadius:'{{#var:explosionRadius}}'},
]
UndyingWillTable = [
    {duration:'{{#var:duration}} sec'},
    {ammoRegenPercentage:'{{#var:ammoRegenPercentage}}%'},
    {attackBonusPercentage:'{{#var:attackBonusPercentage}}%'},
    {speedMultiplier:'{{#var:speedMultiplier}}%'},
]
BorrowTimeTable = [
    {durationPerShard:'{{#var:durationPerShard}} sec'},
    {temporalShards:'{{#var:temporalShards}}'},
    {ammoRegenPercentage:'{{#var:ammoRegenPercentage}}%'},
]
ConsumeTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {duration:'{{#var:duration}} sec'},
    {cooldown:'{{#var:cooldown}} sec'},
    {healAsPercentageOfMaxHP:'{{#var:healAsPercentageOfMaxHP}}%'},
    {ammoConvertToHPPercentage:'{{#var:ammoConvertToHPPercentage}}%'},
    {increasedAmmoRegenRateMultiplier:'{{#var:increasedAmmoRegenRateMultiplier}}x'},
    {consumedAmmoPercentage:'{{#var:consumedAmmoPercentage}}%'},
]
ChargedShieldTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {duration:'{{#var:duration}} sec'},
    {cooldown:'{{#var:cooldown}} sec'},
    {shieldAsPercentageOfMaxHP:'{{#var:shieldAsPercentageOfMaxHP}}%'},
    {damageAsPercentageOfMaxHP:'{{#var:damageAsPercentageOfMaxHP}}%'},
    {explosionRadius:'{{#var:explosionRadius}}'},
]
AdaptiveBreathTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {rageBonus:'{{#var:rageBonus}}'},
    {healthBonus:'{{#var:healthBonus}}'},
    {usableDelayForEachSpell:'{{#var:usableDelayForEachSpell}} sec'},
    {spellIdentifiers:'{{#var:spellIdentifiers}}'},
]
GalvanicOverloadTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {empoweredDamagePercentageApplied:'{{#var:empoweredDamagePercentageApplied}}%'},
    {empoweredRageBonus:'{{#var:empoweredRageBonus}}'},
    {empoweredDuration:'{{#var:empoweredDuration}} sec'},
    {damageAsPercentageOfMaxHP:'{{#expr:{{#var:damageAsPercentageOfMaxHP}}/100}}%'},
]
HeatBlastShieldTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {duration:'{{#var:duration}} sec'},
    {damageReductionPercentage:'{{#var:damageReductionPercentage}}%'},
    {healAsPercentageOfMaxHP:'{{#var:healAsPercentageOfMaxHP}}%'},
    {solarEnergyBonusPerShot:'{{#var:solarEnergyBonusPerShot}}'},
    {damageAsPercentageOfMaxHP:'{{#var:damageAsPercentageOfMaxHP}}%'},
    {explosionRadius:'{{#var:explosionRadius}}'},
]
BloodFuryTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {duration:'{{#var:duration}} sec'},
    {cooldown:'{{#var:cooldown}} sec'},
    {hpHealPercentage:'{{#var:hpHealPercentage}}%'},
    {rageRegenerationPercentage:'{{#var:rageRegenerationPercentage}}%'},
    {ragePointsBonus:'{{#var:ragePointsBonus}}'},
]
ShadowApophetTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {delayToActivateDragon:'{{#var:delayToActivateDragon}} sec'},
    {attackPowerAsPercentOfDragonHP:'{{#var:attackPowerAsPercentOfDragonHP}}%'},
    {hpAsPercentOfDragonHP:'{{#var:hpAsPercentOfDragonHP}}%'},
    {percentageOfDamageAbsorbed:'{{#var:percentageOfDamageAbsorbed}}%'},
    {ragePercentageIncrease:'{{#var:ragePercentageIncrease}}%'},
]
HealthRageDeathMarkTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {cooldown:'{{#var:cooldown}} sec'},
    {ragePointsRestored:'{{#var:ragePointsRestored}}'},
    {healAsPercentageOfMaxHP:'{{#var:healAsPercentageOfMaxHP}}%'},
]
FreezeAttackTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {frozenDuration:'{{#var:frozenDuration}} sec'},
    {cooldown:'{{#var:cooldown}} sec'},
    {splashRange:'{{#var:splashRange}}'},
    {damageAsPercentageOfMaxHP:'{{#var:damageAsPercentageOfMaxHP}}%'},
]
FrostbiteTable = [
    {damagePercentageIncreaseModifier:'{{#var:damagePercentageIncreaseModifier}}%'},
]
HealDragonTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {healTime:'{{#var:healTime}} sec'},
    {cooldown:'{{#var:cooldown}} sec'},
    {healAsPercentageOfMaxHP:'{{#var:healAsPercentageOfMaxHP}}%'},
]
MindControlTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {duration:'{{#var:duration}} sec'},
    {cooldown:'{{#var:cooldown}} sec'},
    {splashRange:'{{#var:splashRange}}'},
    {damageAsPercentageOfMaxHP:'{{#var:damageAsPercentageOfMaxHP}}%'},
]
TimeShiftTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {duration:'{{#var:duration}} sec'},
    {cooldown:'{{#var:cooldown}} sec'},
    {speedMultiplier:'{{#var:speedMultiplier}}%'},
]
FrozenTombTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {duration:'{{#var:duration}} sec'},
    {range:'{{#var:range}}'},
    {splashRange:'{{#var:splashRange}}'},
    {freezeDamagePercentOfMaxHP:'{{#var:freezeDamagePercentOfMaxHP}}%'},
    {shatterDamagePercentOfMaxHP:'{{#var:shatterDamagePercentOfMaxHP}}%'},
    {shieldAsPercentageOfMaxHP:'{{#expr:{{#var:shieldAsPercentageOfMaxHP}}*100}}%'},
]
InvincibleTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {duration:'{{#var:duration}} sec'},
    {cooldown:'{{#var:cooldown}} sec'},
]
GloomAndDoomTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {abilityRadius:'{{#var:abilityRadius}}'},
]
NorthernLightsTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {duration:'{{#var:duration}} sec'},
    {healAsPercentageOfMaxHP:'{{#var:healAsPercentageOfMaxHP}}%'},
    {energyRadius:'{{#var:energyRadius}}'},
    {ragePointsRestored:'{{#var:ragePointsRestored}}'},
]
InstantKillTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {cooldown:'{{#var:cooldown}} sec'},
    {immediateAttackMultiplier:'{{#var:immediateAttackMultiplier}}x'},
]
LockdownTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {duration:'{{#var:duration}} sec'},
    {splashRange:'{{#var:splashRange}}'},
    {allowDamageTime:'{{#var:allowDamageTime}}'},
]
FerociousBarrierTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {duration:'{{#var:duration}} sec'},
    {cooldown:'{{#var:cooldown}} sec'},
    {empoweredDuration:'{{#var:empoweredDuration}} sec'},
    {damageAbsorbedPercentage:'{{#var:damageAbsorbedPercentage}}%'},
    {attackBonusPercentage:'{{#var:attackBonusPercentage}}%'},
    {attackBonusCapPercentage:'{{#var:attackBonusCapPercentage}}%'},
]
CloakTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {duration:'{{#var:duration}} sec'},
    {cooldown:'{{#var:cooldown}} sec'},
    {speedMultiplier:'{{#var:speedMultiplier}}%'},
    {attackBonusPercentage:'{{#var:attackBonusPercentage}}%'},
    {ragePercentageIncrease:'{{#var:ragePercentageIncrease}}%'},
    {ammoRechargePercentage:'{{#var:ammoRechargePercentage}}%'},
    {canUseSpells:'{{#var:canUseSpells}}'},
    {canAttack:'{{#var:canAttack}}'},
    {alwaysHasCooldown:'{{#var:alwaysHasCooldown}}'},
]
ExplosiveAegisTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {duration:'{{#var:duration}} sec'},
    {cooldown:'{{#var:cooldown}} sec'},
    {damageReductionPercentage:'{{#var:damageReductionPercentage}}%'},
    {attackBonusPercentage:'{{#var:attackBonusPercentage}}%'},
    {shieldAsPercentageOfMaxHP:'{{#var:shieldAsPercentageOfMaxHP}}%'},
    {damageAsPercentageOfMaxHP:'{{#expr:{{#var:damageAsPercentageOfMaxHP}}/100}}%'},
    {explosionRadius:'{{#var:explosionRadius}}'},
]
DreadfulRoarTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {radius:'{{#var:radius}}'},
    {debuffType:'{{#var:debuffType}}'},
    {percentageIncreasedDamage:'{{#var:percentageIncreasedDamage}}%'},
    {damageAsPercentageOfMaxHP:'{{#var:damageAsPercentageOfMaxHP}}%'},
]
CurePoisonTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {duration:'{{#var:duration}} sec'},
    {healAsPercentageOfMaxHP:'{{#var:healAsPercentageOfMaxHP}}%'},
]
SacrificeTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {duration:'{{#var:duration}} sec'},
    {rageBonus:'{{#var:rageBonus}}'},
    {damagePercentageApplied:'{{#var:damagePercentageApplied}}%'},
]
SouthernCrossTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {cooldown:'{{#var:cooldown}} sec'},
    {range:'{{#var:range}}'},
    {splashRange:'{{#var:splashRange}}'},
    {damageAsPercentageOfMaxHP:'{{#var:damageAsPercentageOfMaxHP}}%'},
    {healAsPercentageOfMaxHP:'{{#var:healAsPercentageOfMaxHP}}%'},
    {energyRadius:'{{#var:energyRadius}}'},
    {ragePointsRestored:'{{#var:ragePointsRestored}}'},
]
DissipateTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {duration:'{{#var:duration}} sec'},
    {cooldown:'{{#var:cooldown}} sec'},
    {speedMultiplier:'{{#var:speedMultiplier}}%'},
    {explosionRadius:'{{#var:explosionRadius}}'},
    {damageAsPercentageOfMaxHP:'{{#var:damageAsPercentageOfMaxHP}}%'},
    {ammoRechargePercentage:'{{#var:ammoRechargePercentage}}%'},
    {attackBonusPercentage:'{{#var:attackBonusPercentage}}%'},
    {empoweredDuration:'{{#var:empoweredDuration}} sec'},
    {shouldNormalDamageHitDisabledTowers:'{{#var:shouldNormalDamageHitDisabledTowers}}'},
]
CelestialDanceTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {cooldown:'{{#var:cooldown}} sec'},
]
DevourHopeTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {cooldown:'{{#var:cooldown}} sec'},
    {healAsPercentageOfMaxHP:'{{#var:healAsPercentageOfMaxHP}}%'},
    {abilityRadius:'{{#var:abilityRadius}}'},
]
DesiccatingSandTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {damageAsPercentageOfMaxHP:'{{#var:damageAsPercentageOfMaxHP}}%'},
    {splashRange:'{{#var:splashRange}}'},
]
StoneskinTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {duration:'{{#var:duration}} sec'},
    {damageReductionPercentage:'{{#var:damageReductionPercentage}}%'},
]
KamikazeTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {duration:'{{#var:duration}} sec'},
    {cooldown:'{{#var:cooldown}} sec'},
    {range:'{{#var:range}}'},
    {splashRange:'{{#var:splashRange}}'},
    {damageAsPercentageOfMaxHP:'{{#var:damageAsPercentageOfMaxHP}}%'},
]
AoeTable = [
    {ragePoints:'{{#var:ragePoints}}'},
    {range:'{{#var:range}}'},
    {splashRange:'{{#var:splashRange}}'},
    {damageAsPercentageOfMaxHP:'{{#var:damageAsPercentageOfMaxHP}}%'},
]



table_format = [
    {'AbsorbMagicSpell':AbsorbMagicTable},
    {'IntimidatingRoarSpell':IntimidatingRoarTable},
    {'AdaptiveResistSpell':AdaptiveResistTable},
    {'EnergySyphonSpell':EnergySyphonTable},
    {'FrenzySpell':FrenzyTable},
    {'StarburnSpell':StarburnTable},
    {'ShieldAssaultSpell':ShieldAssaultTable},
    {'LightSpeedSpell':LightSpeedTable},
    {'ElementalBarrierSpell':ElementalBarrierTable},
    {'IncreaseRageGenerationSpell':IncreaseRageGenerationTable},
    {'FuryOfTheWastesSpell':FuryOfTheWastesTable},
    {'IsolationSpell':IsolationTable},
    {'StealEssenceSpell':StealEssenceTable},
    {'CrumbleToDustSpell':CrumbleToDustTable},
    {'BattlecrySpell':BattlecryTable},
    {'InvertSpell':InvertTable},
    {'HurricaneSpell':HurricaneTable},
    {'FluxSpell':FluxTable},
    {'CrystallineShieldSpell':CrystallineShieldTable},
    {'DeflectingGaleSpell':DeflectingGaleTable},
    #
    {'SummonAIBattleDragonSpell':SummonAIBattleDragonTable},
    {'RadianceSpell':RadianceTable},
    {'ThunderstormSpell':ThunderstormTable},
    {'ChainLightningSpell':ChainLightningTable},
    {'ShattershardSpell':ShattershardTable},
    {'BerserkSpell':BerserkTable},
    {'UmbralSpikeSpell':UmbralSpikeTable},
    {'NightfallSpell':NightfallTable},
    {'DaybreakSpell':DaybreakTable},
    {'RisingPhoenixSpell':RisingPhoenixTable},
    {'CosmicEnergySpell':CosmicEnergyTable},
    {'DodgeSpell':DodgeTable},
    {'HealingMarkSpell':HealingMarkTable},
    {'HeatedPiercingBreathSpell':HeatedPiercingBreathTable},
    {'ShortCircuitSpell':ShortCircuitTable},
    {'AlterFateSpell':AlterFateTable},
    {'NovaSpell':NovaTable},
    {'SeethingSparkSpell':SeethingSparkTable},
    {'SeekerShotsSpell':SeekerShotsTable},
    {'MaleficBreathSpell':MaleficBreathTable},
    #
    {'NocturnalFissureSpell':NocturnalFissureTable},
    {'UndyingWillSpell':UndyingWillTable},
    {'BorrowTimeSpell':BorrowTimeTable},
    {'ConsumeSpell':ConsumeTable},
    {'ChargedShieldSpell':ChargedShieldTable},
    {'AdaptiveBreathSpell':AdaptiveBreathTable},
    {'GalvanicOverloadSpell':GalvanicOverloadTable},
    {'HeatBlastShieldSpell':HeatBlastShieldTable},
    {'BloodFurySpell':BloodFuryTable},
    {'ShadowApophetSpell':ShadowApophetTable},
    {'HealthRageDeathMarkSpell':HealthRageDeathMarkTable},
    {'FreezeAttackSpell':FreezeAttackTable},
    {'FrostbiteSpell':FrostbiteTable},
    {'HealDragonSpell':HealDragonTable},
    {'MindControlSpell':MindControlTable},
    {'TimeShiftSpell':TimeShiftTable},
    {'FrozenTombSpell':FrozenTombTable},
    {'InvincibleSpell':InvincibleTable},
    {'GloomAndDoomSpell':GloomAndDoomTable},
    {'NorthernLightsSpell':NorthernLightsTable},
    #
    {'InstantKillSpell':InstantKillTable},
    {'LockdownSpell':LockdownTable},
    {'FerociousBarrierSpell':FerociousBarrierTable},
    {'CloakSpell':CloakTable},
    {'ExplosiveAegisSpell':ExplosiveAegisTable},
    {'DreadfulRoarSpell':DreadfulRoarTable},
    {'CurePoisonSpell':CurePoisonTable},
    {'SacrificeSpell':SacrificeTable},
    {'SouthernCrossSpell':SouthernCrossTable},
    {'DissipateSpell':DissipateTable},
    {'CelestialDanceSpell':CelestialDanceTable},
    {'DevourHopeSpell':DevourHopeTable},
    {'DesiccatingSandSpell':DesiccatingSandTable},
    {'StoneskinSpell':StoneskinTable},
    {'KamikazeSpell':KamikazeTable},
    {'AoeSpell':AoeTable},
]

spell_filename = []
for file in glob.glob('wd/assets/*Spell.csv'):
    spell_filename.append(file.split('/')[-1])

for filename in spell_filename:
    if filename in file_skip_list:
        continue
    spell_name = filename[:-4]
    #print spell_name
    spell_data = spelldata.getSpellData(spell_name)
    meta = createAbilityMeta()
    f = open('output/TEMPLATE_'+spell_name+'.txt', 'w+')
    f.write(meta)
    table = createTable(spell_name)
    f.write(table)
    family = createFamily()
    f.write(family)
    f.close()

    upload = 1
    title = 'Template:'+spell_name
    text = meta + table + family

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

