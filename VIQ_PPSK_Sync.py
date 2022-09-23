#!/usr/bin/env python3
import json
import requests
import getpass
import logging
import os
import pandas as pd
import numpy as np
from pprint import pprint


####################################
# written by:   Tim Smith
# e-mail:       tismith@extremenetworks.com
# date:         25th April 2022
# version:      2.0.0
####################################


## Enter Username and password
#XIQ_username = "enter your ExtremeCloudIQ Username"
#XIQ_password = "enter your ExtremeCLoudIQ password"
####OR###
## TOKEN permission needs - enduser
XIQ_token = "****"

usergroup_name = "enter usergroup name"

exclude_ex_accounts = []

#-------------------------
# logging
PATH = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(
    filename='{}/XIQ-VIQ-sync.log'.format(PATH),
    filemode='a',
    level=os.environ.get("LOGLEVEL", "INFO"),
    format= '%(asctime)s: %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
)

PATH = os.path.dirname(os.path.abspath(__file__))

URL = "https://api.extremecloudiq.com"
headers = {"Accept": "application/json", "Content-Type": "application/json"}

def GetaccessToken(XIQ_username, XIQ_password):
    url = URL + "/login"
    payload = json.dumps({"username": XIQ_username, "password": XIQ_password})
    response = requests.post(url, headers=headers, data=payload)
    if response is None:
        log_msg = "ERROR: Not able to login into ExtremeCloudIQ - no response!"
        logging.error(log_msg)
        raise TypeError(log_msg)
    if response.status_code != 200:
        log_msg = f"Error getting access token - HTTP Status Code: {str(response.status_code)}"
        try:
            data = response.json()
            if "error_message" in data:
                log_msg += f"\n\t{data['error_message']}"
        except:
            log_msg += ""
        logging.error(f"{log_msg}")
        raise TypeError(log_msg)
    data = response.json()

    if "access_token" in data:
        #print("Logged in and Got access token: " + data["access_token"])
        headers["Authorization"] = "Bearer " + data["access_token"]
        return 0

    else:
        log_msg = "Unknown Error: Unable to gain access token"
        logging.warning(log_msg)
        raise TypeError(log_msg)

def retrievePPSKUsers(pageSize, usergroupID):
    page = 1
    pageCount = 1
    firstCall = True

    ppskUsers = []

    while page <= pageCount:
        url = URL + "/endusers?page=" + str(page) + "&limit=" + str(pageSize) + "&user_group_ids=" + str(usergroupID)

        # Get the next page of the ppsk users
        response = requests.get(url, headers=headers, verify = True)
        if response is None:
            log_msg = "Error retrieving PPSK users from XIQ - no response!"
            logging.error(log_msg)
            raise TypeError(log_msg)

        elif response.status_code != 200:
            log_msg = f"Error retrieving PPSK users from XIQ - HTTP Status Code: {str(response.status_code)}"
            logging.error(log_msg)
            logging.warning(f"\t\t{response.json()}")
            raise TypeError(log_msg)

        rawList = response.json()
        ppskUsers = ppskUsers + rawList['data']

        if firstCall == True:
            pageCount = rawList['total_pages']
            firstCall = False
        if rawList['total_pages'] > 0:
            print(f"completed page {page} of {rawList['total_pages']} collecting PPSK Users")
        else:
            print(f"There are no users in the PPSK user group")
        page = rawList['page'] + 1 
    return ppskUsers

def get_external_accounts():
    url = URL + "/account/external"
    response = requests.get(url, headers=headers)
    if response is None:
        log_msg = f"ERROR: Not able to get external accounts for this user!"
        raise TypeError(log_msg)
    if response.status_code != 200:
        log_msg = f"Error receiving external accounts - HTTP Status Code: {str(response.status_code)}"
        try:
            data = response.json()
            if "error_message" in data:
                log_msg += f"\n\t{data['error_message']}"
        except:
            log_msg += ""
        logging.error(log_msg)
        raise TypeError(log_msg)
    data = response.json()
    return(data)

def switch_XIQ_Account(account):
    url = URL + "/account/:switch?id=" + str(account)
    response = requests.post(url, headers=headers)
    if response is None:
        log_msg = f"ERROR: Not able to generate token for account {account}!"
        raise TypeError(log_msg)
    if response.status_code != 200:
        log_msg = f"Error generating token for account {account} - HTTP Status Code: {str(response.status_code)}"
        try:
            data = response.json()
            if "error_message" in data:
                log_msg += f"\n\t{data['error_message']}"
        except:
            log_msg += ""
        logging.error(log_msg)
        raise TypeError(log_msg)
    data = response.json()

    if "access_token" in data:
        #print("Logged in and Got access token: " + data["access_token"])
        headers["Authorization"] = "Bearer " + data["access_token"]
        return 0

    else:
        log_msg = "Unknown Error: Unable to gain access token"
        logging.warning(log_msg)
        raise TypeError(log_msg)

def get_usergroup_id(usergroup_name):
    grpid = ''
    url  = URL + "/usergroups"
    response = requests.get(url, headers=headers)
    if response is None:
        log_msg = f"ERROR: Not able to get user group info for this user!"
        raise TypeError(log_msg)
    if response.status_code != 200:
        log_msg = f"Error receiving user group info - HTTP Status Code: {str(response.status_code)}"
        try:
            data = response.json()
            if "error_message" in data:
                log_msg += f"\n\t{data['error_message']}"
        except:
            log_msg += ""
        logging.error(log_msg)
        raise TypeError(log_msg)
    data = response.json()
    # check defined name and get id
    for group in data['data']:
        if usergroup_name == group['name']:
            grpid = group['id']
    if grpid:
        return grpid
    else:
        logging.error(f"group {usergroup_name} not found")
        raise ValueError("Group Not found")

