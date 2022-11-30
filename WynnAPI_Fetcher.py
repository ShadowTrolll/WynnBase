import requests
import json
import os
import re

mDEBUG = True

scriptPath = os.getcwd()
resPath = scriptPath + "/Resources/"
baseUrl = r"https://api.wynncraft.com/v2/"
respCodeDict = {
    200: "Success", 400: "Bad Request", 404: "Not Found",
    429: "Too Many Requests", 500: "Internal Server Error",
    502: "Bad Gateway", 503: "Service Unavailable"
    }
attrDict = {
    "\"left\"": "\"Effectiveness (Left of This) [%]\"",
    "\"right\"": "\"Effectiveness (Right of This) [%]\"",
    "\"above\"": "\"Effectiveness (Above This) [%]\"",
    "\"under\"": "\"Effectiveness (Under This) [%]\"",
    "\"touching\"": "\"Effectiveness (Touching This) [%]\"",
    "\"notTouching\"": "\"Effectiveness (Not Touching This) [%]\"",
    "\"duration\"": "\"Effect Duration [s]\"",
    "\"durabilityModifier\"": "\"Durability\"",
    "\"strengthRequirement\"": "\"Requires Strength\"",
    "\"dexterityRequirement\"": "\"Requires Dexterity\"",
    "\"intelligenceRequirement\"": "\"Requires Intelligence\"",
    "\"defenceRequirement\"": "\"Requires Defence\"",
    "\"agilityRequirement\"": "\"Requires Agility\"",
    "\"charges\"": "\"Charge Count\"",
    "\"INTELLIGENCEPOINTS\"": "\"Intelligence\"",
    "\"STRENGTHPOINTS\"": "\"Strength\"",
    "\"DEXTERITYPOINTS\"": "\"Dexterity\"",
    "\"DEFENSEPOINTS\"": "\"Defence\"",
    "\"AGILITYPOINTS\"": "\"Agility\"",
    "\"DAMAGEBONUS\"": "\"Main Attack Damage [%]\"",
    "\"EARTHDAMAGEBONUS\"": "\"Earth Damage [%]\"",
    "\"THUNDERDAMAGEBONUS\"": "\"Thunder Damage [%]\"",
    "\"WATERDAMAGEBONUS\"": "\"Water Damage [%]\"",
    "\"FIREDAMAGEBONUS\"": "\"Fire Damage [%]\"",
    "\"AIRDAMAGEBONUS\"": "\"Air Damage [%]\"",
    "\"SPELLDAMAGE\"": "\"Spell Damage [%]\"",
    "\"DAMAGEBONUSRAW\"": "\"Main Attack Damage [RAW]\"",
    "\"EARTHDAMAGEBONUSRAW\"": "\"Earth Damage [RAW]\"",
    "\"THUNDERDAMAGEBONUSRAW\"": "\"Thunder Damage [RAW]\"",
    "\"WATERDAMAGEBONUSRAW\"": "\"Water Damage [RAW]\"",
    "\"FIREDAMAGEBONUSRAW\"": "\"Fire Damage [RAW]\"",
    "\"AIRDAMAGEBONUSRAW\"": "\"Air Damage [RAW]\"",
    "\"SPELLDAMAGERAW\"": "\"Spell Damage [RAW]\"",
    "\"GATHER_SPEED\"": "\"Gathering Speed [%]\"",
    "\"GATHER_XP_BONUS\"": "\"Gathering XP Bonus [%]\"",
    "\"HEALTHBONUS\"": "\"Health\"",
    "\"HEALTHREGENRAW\"": "\"Health Regen [RAW]\"",
    "\"HEALTHREGEN\"": "\"Health Regen [%]\"",
    "\"LIFESTEAL\"": "\"Life Steal [Per 4s]\"",
    "\"MANASTEAL\"": "\"Mana Steal [Per 3s]\"",
    "\"EARTHDEFENSE\"": "\"Earth Defense [%]\"",
    "\"THUNDERDEFENSE\"": "\"Thunder Defense [%]\"",
    "\"WATERDEFENSE\"": "\"Water Defense [%]\"",
    "\"FIREDEFENSE\"": "\"Fire Defense [%]\"",
    "\"AIRDEFENSE\"": "\"Air Defense [%]\"",
    "\"WEAPONSMITHING\"": "\"Weaponsmithing\"",
    "\"WOODWORKING\"": "\"Woodworking\"",
    "\"ARMOURING\"": "\"Armouring\"",
    "\"TAILORING\"": "\"Tailoring\"",
    "\"JEWELING\"": "\"Jeweling\"",
    "\"COOKING\"": "\"Cooking\"",
    "\"ALCHEMISM\"": "\"Alchemism\"",
    "\"SCRIBING\"": "\"Scribing\"",
    "\"STAMINA_REGEN\"": "\"Sprint Regen [%]\"",
    "\"ATTACKSPEED\"": "\"Attack Speed Tier\"",
    "\"SPEED\"": "\"Walk Speed [%]\"",
    "\"THORNS\"": "\"Thorns [%]\"",
    "\"EXPLODING\"": "\"Exploding [%]\"",
    "\"POISON\"": "\"Poison [Per 3s]\"",
    "\"LOOT_QUALITY\"": "\"Loot Quality [%]\"",
    "\"LOOTBONUS\"": "\"Loot Bonus [%]\"",
    "\"REFLECTION\"": "\"Reflection [%]\"",
    "\"SOULPOINTS\"": "\"Soul Point Regen [%]\"",
    "\"MANAREGEN\"": "\"Mana Regen [Per 5s]\"",
    "\"EMERALDSTEALING\"": "\"Stealing [%]\""
    }
