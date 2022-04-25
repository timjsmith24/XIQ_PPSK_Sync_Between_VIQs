# XIQ - Sync Externally Managed VIQ PPSK Users
## VIQ_PPSK_Sync.py
### Purpose
This script will collect the PPSK Users from a the main VIQ account and create those same PPSK Users in all Externally Managed VIQs. The name of the user group needs to be the same on all managed accounts, including the viq they export from. If you have a specific Managed VIQ(s) you want to skip you can add the Name of the VIQ to the script to be excluded.
## User Input Data

In order for the script to run successfully, the XIQ account username and password will need to be entered, or ideally, a token generated from that account with enduser permissions.

### XIQ username and password (This can be skipped if entering a generated token)
>NOTE: The preferred method is to not include the username and password but use a token with specified permissions. In order to use a username and password, the #'s need to be removed at the beginning of the following lines.
##### lines 20-22
```
## Enter Username and password
#XIQ_username = "enter your ExtremeCloudIQ Username"
#XIQ_password = "enter your ExtremeCLoudIQ password"
```
### XIQ token with enduser permission (Only needed if username and password are not provided.)
```
## TOKEN permission needs - enduser
XIQ_token = "****"
```
### The name of the XIQ usergroup you would like to sync users.
```
usergroup_name = "enter usergroup name"
```
### Managed VIQ(s) to skip (Optional)
>##### lines 29
```
exclude_ex_accounts = []
```
inside of the brackets enter the name of the VIQs you want to skip. Each name should be entered within quotes. If multiple names are entered they should be separated by a comma.
>##### Example:
>```
>exclude_ex_accounts = ["va2-Lab","JP_Lab"]
>```

## Script Outputs
#### Terminal Window
```
python VIQ_PPSK_Sync.py 

completed page 1 of 1 collecting PPSK Users

Starting VIQ JP_Lab...

User tim@smithhome.com already exists, skipping user
User miles@smithhome.com already exists, skipping user
User adele@smithhome.com already exists, skipping user
User bauer@smithhome.com already exists, skipping user
User tripp@smithhome.com already exists, skipping user
User kayce@smithhome.com - 1059916324374249 was successfully deleted.

Starting VIQ Tim - SC - Lab...

successfully created PPSK user tim@smithhome.com
successfully created PPSK user miles@smithhome.com
successfully created PPSK user adele@smithhome.com
successfully created PPSK user bauer@smithhome.com
successfully created PPSK user tripp@smithhome.com
```

The script will check to see if the user already exists. If it does, the user will be skipped.
If a user exists in the PPSK Group and is not in the csv file, the script will delete the user from the PPSK Group.