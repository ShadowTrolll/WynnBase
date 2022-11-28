import requests
import json
import os

mDEBUG = True

scriptPath = os.getcwd()
resPath = scriptPath + "/Resources/"
baseUrl = r"https://api.wynncraft.com/v2/"
respCodeDict = {200: "Success", 400: "Bad Request", 404: "Not Found",
                429: "Too Many Requests", 500: "Internal Server Error",
                502: "Bad Gateway", 503: "Service Unavailable"}

def DEBUG(txt):
    if mDEBUG: print("DEBUG: " + txt)

def DEBUG_RESP(code):
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