def CreatePPSKuser(payload, name):
    url = URL + "/endusers"

    #print("Trying to create user using this URL and payload " + url)
    response = requests.post(url, headers=headers, data=payload, verify=True)
    if response is None:
        log_msg = "Error adding PPSK user - no response!"
        logging.error(log_msg)
        raise TypeError(log_msg)

    elif response.status_code != 200:
        log_msg = f"Error adding PPSK user {name} - HTTP Status Code: {str(response.status_code)}"
        try:
            data = response.json()
            if "error_message" in data:
                log_msg += f"\n\t{data['error_message']}"
        except:
            log_msg += ""
        logging.error(log_msg)
        raise TypeError(log_msg)

    elif response.status_code ==200:
        logging.info(f"successfully created PPSK user {name}")
        print(f"successfully created PPSK user {name}")
    #print(response)

def deleteuser(userId):
    url = URL + "/endusers/" + str(userId)
    #print("\nTrying to delete user using this URL and payload\n " + url)
    response = requests.delete(url, headers=headers, verify=True)
    if response is None:
        log_msg = f"Error deleting PPSK user {userId} - no response!"
        logging.error(log_msg)
        raise TypeError(log_msg)
    elif response.status_code != 200:
        log_msg = f"Error deleting PPSK user {userId} - HTTP Status Code: {str(response.status_code)}"
        try:
            data = response.json()
            if "error_message" in data:
                log_msg += f"\n\t{data['error_message']}"
        except:
            log_msg += ""
        logging.error(log_msg)
        raise TypeError(log_msg)
    elif response.status_code == 200:
        return 'Success'
    #print(response)

def main():
    print("\n")
    ## Get token for Main Account ##
    if not XIQ_token:
        try:
            login = GetaccessToken(XIQ_username, XIQ_password)
        except TypeError as e:
            print(e)
            raise SystemExit
        except:
            log_msg = "Unknown Error: Failed to generate token"
            print(log_msg)
            raise SystemExit  
    else:
        headers["Authorization"] = "Bearer " + XIQ_token 

    ## get ppsk users for usergroup ##
    try:
        usergroupID= get_usergroup_id(usergroup_name)
    except TypeError as e:
        print(e)
        raise SystemExit
    except ValueError as e:
        print(e)
        raise SystemExit
    mst_ppsk_users = retrievePPSKUsers(100, usergroupID)

    ## get external accounts ##
    ex_accts = get_external_accounts()
    for account in ex_accts:
        print(f"\nStarting VIQ {account['alias']}...\n")
        if account['alias'] in exclude_ex_accounts:
            print(f"The {account['alias']} account is in the excluded list and will be skipped")
            continue
        try:
            switch_XIQ_Account(account['id'])
        except TypeError as e:
            print(e)
            print(f"Skipping connection to {account['alias']}.")
            continue
            
        except:
            log_msg = "Unknown Error: Failed to generate token"
            print(log_msg)
            print(f"Skipping connection to {account['alias']}.")
            continue

        ## GET group ID ##
        try:
            usergroupID= get_usergroup_id(usergroup_name)
        except TypeError as e:
            print(f"{e} on {account['alias']}")
            continue
        except ValueError as e:
            print(f"{e} on {account['alias']}")
            continue

        try:
            acc_ppsk_users = retrievePPSKUsers(100,usergroupID)
        except TypeError as e:
            print(e)
            print(f"Failed to collect PPSK users on {account['alias']}.")
            print(f"Skipping {account['alias']}.")
            continue
        except:
            log_msg = ("Unknown Error: Failed to retrieve users from XIQ")
            logging.error(log_msg)
            print(log_msg)
            print(f"Failed to collect PPSK users on {account['alias']}.")
            print(f"Skipping {account['alias']}.")
            continue
        
 
        for row in mst_ppsk_users:
            if any(row['user_name'] in x['user_name'] for x in acc_ppsk_users):
                log_msg = (f"User {row['user_name']} already exists, skipping user")
                logging.info(log_msg)
                print(log_msg)
            else:

                payload = json.dumps({"user_group_id": usergroupID ,
                "name": f"{row['name']}",
                "user_name": row['user_name'],
                "organization": row['organization'],
                "visit_purpose": row['visit_purpose'],
                "description": row['description'],
                "email_address": row['email_address'],
                "phone_number": row['phone_number'],
                "password": row['password'],
                "email_password_delivery": "",
                "sms_password_delivery": ""})
                try:
                    CreatePPSKuser(payload, row['user_name'])
                except TypeError as e:
                    log_msg = f"failed to create {row['user_name']}: {e}"
                    print(log_msg)
                except:
                    log_msg = f"Unknown Error: Failed to create user {row['user_name']} - {row['email_address']}"
                    print(log_msg)
        
        for acc_ppsk_user in acc_ppsk_users:
            if not any(acc_ppsk_user['user_name'] == d['user_name'] for d in mst_ppsk_users):   
                ## Delete PPSK user ##
                try:
                    result= deleteuser(acc_ppsk_user['id'])
                except TypeError as e:
                    logmsg = f"Failed to delete user {acc_ppsk_user['user_name']}  with error {e}"
                    logging.error(logmsg)
                    print(logmsg)
                    continue
                except:
                    log_msg = f"Unknown Error: Failed to create user {acc_ppsk_user['user_name']} "
                    logging.error(log_msg)
                    print(log_msg)
                    continue
                if result == 'Success':
                    log_msg = f"User {acc_ppsk_user['user_name']} - {acc_ppsk_user['id']} was successfully deleted."
                    logging.info(log_msg)
                    print(log_msg)  
        
if __name__ == '__main__':
	main()