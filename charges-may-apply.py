from __future__ import print_function
import httplib2
import os
import sys
import json
import shelve
from pprint import pprint

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

#Load the config.json and return a dictionary for the check_cell function to use
"""
def load_config():
	with open('config.json') as data_file:
		return json.load(data_file)
"""
def load_config():
	with open('config.json') as data_file:
		data = json.load(data_file)
		#print (data)
		#return data["inventories"]
		return data

#Function checks for flag file. If file is not present (first run), the function creates it.
def check_for_flags_file():	
    if os.path.isfile('.flags') == False:	
        s = shelve.open('.flags', writeback=True)
	with open('config.json') as f:
		temp_dict = json.load(f) 
		list_dict = temp_dict["inventories"]	
        list_of_ids = []
        for i in list_dict:
                list_of_ids.append(i["inventory_id"])
        number_of_inventories = len(list_of_ids)
        zeroes = [0 for x in range(number_of_inventories)]
        sent_flags = dict(zip(list_of_ids,zeroes))
        s.close()
    else:
    	print ("File exists")

def check_if_sent(this_id):
	s = shelve.open('.flags')
	s_string = s['%s' % this_id]
	return s_string
	s.close()

def set_flag_to_1(this_id):
	s = shelve.open('.flags', writeback=True)
	s['%s' % this_id] = 1
	s.close()

def set_flag_to_0(this_id):
	s = shelve.open('.flags', writeback=True)
	s['%s' % this_id] = 0
	s.close()

def check_cell(cell_to_check, threshold, this_inv_id, command):
	if (cell_to_check < threshold and check_if_sent(this_inv_id) == 0):
		#Debug statement
		#print ("Low on inventory")
		os.system(command)
		set_flag_to_1(this_inv_id)
	elif (cell_to_check > threshold and check_if_sent(this_inv_id) ==1):
		set_flag_to_0(this_inv_id)

def main():
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?''version=v4')
	service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)
	data = load_config()
	check_for_flags_file()

	#Create a dictionary from the config.json
	inventories_dict_list = load_config()
	#Check if the script has run once by looking for the .flags file
	#check_for_flags_file(**inventories_dict)
	#Define variables that don't change per inventory
	from_email = data["sendemail"]["from"]
	to_email = data["sendemail"]["to"]
	username = data["sendemail"]["user"]
	password = data["sendemail"]["pass"]
	spreadsheetId = data["google_api"]["spreadsheetId"]

	#Turn dict_list into dict
	inventories_dict = inventories_dict_list["inventories"]
	#Iterate over the dictionaries to get the variables for each inventory
	#Perform the check and flag funcitons on each inventory
	
	for i in inventories_dict:
		#Define the variable that are unique to each inventory
		inventory_id = i["inventory_id"]
		target_cell = i["target_cell"]
		threshold_value = i["threshold"]
		subject = i["subject"]
		message = i["message"]
		#Define Sheets variables
		rangeName = '%s' % target_cell
		#Get the value using the API
		results = service.spreadsheets().values().get(
			spreadsheetId=spreadsheetId, range=rangeName).execute()
		values = results.get('values', [])
		#Define the sendemail command
		cmd = ('sendemail -f "%s" -t "%s" -u "%s" -m "%s" -s smtp.gmail.com:587 -xu "%s" -xp "%s"' % (from_email, to_email, subject, message, username, password))
	
		check_cell(values, threshold_value, inventory_id, cmd)

if __name__ == '__main__':
    main()
