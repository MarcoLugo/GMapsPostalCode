#########################################################################################
# Title: GMapsPostalCode
# Author: Marco Lugo
# Description: uses the Google Maps API to extract the postal code of a given Canadian
#              address.
#
#              Example:
#              python getPostalCode.py schwartz+montreal
#              output --> H2W 1X9
#
#              To get your own API key go to:
#              https://developers.google.com/places/web-service/get-api-key
#########################################################################################

import sys
import urllib.request
import json

API_KEY = ''

def getGoogleMapsAddress(address, api_key):
    URL = 'https://maps.googleapis.com/maps/api/geocode/json?address=+'+address+'&key='+api_key
    try:
        request = urllib.request.urlopen(URL)
    except:
        return(-1)
    googleResponse = request.read().decode('utf8')
    result = json.loads(googleResponse)
    return(result)


def getGoogleMapsPostalCode(address, api_key):
    results = getGoogleMapsAddress(address, api_key)

    if(results['status'] != 'OK'):
        return(-2) #Error detected with the HTTP request or the Google API

    postal_code = -1 #default value

    for result in results['results'][0]['address_components']:
        if result['types'][0] == 'postal_code':
            postal_code = result['long_name']
            
    return(postal_code)


def showHelp():
    print('Example usage: python ' + sys.argv[0] + ' address')
    print(' - Addresses cannot have spaces')
    print(' - The program will return -1 if no result was found with the given address and -2 if the address triggered an error in the request.')
    print('')
    print(' Example: python ' + sys.argv[0] + ' schwartz+montreal\n')



if __name__ == "__main__":
    if(len(sys.argv) != 2):
        print('ERROR: please review arguments\n')
        showHelp()
        exit()

    s = getGoogleMapsPostalCode(sys.argv[1], API_KEY)
    print(s)
