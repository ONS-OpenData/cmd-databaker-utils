
import requests


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

    if "/codes" not in url:
        raise ValueError("Aborting. This function is intended for use with the dp-codelist-api. Urls should end with /codes.")


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

    return [{x["id"] ,x["label"]} for x in data["items"]]


# return a lookup dictionary of {label:code}
def getLabelLookup(url):

    verifyCorrectEndpoint(url)
    data = getDataFromSource(url)

    return [{x["label"] ,x["id"]} for x in data["items"]]


