# XIQ - Sync Externally Managed VIQ PPSK Users
## PPSK_Sync.py
### Purpose
This script will import a CSV export of PPSK Users from a VIQ and create those same PPSK Users in all Externally Managed VIQs. The name of the user group needs to be the same on all managed accounts, including the viq the export was from. If you have a specific Managed VIQ(s) you want to skip you can add the Name of the VIQ to the script to be excluded.
## User Input Data
the exported csv file should be downloaded from the account to sync from. This csv file should be moved into the same folder as the script.

Most of the user inputs will be done using prompts once the script is ran. 

When ran, the script will as the user for the XIQ login credentials, the name of the csv file, and the name of the PPSK group. 

### Managed VIQ(s) to skip (Optional)
>##### lines 30
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
python PPSK_Sync.py 
Enter your XIQ login credentials
Email: timjsmith24@gmail.com
Password: 

Make sure the csv file is in the same folder as the python script.
Please enter csv filename: ExportedUsers.csv

Make sure the PPSK group exists in each VIQ.
Please enter PPSK group name: PPSK_Test



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