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

#scopes = ['https://www.googleapis.com/auth/sqlservice.admin','https://www.googleapis.com/auth/spreadhseets']
scopes = ['https://www.googleapis.com/auth/spreadsheets']


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    #store = oauth2client.file.Storage(credential_path)
    #credentials = store.get()
    credentials = ServiceAccountCredentials.from_json_keyfile_name('project_key.json', scopes)
    """
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    """
    return credentials

def main():
    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/E2upms/edit
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '%s' % config_spreadsheet

    rangeName = 'A2:D'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])
    
    ink_level = int(values[0][3])
    #print ('%s' % ink_level)
    #print bool_flag

    if (ink_level < 58 and bool_flag==0):
	print ('Ink is low!')
        os.system(cmd)
	#d = {"sent_flag":{"flag":1}}
	with open('config.json', 'r') as f:
	    d = json.load(f)
	    d["sent_flag"]["flag"] = 1
	with open('config.json', 'w') as f:
	    json.dump(d,f)
    elif (ink_level > 57 and bool_flag==1):
	#d = {"sent_flag":{"flag":0}}
	with open('config.json', 'r') as f:
	    d = json.load(f)
	    d["sent_flag"]["flag"] = 0 
	with open('config.json', 'w') as f:
	    json.dump(d,f)
        
    
    """
    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s' % (row[0], row[3]))
    """

if __name__ == '__main__':
    main()
