import requests
import pandas as pd


# NOTES = 'r' by common convention is 'response'

# get response from a url
def getResponse(url):
    r = requests.get(url)

    # 200 is StatusOK, ie the request has worked, see: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
    if r.status_code != 200:
        raise ValueError("Request failed on {u}. With error code {r}.".format(u=url, s=r.status_code))

    return r


# unpack a json response to a dictionary
def unpackJson(r):
    try:
        return r.json()
    except:
        raise ValueError("Cannot unpack json into a dict...is your source url json?")


# get and then unpack json from a url
def getDataFromSource(url):
    r = getResponse(url)
    return unpackJson(r)


# verify that the request is for the expected endpoints
def verifyCorrectEndpoint(url):
    if "api.beta.ons.gov.uk/" not in url and "api.ons.gov.uk" not in url and "api.dev.cmd." not in url:
        raise ValueError(
            "Aborting. This function is intended for use with the dp-codelist-api. Urls should end with /codes.")


# get all codes for a given codelist
def getAllCodes(url):
    verifyCorrectEndpoint(url)
    data = getDataFromSource(url)

    return [x["id"] for x in data["items"]]


# get all codes for a given codelist
def getAllLabels(url):
    verifyCorrectEndpoint(url)
    data = getDataFromSource(url)

    return [x["label"] for x in data["items"]]


# returns a lookup dictionary of {code:label}
def getCodeLookup(url):
    verifyCorrectEndpoint(url)
    data = getDataFromSource(url)

    return [{x["id"], x["label"]} for x in data["items"]]


# return a lookup dictionary of {label:code}
def getLabelLookup(url):
    verifyCorrectEndpoint(url)
    data = getDataFromSource(url)

    return [{x["label"], x["id"]} for x in data["items"]]


# returns a dictionary of {url:id} for all codelists on the code list API
# we're using the url for key as codelist are versioned but their names are not
def getCodeListDict():

    try:
        # always use cmd-dev by preference
        r = getResponse("https://api.dev.cmd.onsdigital.co.uk/v1/code-lists")
    except:
        print("WARNING - cannot access cmd-dev. Using Public Apis.")
        r = getResponse("https://api.beta.ons.gov.uk/v1/code-lists")


    data = unpackJson(r)

    urlDict = [x["links"]["self"]["href"] for x in data["items"]]

    return urlDict


# getEditionSpecificCodelists takes a simple codelist url and gets to the specific codes via edition
# this    >> https://api.beta.ons.gov.uk/v1/code-lists/cpi1dim1aggid
# to this >> https://api.beta.ons.gov.uk/v1/code-lists/cpi1dim1aggid/editions/one-off/codes
def getEditionSpecificCodelists(allCl):
    allClDictList = []
    for cl in allCl:

        r = getResponse(cl + "/editions")
        data = unpackJson(r)

        # we need to create a lookup for each edition specific codelist
        for item in data["items"]:
            itemDict = {
                "url": item["links"]["codes"]["href"],
                "edition": item["links"]["self"]["id"],
                "label": item["label"]
            }

            allClDictList.append(itemDict)

    return allClDictList


#
def findCodelists(dictOfItemLists, removeZeroMatches=True):
    # police input
    if type(dictOfItemLists) != dict:
        raise ValueError("Aborting. The findCodelists function requires a dictionary.")

    for key in dictOfItemLists.keys():

        if type(dictOfItemLists[key]) != list:
            raise ValueError(
                "Aborting. The findCodelists fuction required a dictionary of {key:[]}, you did not provide a list.")

    # codelists from the cmd-api
    allCl = getCodeListDict()
    allClDict = getEditionSpecificCodelists(allCl)

    allResults = []
    for key in dictOfItemLists.keys():
        allResults.append(findCodelist(key, dictOfItemLists[key], allClDict))

    return allResults


#
def findCodelist(listName, itemList, allCLDict):
    result = {
        "bestMatchPerc": 0,
        "bestMatchUrl": None,
        "name":listName,
    }

    for cl in allCLDict:

        codesFromApi = getAllCodes(cl["url"])
        matches = len([x for x in itemList if x in codesFromApi])

        percMatch = (100 / len(itemList)) * matches

        if percMatch > result["bestMatchPerc"]:
            result["bestMatchPerc"] = percMatch
            result["bestMatchUrl"] = cl["url"]
            result["name"] = listName

    return result

