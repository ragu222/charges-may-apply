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

Make sure to replace the default values with your real values. And DON'T TOUCH the sent_flag or flag value. You've been warned.

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

`sudo apt-get install pip`

`sudo apt-get install lib`