#"\"\"": "\"\"",

def DEBUG(txt):
    if mDEBUG: print("DEBUG: " + txt)

def DEBUG_RESP(code):
    if not mDEBUG: return
    DEBUG("Fetching finished with response code " + str(code) + ": " + respCodeDict[code])



DEBUG("Starting the script")

if not os.path.exists(resPath + "ingredient_list.json"):
    os.makedirs(resPath, exist_ok=True)
    DEBUG("Ingredient list missing, fetching")
    response = requests.get(baseUrl + r"ingredient/list")
    if response.status_code == 200:
        with open(resPath + "ingredient_list.json", 'w') as f:
            f.write(json.dumps(response.json()))
    DEBUG_RESP(response.status_code)

if not os.path.exists(resPath + "ingredient_list.json"):
    DEBUG("Could not obtain ingredient list, quitting")
    exit()

DEBUG("Loading ingredient list")
f = open(resPath + "ingredient_list.json")
ingList = json.loads(f.read())["data"]
f.close()

ingFailed = {}
DEBUG("Fetching missing ingredients")
for ingName in ingList:
    if not os.path.exists(resPath + "ing_" + ingName + ".json"):
        DEBUG("Fetching ingredient: " + ingName)
        response = requests.get(baseUrl + r"ingredient/get/" + ingName.replace(" ","_"))
        DEBUG_RESP(response.status_code)
        if response.status_code == 400:
            DEBUG("Attempting name search")
            response = requests.get(baseUrl + r"ingredient/search/name/" + ingName)
            DEBUG_RESP(response.status_code)
            
        if response.status_code == 200:
            if len(response.json()["data"]) > 0:
                with open(resPath + "ing_" + ingName + ".json", 'w') as f:
                    f.write(json.dumps(response.json()))
                next
        
        ingFailed[ingName] = response.status_code
        if not (response.status_code == 404 or response.status_code == 400): break
DEBUG("Done")
if len(ingFailed) > 0:
    DEBUG("Could not obtain ingredients: " + json.dumps(ingFailed))

DEBUG("Building output JSON")
jsonStr = "{\"LIST\":"
jsonStr += json.dumps(ingList)

DEBUG("Processing ingredient data")
regex = re.compile("(%s)" % "|".join(map(re.escape, attrDict.keys())))
jsonStr += ",\"DATA\":{"
for ingName in ingList:
    if not os.path.exists(resPath + "ing_" + ingName + ".json"): continue
    with open(resPath + "ing_" + ingName + ".json") as f:
        itemStr = json.dumps(json.loads(f.read())["data"][0])
        itemStr = regex.sub(lambda mo: attrDict[mo.string[mo.start():mo.end()]], itemStr) 
        jsonStr += "\"" + ingName + "\":" + itemStr + ","
jsonStr = jsonStr[:-1] + "}"


DEBUG("Writing processed data to output")
jsonStr += "}"
with open(scriptPath + "/IngData.json", 'w') as f:
    f.write(jsonStr)

print("Done")
input("Press enter to exit...")
