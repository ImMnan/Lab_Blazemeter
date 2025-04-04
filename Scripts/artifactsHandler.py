# This script checks all the sessions to determine if there are any missing artifacts.zip files based on a given master ID
# You will need an api-key.json file that contains a BZM admin key to use this script
# Script is V1, I plan to improve it once I get feedback

import json
import logging
import time
import os
import requests
from requests.auth import HTTPBasicAuth

# Gets the current time and builds the log file using the time as part of the filename
now = time.time()
logging.basicConfig(filename='./checkForArtifacts_%s.log' % now,
                    format='%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s', level=logging.DEBUG)

# Base url for all the API calls
base_url = 'https://a.blazemeter.com/api/v4/'

# Grabs the API key from the api-key.json file and uses that for API authentications
def get_api_key():
    if os.path.isfile(os.getcwd() + '/api-key.json'):
        logging.info("Loading api key from file.")
        my_file = open(os.getcwd() + '/api-key.json', 'r')
        contents = my_file.read()
        key = json.loads(contents)
        key_id = key['id']
        secret = key['secret']
        auth = HTTPBasicAuth(key_id, secret)
        check = check_api_key(auth)
        if check:
            return auth
        else:
            logging.error('API Key in api-key.json is not valid. Notifying monitoring channel and exiting...')
            # Exit code 4 means api key file contains a non-admin API key
            exit(4)
    else:
        logging.error("Failed to find API key file.")
        logging.error('api-key.json file failed to load. Notifying monitoring channel and exiting...')
        # Exit code 3 means api key file is missing
        exit(3)

# Verifies the API key being used is a BZM admin key
def check_api_key(auth):
    check = True
    logging.info('GET ' + base_url + 'user')
    r = requests.get(base_url + 'user', auth=auth)
    response = r.json()
    logging.info(response)
    if r.status_code == 200:
        logging.info('API Key is valid.')
        logging.info('Checking for admin access')
        if response['result']['features']['admin']:
            logging.info('API Key has admin access.')
            directUser(auth)
            return check
        else:
            logging.error('API Key does not have admin access.')
            check = False
            return check
    else:
        logging.error('API Key is not valid.')
        print('Your API Key is not valid. Please check the api-key.json file.')
        check = False
        return check

# Directory Function to determine user's purpose
def directUser(auth):
    # while loop to prevent script from ending on invalid input
    while True:
        print("Please select the task you want to script to perform from below choices (Just type the number and press Enter)")
        userChoice = input("[1] - Find Failed Sessions" + "\n" + "[2] - Download Artifacts and/or Admin-Artifacts" + "\n" + "[3] - Download specific files by filename (coming soon)" + "\n" + "[4] - Download Specific files by file type (coming soon)" + "\n")
        userChoice = userChoice.replace(" ", '')

        # Directory itself. Logs choice, directs to next function for chosen application flow
        if userChoice == "1":
            logging.info("User chose to find failed sessions")
            getSessions(auth)
            break
        if userChoice == "2":
            logging.info("User chose to download artifacts")
            downloadArtifacts(auth)
            break
        if userChoice == "3":
            logging.info("User chose to download files by name")
            downloadFilesByName(auth)
            break
        if userChoice == "4":
            logging.info("user chose to download files by type")
            downloadFilesByType(auth)
            break
        else:
            print("Invalid input, please be sure to only type a number between 1 & 4 and press enter")


# Retrieve Sessions based on Master ID
def getSessions(auth):
    # while loop to prevent script from ending on invalid input
    while True:
        masterId = input('Enter the master ID: ')
        masterId = masterId.replace(" ", '')

        sessionIDs = []

        if masterId.isdigit():
            print(masterId)
            logging.info('masterId value is {}'.format(masterId))
            logging.info('GET ' + base_url + 'masters/' + masterId + '/sessions')

            request = requests.get(base_url + 'masters/' + masterId + '/sessions', auth=auth)

            # If request is successful, append all session IDs to sessionIDs list
            # On failure, log status code and inform user
            if request.status_code == 200:
                response = request.json()
                logging.info(response)

                sessions = response['result']['sessions']

                for session in sessions:
                    sessionIDs.append(session['id'])
                
                findBrokenSessions(auth, sessionIDs)
                break
            else:
                print('Request failed with status code:' + request.status_code)
                logging.info('Request failed with status code:' + request.status_code)
        else:
            print('Could not find Master ID {}, please ensure to use only integers and try again.'.format(masterId))


