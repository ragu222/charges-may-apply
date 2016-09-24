# charges-may-apply
--
##Description
The goal of this project is to send an alert via text message to a mobile number when the value in a specific Google Sheet cell falls below a certain threshold.


##Instructions
The basic flow goes like this: Python script pulls a value from a Sheet using the Sheets API --> Python compares that value to a threshold number that you define --> If the value is lower than the threshold number the script uses an app called 'sendemail' to send an email to your carrier's email-to-txt service which, in turn, texts you with a message of your choice.

There are a lot of steps so I'm going to break this section down into sub-sections corresponding to those steps I just outlined above.

###Set up the server
Spin up a linux server. This example uses Ubuntu 14.04, so if you're using something else you're obviously going to have to replace 'apt' with 'yum', etc. (Just use Ubuntu)

First install the **sendemail** app and it's dependencies:

`ragu222@ubuntu-14.04:~$ sudo apt-get install libio-socket-ssl-perl libssl-dev sendemail`

My carrier is AT&T so I can only vouch for them. [This](https://goo.gl/fMHAfa) is a list of other carriers' email-to-sms domains. Good luck.

FYI I created a dummy email (emailbot@wrightesd.org) so that I didn't have a real user's password sitting around in plain text. And if you do this remember to log into the dummy account at least once to make sure you can actually send emails from it.

Next install `git`:

`ragu222@ubuntu-14.04:~$ sudo apt-get install git`

and clone this repo:

`ragu222@ubuntu-14.04:~$ sudo git clone https://github.com/ragu222/charges-may-apply`

If you're not familiar with `git` don't sweat it. The details are really not important for this demo. We're basically copying this directory(containing this Readme.md file and the charges-may-apply.py python script, and the config.json) onto your local machine. That's it.

Note that when you clone the repository it creates a new directory with the same name. You want to use that as your working directory for the rest of the demo:

`cd ./charges-may-apply`

Next you want to edit the config file to replace the default values with your real values. And DON'T TOUCH the *sent_flag* or *flag* values! You've been warned.

`vi config.json`

You don't have to use vi. You can use whatever editor you want (you really should use vi, though).

```json
{
  "sendemail": {
      "from":"your_email@your_domain.org",
      "to"  :"7075551234@txt.att.net",
      "user":"your_email@your_domain.org",
      "pass":"password"
  },
  "sent_flag": {
      "flag":0
  }
}
```

###Python script

Next, install `pip`. If you're not familiar with Python, `pip` is Python's package installer. You'll need a couple of non-default python packages to work with the Google Sheets API:


`ragu222@ubuntu-14.04:~$ sudo apt-get install pip`

Then use pip to install those packages:

`ragu222@ubuntu-14.04:~$ sudo pip install httplib2 google-api-python-client`


###Google Sheets

####API

Next you have to create a Service Account in the Google Developer Console. This creates an email address (this is important because you'll need to share your Sheet with this Service Account email address later) and generates a key pair that you'll download as a json file into your working directory.

[Here](https://developers.google.com/sheets/quickstart/python) and [here](https://developers.google.com/identity/protocols/OAuth2ServiceAccount) are the official Google references. They're fairly complete, but I'm going to walk through it here again with pictures because it took me a few tries to get it right.

####Create the Sheet

I'm going to go ahead and assume you know how to create a Google Sheet so this section's pretty sparse.

You can make the Sheet look however you want, but remember that this demo is looking at cell D2. So if you want to change the target cell in your Sheet make sure to reflect that change in the python script.

The most important part of this step is to share the Sheet with your Service Account email address. That address is found [here.](https://console.cloud.google.com/iam-admin/serviceaccounts/)

###Cron

`ragu222@ubuntu-14.04:~/charges-may-apply$ crontab -e`

If this is your first crontab it's going ask you which editor you want to use (vi).

Add this entry to the bottom of the file and save it:

`*/5 * * * /usr/bin/python /home/yourusernamehere/charges-may-apply.py`

This crontab entry checks the Sheet every 5 minutes. If you want to change that interval this is where to do it.

##Conclusion

That's it! Have fun.

###PS
It's late. I'll clean up the code later.


