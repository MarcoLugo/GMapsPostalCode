#!/usr/bin/python3
#########################################################################################
# Title: GMapsPostalCodes
# Author: Marco Lugo
# Description: uses the Google Maps API to extract the postal codes for Canadian Addresses
#              given as input via a text file.
#
#              Example:
#              python getPostalCode.py address_list.txt address_list_output.txt
#
#              To get your own API key go to:
#              https://developers.google.com/places/web-service/get-api-key
#########################################################################################

import sys
import urllib.request
import json
import re
import os.path


API_KEY = '' # DON'T FORGET TO ADD YOUR API KEY

# prepare and compile regex pattern to remove accents
accent_replacements = {
    'à':'a', 'â':'a', 'ä':'a',
    'é': 'e', 'è':'e', 'ê':'e', 'ë':'e',
    'î':'i', 'ï':'i',
    'ô':'o', 'ö':'o',
    'û':'u', 'ü':'u',
    'ç':'c'
    }
accent_replacements = dict((re.escape(k), v) for k, v in accent_replacements.items())
pattern = re.compile("|".join(accent_replacements.keys()))


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

    if isinstance(results, int):
        if results == -1:
            return(-2) #Error detected with the HTTP request or the Google API
    else:
        if results['status'] != 'OK':
            return(-2) #Error detected with the HTTP request or the Google API

    postal_code = -1 #default value

    for result in results['results'][0]['address_components']:
        if result['types'][0] == 'postal_code':
            postal_code = result['long_name']

    return(postal_code)


def showHelp():
    print('Example usage: python ' + sys.argv[0] + ' input_file output_file')
    print('')
    print(' Example: python ' + sys.argv[0] + ' address_list.txt address_list_output.txt\n')




if __name__ == "__main__":
    if(len(sys.argv) != 3):
        print('ERROR: please review arguments\n')
        showHelp()
        exit()


    fname_in = sys.argv[1]
    fname_out = sys.argv[2]

    if not os.path.isfile(fname_in):
        print('Error: input file does not exist.')
        exit()

    if os.path.isfile(fname_out):
        print('Error: output file already exists.')
        exit()

    # read input file
    with open(fname_in, encoding='utf-8') as f:
        content = f.read().splitlines()

    # process input file, line by line
    n_lines = len(content) - 1
    for i, line in enumerate(content):
        print(i, '/', n_lines, ': ', line)
        unaccented_line = text = pattern.sub(lambda m: accent_replacements[re.escape(m.group(0))], line.lower())
        line_nospace = unaccented_line.replace(' ', '+') # we cannot have whitespace in the url request
        result = getGoogleMapsPostalCode(line_nospace, API_KEY)
        print(' ---> ', result)

        with open(fname_out, 'a') as f:
            out_string = line + ';' + str(result) + '\n'
            f.write(out_string)
