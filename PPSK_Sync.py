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
# date:         3rd December 2021
# version:      1.0.0
####################################


print("Enter your XIQ login credentials")
XIQ_username = input("Email: ")
XIQ_password = getpass.getpass("Password: ")

print("\nMake sure the csv file is in the same folder as the python script.")
filename = input("Please enter csv filename: ")

print("\nMake sure the PPSK group exists in each VIQ.")
usergroup_name = input("Please enter PPSK group name: ")

exclude_ex_accounts = []
XIQ_token = ''

PATH = os.path.dirname(os.path.abspath(__file__))

URL = "https://api.extremecloudiq.com"
headers = {"Accept": "application/json", "Content-Type": "application/json"}

def GetaccessToken(XIQ_username, XIQ_password):
    url = URL + "/login"
    payload = json.dumps({"username": XIQ_username, "password": XIQ_password})
    response = requests.post(url, headers=headers, data=payload)
    if response is None:
        log_msg = "ERROR: Not able to login into ExtremeCloudIQ - no response!"
        raise TypeError(log_msg)
    if response.status_code != 200:
        log_msg = f"Error getting access token - HTTP Status Code: {str(response.status_code)}"
        try:
            data = response.json()
            if "error_message" in data:
                log_msg += f"\n\t{data['error_message']}"
        except:
            log_msg += ""
        raise TypeError(log_msg)
    data = response.json()

    if "access_token" in data:
        #print("Logged in and Got access token: " + data["access_token"])
        headers["Authorization"] = "Bearer " + data["access_token"]
        return 0

    else:
        log_msg = "Unknown Error: Unable to gain access token"
        raise TypeError(log_msg)

def retrievePPSKusers(pageSize, usergroupID):
    #print("Retrieve all PPSK users  from ExtremeCloudIQ")
    page = 1

    ppskusers = []

    while page < 1000:
        url = URL + "/endusers?page=" + str(page) + "&limit=" + str(pageSize) + "&user_group_ids=" + str(usergroupID)
        #print("Retrieving next page of PPSK users from ExtremeCloudIQ starting at page " + str(page) + " url: " + url)

        # Get the next page of the ppsk users
        response = requests.get(url, headers=headers, verify = True)
        if response is None:
            log_msg = "Error retrieving PPSK users from XIQ - no response!"
            raise TypeError(log_msg)
        elif response.status_code != 200:
            log_msg = f"Error retrieving PPSK users from XIQ - HTTP Status Code: {str(response.status_code)}"
            try:
                data = response.json()
                if "error_message" in data:
                    log_msg += f"\n\t{data['error_message']}"
            except:
                log_msg += ""
            raise TypeError(log_msg)
        rawList = response.json()['data']
        #for name in rawList:
        #    print(name)
        #print("Retrieved " + str(len(rawList)) + " users on this page")
        ppskusers = ppskusers + rawList
        if len(rawList) == 0:
            #print("Reached the final page - stopping to retrieve users ")
            break
        page = page + 1
    return ppskusers

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
        raise TypeError(log_msg)
    data = response.json()

    if "access_token" in data:
        #print("Logged in and Got access token: " + data["access_token"])
        headers["Authorization"] = "Bearer " + data["access_token"]
        return 0

    else:
        log_msg = "Unknown Error: Unable to gain access token"
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
        raise TypeError(log_msg)
    data = response.json()
    # check defined name and get id
    for group in data['data']:
        if usergroup_name == group['name']:
            grpid = group['id']
    if grpid:
        return grpid
    else:
        raise ValueError("Group Not found")

def CreatePPSKuser(payload, name):
    url = URL + "/endusers"

    #print("Trying to create user using this URL and payload " + url)
    response = requests.post(url, headers=headers, data=payload, verify=True)
    if response is None:
        log_msg = "Error adding PPSK user - no response!"
        raise TypeError(log_msg)

    elif response.status_code != 200:
        log_msg = f"Error adding PPSK user {name} - HTTP Status Code: {str(response.status_code)}"
        try:
            data = response.json()
            if "error_message" in data:
                log_msg += f"\n\t{data['error_message']}"
        except:
            log_msg += ""
        raise TypeError(log_msg)

    elif response.status_code ==200:
        print(f"successfully created PPSK user {name}")
    #print(response)

def deleteuser(userId):
    url = URL + "/endusers/" + str(userId)
    #print("\nTrying to delete user using this URL and payload\n " + url)
    response = requests.delete(url, headers=headers, verify=True)
    if response is None:
        log_msg = f"Error deleting PPSK user {userId} - no response!"
        raise TypeError(log_msg)
    elif response.status_code != 200:
        log_msg = f"Error deleting PPSK user {userId} - HTTP Status Code: {str(response.status_code)}"
        try:
            data = response.json()
            if "error_message" in data:
                log_msg += f"\n\t{data['error_message']}"
        except:
            log_msg += ""
        raise TypeError(log_msg)
    elif response.status_code == 200:
        return 'Success'
    #print(response)

def main():
    print("\n")
    ##  load CSV file   ##
    if os.path.isfile(PATH + '/' + filename):
        try:
            df = pd.read_csv(PATH + '/' + filename)
        except:
            print(f"failed to load file {filename}")
            print("script exiting....")
            raise SystemExit
    else:
        print(f"The file {filename} was not in {PATH}")
        print("script exiting....")
        raise SystemExit
    
    df = df.replace(np.nan," ")
    filt = df['User Group Name'] == usergroup_name
    mst_ppsk_users = (df.loc[filt])
    
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
            acc_ppsk_users = retrievePPSKusers(100,usergroupID)
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
        
        for index, row in mst_ppsk_users.iterrows():
            if any(row['User Name'] in x['user_name'] for x in acc_ppsk_users):
                
                print(f"User {row['User Name']} already exists, skipping user")
            else:
                #print(row)
                '''
                Index(['User Name', 'User Group Name', 'User Type', 'Password', 'Email',
                    'Delivery Email', 'Delivery Phone', 'Description', 'Expiration',
                    'First Name', 'Last Name', 'Phone', 'Organization', 'Visiting Purpose',
                    'PPSK', 'Password NT', 'Encrypted Password'],
                     dtype='object')
                     '''
                payload = json.dumps({"user_group_id": usergroupID ,
                "name": f"{row['First Name']} {row['Last Name']}",
                "user_name": row['User Name'],
                "organization": row['Organization'],
                "visit_purpose": row['Visiting Purpose'],
                "description": row['Description'],
                "email_address": row['Email'],
                "phone_number": row['Phone'],
                "password": row['Password'],
                "email_password_delivery": "",
                "sms_password_delivery": ""})
                try:
                    CreatePPSKuser(payload, row['User Name'])
                except TypeError as e:
                    log_msg = f"failed to create {row['User Name']}: {e}"
                    print(log_msg)
                except:
                    log_msg = f"Unknown Error: Failed to create user {row['User Name']} - {row['Email']}"
                    print(log_msg)
        
        for acc_ppsk_user in acc_ppsk_users:
            if acc_ppsk_user['user_name'] not in mst_ppsk_users.values:
                
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