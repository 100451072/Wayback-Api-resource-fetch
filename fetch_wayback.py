#!/bin/env python3

import requests
import os
import sys
import re

access_key = ""
secret_key = ""

def req_url(req_url:str) -> int:
    """ Request req_url to wayback machine""" 
    api_url = f"https://web.archive.org/__wb/calendarcaptures?url={req_url}&matchType=prefix&collapse=urlkey&output=json&access_key={access_key}&secret_key={secret_key}"

    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            # Get the name of the file
            filename = os.path.basename(req_url)
            with open(filename, "wb") as f:
                # Write the content of the file
                f.write(response.content)
                # Output for possible pipe chaining
                print(filename)
            return 0
        else:
            # Write to the stderr so it can be removed with &>/dev/null output
            print(f"Not written {req_url}", file=sys.stderr)
            return 1
    # In case of error in the requests
    except requests.exceptions.RequestException as e:
        error_message = f"An error occurred: {str(e)}"
        print(error_message, file=sys.stderr)

def list_url_req(input_filename:str, output_filename:str, req_filter:str=None):
    """ Open a file with url and request them, add the obtained to index"""
    with open(output_filename, "w") as index:
        with open(input_filename, "r") as f:
            url = f.readline()
            while url:
                # Aply filter
                if filter_url(url, req_filter) == 0:
                    # Req one url
                    if req_url(url) == 0:
                        # Write it to index.txt
                        index.write(os.path.basename(url))
                else: 
                    print(f"Debuggin --> {url}")

def filter_url(url:str, filter_url:str) -> int:
    """ Funcion in charge of filtering url using regex"""
    # Filter used
    if filter_url != None:
         # Escape special characters in the user input
        filter_pattern = re.escape(filter_url)

        # Construct the regex pattern
        pattern = fr"\b{filter_pattern}\b"  # Adding word boundary anchors

        # Search for the pattern in the text
        matches = re.findall(pattern, url.strip('\'"'))
        if matches:
            # Match
            return 0
        else:
            # No match
            return 1

    # No filter
    else:
        return 0
    
def handle_args():
    """ Handle arguments"""
    if (len(sys.argv) != 5 and len(sys.argv) != 7)or sys.argv[1] != "-i" or sys.argv[3] != "-o":
        print("Script to fetch resources from wayback machine\nUsage: \n    -i <url_list> -o <ouptut_index_file>\n    -i <url_list> -o <output_index_file> -f <regex_filter>")
        exit(1)
    
    if (not os.path.exists(sys.argv[2]) or os.path.exists(sys.argv[4])):
        print("ERROR: input file does not exist, or output file already exists")
        exit(2)

    # check input with Filter
    if (len(sys.argv) == 7) and (not sys.argv[5] == "-f"):
        print("ERROR: invalid argument ", sys.argv[5])
        exit(3)


if __name__ == "__main__":
    handle_args()
    # With filter
    if (len(sys.argv) == 7):
        list_url_req(sys.argv[2], sys.argv[4], sys.argv[6])
    # Without filter
    else:
        list_url_req(sys.argv[2], sys.argv[4])
    exit(0)

