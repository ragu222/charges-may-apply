# charges-may-apply
--
###\*UPDATE\*
I updated the the code so that it's much cleaner. It looks a little more polished instead of a proof of concept, but it's basically doing the same thing as before.

##Description
The goal of this project is to send an alert via text message to a mobile number when the value in a specific Google Sheet cell falls below a certain threshold.


##Instructions
The basic flow goes like this: Python script pulls a value from a Sheet using the Sheets API --> Python compares that value to a threshold number that you define --> If the value is lower than the threshold number the script uses an app called 'sendemail' to send an email to your carrier's email-to-txt service which, in turn, texts you with a message of your choice.

###Set up the server
Spin up a linux server. This example uses Ubuntu 14.04, so if you're using something else you're obviously going to have to replace 'apt' with 'yum', etc. (Just use Ubuntu)

First install the **sendemail** app and it's dependencies:

```bash
ragu222@ubuntu-14.04:~$ sudo apt-get install libio-socket-ssl-perl libssl-dev sendemail
```

My carrier is AT&T so I can only vouch for them. [This](https://goo.gl/fMHAfa) is a list of other carriers' email-to-sms domains. Good luck.

FYI I created a dummy email (emailbot@wrightesd.org) so that I didn't have a real user's password sitting around in plain text. And if you do this remember to log into the dummy account at least once to make sure you can actually send emails from it.

Next install `git`:

```bash
ragu222@ubuntu-14.04:~$ sudo apt-get install git
```

and clone this repo:

```bash
ragu222@ubuntu-14.04:~$ git clone https://github.com/ragu222/charges-may-apply
```

If you're not familiar with `git` don't sweat it. The details are really not important for this demo. We're basically copying this directory(containing this Readme.md file and the charges-may-apply.py python script, and the config.json) onto your local machine. That's it.

Note that when you clone the repository it creates a new directory with the same name. You want to use that as your working directory for the rest of the demo:

```bash
ragu222@ubuntu-14.04:~$ cd ./charges-may-apply
```

Next you want to edit the config file to replace the default values with your real values.

```bash
ragu222@ubuntu-14.04:~/charges-may-apply$ vi config.json
```
```json
{
	"sendemail": {
		"from":"your_email@your_domain.org",
		"to"  :"7075551234@txt.att.net",
		"user":"your_email@your_domain.org",
		"pass":"your_password_here"
	},
	"google_api": {
		"spreadsheetId":"18Rtd53P1SXAuhD3XNnQozALflWJxMitJQnSCtyxXP5o"
	},
	"inventories": [
		{
			"inventory_id":112,
			"title":"Elephants",
			"descr":"How many elephants are left?",
			"target_cell":"D2",
			"threshold":"50",
			"subject":"This is the subject ",
			"message":"You're low on elephants!",
		},
		{
			"inventory_id":555,
			"title":"Tigers",
			"descr":"How many elephants are left?",
			"target_cell":"D2",
			"threshold":"50",
			"subject":"This is the subject ",
			"message":"You're low bears !",
		}
	 ]
}
```
A few things about the config.json file:

	+ The inventory_id must be unique and an integer. I chose those 2 random numbers to help me debug.
	+ You can make the target cell whatever you want.
	+ If you want to check more than two inventories just copy and paste a block (including the curly brackets), and change the inventory_id.
	
Your google sheet ID you won't know until you create you Sheet. Once you've created it come back and fill this part in. The googlesheetId is the part of the Sheets link that is a long string of letters and numbers.
```https://docs.google.com/spreadsheets/d/**18Rtd53P1SXAuhD3XNnQozALflWJxMitJQnSCtyxXP5o**/edit#gid=0```

The sheetId in this example config is a Sheet that I own. If you want to use it to try out this code just let me know and I'll share the service account email and the key with you.

###Python script

Next, install `pip`. If you're not familiar with Python, `pip` is Python's package installer. You'll need a couple of non-default python packages to work with the Google Sheets API:


```bash
ragu222@ubuntu-14.04:~/charges-may-apply$ sudo apt-get install pip
```

Then use pip to install those packages:

```bash
ragu222@ubuntu-14.04:~/charges-may-apply$ sudo pip install httplib2 google-api-python-client
```


###Google Sheets

####API

Next you have to create a Service Account in the Google Developer Console. This creates an email address (this is important because you'll need to share your Sheet with this Service Account email address later) and generates a key pair that you'll download as a json file into your working directory.

[Here](https://developers.google.com/sheets/quickstart/python) are the official instructions and [this](https://developers.google.com/identity/protocols/OAuth2ServiceAccount) is a good reference. They're fairly complete, but I think in the near future I'm going to add some details and pictures here because it was a little tricky getting this part right.

After you download the key from Google, copy it into your working directory and rename it project_key.json


####Create the Sheet

I'm going to go ahead and assume you know how to create a Google Sheet so this section's pretty sparse.

You can make the Sheet look however you want, but remember that this demo is looking at cell D2. So if you want to change the target cell in your Sheet make sure to reflect that change in the python script.

The most important part of this step is to share the Sheet with your Service Account email address. That address is found [here.](https://console.cloud.google.com/iam-admin/serviceaccounts/)

###Cron

You should probably run the python script once to make sure it's actually pulling data and that it's texting your phone.

```bash
ragu222@ubuntu-14.04:~/charges-may-apply$ python charges-may-apply.py
```
Once you know that runs without error you want to run that every 5 minutes (or however often you want to check the Sheet cell). You do this by creating a cron job.

**Note** 
I also set a flag in the config.json file that says, "I sent a text message, stop sending text messages." Otherwise the script will keep sending you a text message every 5 minutes as long as the inventory is low.

If this is your first crontab it's going ask you which editor you want to use (vi).

Add this entry to the bottom of the file and save it:

`*/5 * * * /usr/bin/python /home/yourusernamehere/charges-may-apply.py`

This crontab entry checks the Sheet every 5 minutes. If you want to change that interval this is where to do it.

##Miscellaneous

If you add or remove inventories to check you will have to delete the hidden ```.flags``` file before running the script again:

```bash
rm .flags
```
The script will automatically create the file again on it's subsequent run.

##Conclusion

That's it! Have fun.



