from __future__ import print_function
import httplib2
import os
import sys
import json
from pprint import pprint

with open('config.json') as data_file:
    data = json.load(data_file)

bool_flag = int(data["sent_flag"]["flag"])

from_email = data["sendemail"]["from"]
to_email = data["sendemail"]["to"]
user = data["sendemail"]["user"]
password = data["sendemail"]["pass"]
config_spreadsheet = data["google_api"]["spreadsheetId"]

cmd = ('sendemail -f "%s" -t "%s" -u "Inventory Alert" -m "Ink low!" -s smtp.gmail.com:587 -o tls=yes -xu "%s" -xp "%s"' % (from_email, to_email, user, password))


from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
from oauth2client.service_account import ServiceAccountCredentials

scopes = ['https://www.googleapis.com/auth/spreadsheets']


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    credentials = ServiceAccountCredentials.from_json_keyfile_name('project_key.json', scopes)
    return credentials

def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '%s' % config_spreadsheet
    
    #This line defines the range
    rangeName = 'A2:D'
    #These two lines put the values from the spreadsheet into a dictionary of tuples called 'values'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    #This line looks assigns a cell value to a variable to a variable called 'ink_level'
    #Both the variable name and the cell are arbitrary. They're chosen randomly for this example
    ink_level = int(values[0][3])
   
    #The next line is a debug line. I used it to make sure that the variable holds the value I think it should
    #print ('%s' % ink_level)
    #print bool_flag

    #This next block of code checks to see if the cell value is below the threshold
    #The 'print' line is debug
    #The 'os.system(cmd) is executing the sendemail binary
    #Lastly it checks to see if the txt has been sent already. If it has then it won't keep sending the alert every 5 minutes
    #or however long the cron job is set to check

    if (ink_level < 58 and bool_flag==0):
	print ('Ink is low!')
        os.system(cmd)
	with open('config.json', 'r') as f:
	    d = json.load(f)
	    d["sent_flag"]["flag"] = 1
	with open('config.json', 'w') as f:
	    json.dump(d,f)
    elif (ink_level > 57 and bool_flag==1):
	with open('config.json', 'r') as f:
	    d = json.load(f)
	    d["sent_flag"]["flag"] = 0 
	with open('config.json', 'w') as f:
	    json.dump(d,f)
        
if __name__ == '__main__':
    main()
