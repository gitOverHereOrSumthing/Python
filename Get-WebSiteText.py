# Description: 
# Version: 1.0.0
# Date Created:  10/02/2020
# Author: Simon Goodson
# Notes: DO NOT RUN IF YOU DONT UNDERSTAND WHAT THIS SCRIPT WILL DO!
# Please add any changes or updates under this line and update the version.

from fake_useragent import UserAgent
import requests
import sys
import argparse

def writeFile(fileName, inputText):
    targetFile = open(fileName, 'w')
    targetFile.write(inputText)
    targetFile.close()

def main():
    print("Checking website...")
    
    try:
        # Getting command line arguments from the script
        parser = argparse.ArgumentParser(description='Website Test Retreival')
        parser.add_argument('--URL', type=str, default="", help='URL to check')
        parser.add_argument('--o', type=str, default="", help='Output file')
        args = parser.parse_args()
        
        URL = args.URL
        if len(URL) == 0:
            print("URL required")
            sys.exit()
            
        OutputFile = args.o
        if len(OutputFile) == 0:
            print("Output File required")
            sys.exit()
        
        
        
        # Creating session
        session_requests = requests.session()

        # Changing the user-agent sent to webpage
        ua = UserAgent()
        header = {'User-Agent':str(ua.random),'referer':str(URL)}

        result = session_requests.get(URL, headers = header)
        
        print(result)
        writeFile(OutputFile, result.text)
    except Exception as err:
        # Code to exit script
        print("Error raised. Error reads: " + str(err))
        sys.exit()

if __name__ == '__main__':
    main()