# Iterates over previously aggregated sessions, checks each session to determine if it produced artifacts
def findBrokenSessions(auth, sessionIDs):
    brokenSessions = []

    # Iterate over sessions, retrieve files for each session, check for presence of artifacts && admin-artifacts
    for sessionId in sessionIDs:
        logging.info('masterId value is {}'.format(sessionId))
        logging.info('GET ' + base_url + 'masters/' + sessionId + '/sessions')

        working = False
        request = requests.get(base_url + 'sessions/' + sessionId + '/files', auth=auth)

        # If request is successful, iterate over files to determine if session failed
        # If not successful, log failure and inform user
        if request.status_code == 200:
            response = request.json()
            logging.info(response)
            files = response['result']['files']

            for entry in files:
                name = entry['name']
                if name == 'admin-artifacts.zip' or name == 'artifacts.zip':
                    working = True
                    break
            
            if working == False:
                brokenSessions.append(sessionId)
        else:
            print('Request failed with status code:' + str(request.status_code))
            logging.info('Request failed with status code:' + str(request.status_code))
    
    # Print out session IDs of failed sessions for user
    for brokenSessionId in brokenSessions:
        print(brokenSessionId)

    if len(brokenSessions) == 0:
        print("No failed sessions found :)")


# Downloads either the artifacts.zip files for all sessions or both the admin-artifacts and artifacts depending on user choice
def downloadArtifacts(auth):
    # while loop to prevent script from ending on invalid input
    while True:
        masterId = input('Enter the master ID: ')
        masterId = masterId.replace(" ", '')

        if masterId.isdigit():
            print(masterId)
            logging.info('masterId value is {}'.format(masterId))

            logging.info('GET' + base_url + 'masters/' + masterId + '/files')
            request = requests.get(base_url + 'masters/' + masterId + '/files', auth=auth)

            # Validate it request was successful, if so proceed, if not log it
            if request.status_code == 200:
                response = request.json()
                logging.info("Request successful with code: " + str(request.status_code))
                sessions = response['result']['sessions']
                break
            else:
                print('Request failed with status code:' + str(request.status_code))
                logging.info('Request failed with status code:' + str(request.status_code))
    
    # Check if user wants to download admin-artifacts
    while True:
        adminArtifactsYN = input('Would you like to also download the admin-artifacts (y/n): ')
        adminArtifactsYN = adminArtifactsYN.lower()
        adminArtifactsYN = adminArtifactsYN.replace(" ", '')
        print(adminArtifactsYN)

        if adminArtifactsYN == "y":
            adminArtifactsYN = True
            logging.info('User chose to also download admin-artifacts')
            break
        if adminArtifactsYN == "n":
            adminArtifactsYN = False
            logging.info('User chose to not download admin-artifacts')
            break
        else:
            print('Invalid input you entered {}, please type only y or n and press Enter'.format(adminArtifactsYN))
            continue

    # Download admin-artifacts && artifacts
    if adminArtifactsYN:
        count = 1
        for session in sessions:
            for files in session['files']:
                if files['name'] == 'admin-artifacts.zip' or files['name'] == 'artifacts.zip':
                    request2 = requests.get(files['link'], auth=auth)

                    # Validate it request was successful, if so proceed, if not log it
                    if request2.status_code == 200:
                        open(str(count) + "_" + files['name'], 'wb').write(request2.content)
                        logging.info("Request successful with code: " + str(request.status_code))
                        logging.info("Downloaded {} to directory ".format(str(count) + "_" + files['name']) + os.getcwd())
                    else:
                        print('Request failed with status code:' + str(request.status_code))
                        logging.info('Request failed with status code:' + str(request.status_code))
            count += 1
    
    # Download only artifacts
    if not adminArtifactsYN:
        count = 1
        for session in sessions:
            for files in session['files']:
                if files['name'] == 'artifacts.zip':
                    request2 = requests.get(files['link'], auth=auth)

                    # Validate it request was successful, if so proceed, if not log it
                    if request2.status_code == 200:
                        open(str(count) + "_" + files['name'], 'wb').write(request2.content)
                        logging.info("Request successful with code: " + str(request.status_code))
                        logging.info("Downloaded {} to directory ".format(str(count) + "_" + files['name']) + os.getcwd())
                    else:
                        print('Request failed with status code:' + str(request.status_code))
                        logging.info('Request failed with status code:' + str(request.status_code))
            count += 1
    return

def downloadFilesByName(auth):
    print("function content otw")
    return

def downloadFilesByType(auth):
    print("function content otw")
    return




auth = get_api_key()

# TODO:
#       Improve Session Identification (What number engine is it, etc.)
#       Add ability to download artifacts and other files -- artifacts downloading complete
#       Improve exception handling -- better, but not done