# charges-may-apply
--
##Description
The goal of this project is to text an alert to a mobile number when a cell in a Google Sheet falls below a certain value


##Instructions
Spin up a linux server. This example uses Ubuntu 14.04, so if you're using something else you're obviously going to have to replace 'apt' with 'yum', etc. (Just use Ubuntu)

First install the **sendemail** app and it's dependencies:

`sudo apt-get install libio-socket-ssl-perl libssl-dev sendemail`

and configure it:

`vi config.json`

You don't have to use vi, you can use whatever editor you want (you should be using vi).

Make sure to replace the default values with your real values. And DON'T TOUCH the *sent_flag* or *flag* values. You've been warned.

```json
{
  "sendemail": {
      "from":"your_email@your_domain.org",
      "to"  :"7075551234@txt.att.net",
      "user":"your_email@your_domain.org",
      "pass":"password"
  }
  "sent_flag": {
      "flag":0
  }
}
```
My carrier is AT&T so I can only vouch for them. [Here](https://goo.gl/fMHAfa) are the other carriers' email-to-sms domains. Good luck. https://goo.gl/fMHAfa

FYI I created a dummy email (emailbot@wrightesd.org) so that I didn't have a real user's password sitting around in plain text. And if you do this remember to log into the dummy account at least once to make sure you can actually send emails from it.

Next you have to create a Service Account in the Google Developer Console. This creates an email address (this is important because you'll need to share you Sheet with this Service Account email address later) and generates a key pair that you'll download as a json file into your working directory.

[Here](https://developers.google.com/sheets/quickstart/python) and [here](https://developers.google.com/identity/protocols/OAuth2ServiceAccount) are the official Google references, but I'll walk you through it here also.

Next, install `pip`. If you're not familiar with Python, `pip` is Python's package installer. You'll need a couple of non-default python packages to work with the Google Sheets API.

`sudo apt-get install httplib2 google-api-python-client`

Finally, clone

`sudo apt-get install pip`

`sudo apt-get install lib`
