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
      "from":"your_email@your_domain.org"
      "to"  :"7075551234@txt.att.net"
      "user":"your_email@your_domain.org"
      "pass":"password"
  }
  "sent_flag":{
      "flag":0
  }
}
```

`sudo apt-get install pip`
`sudo apt-get install lib`
