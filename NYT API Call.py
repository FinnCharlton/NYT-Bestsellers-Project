#Import required packages
import requests as rq
import pandas as pd
import json
import time

#Set API key
APIKey = "kHz67Lh50kdWNCEotfani0UsrAi931jQ"

#Function to get list names from NYT Bestsellers API
def getListNames():
    response = rq.get(f"https://api.nytimes.com/svc/books/v3/lists/names.json?api-key={APIKey}")
    return response

# #Create string of all list names in API call
lists = {}
for list in getListNames().json()["results"]:
    lists[list["list_name"]] = list["list_name_encoded"]



#Function to call API for specified list, and parse into Dataframe
def getFullList(listName,listNameEncoded):
    response = rq.get(f"https://api.nytimes.com/svc/books/v3/lists/current/{listNameEncoded}.json?api-key={APIKey}")
    if response.status_code != 200:
        print(f"{listName} Error {response.status_code}")
        return pd.DataFrame()
    responseString = json.dumps(response.json()["results"]["books"],sort_keys=False,indent=4)
    dfBestsellers = pd.read_json(responseString)
    dfBestsellers["List Name"] = listName
    return dfBestsellers

fullBestsellerList = pd.DataFrame()
for key,value in lists.items():
    df = getFullList(key, value)
    fullBestsellerList = pd.concat([fullBestsellerList,df])
    time.sleep(12)

fullBestsellerList.to_csv("Full Bestseller.csv")

#Parse Response into JSON
# responseString = json.dumps(getFullList("hardcover-fiction").json()["results"]["books"],sort_keys=False,indent=4)

# #Write to Local File for Dev
# file = open("Example JSON.txt","w")
# file.write(responseString)