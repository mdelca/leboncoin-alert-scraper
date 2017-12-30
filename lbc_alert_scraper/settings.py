#!/usr/local/bin/python
# coding: utf-8

# Here add you server config and mail parameter
EMAIL_SENDER = "<email-of-the-sender>"
EMAIL_SENDER_PSWD = "" # password of the mail server, leave empty if no authentication
EMAIL_RECEIVER = "<email-of-the-receiver>"
SERVER_EMAIL_SENDER = "<mail-server-adress>" # For me host at OVH it's : ssl0.ovh.net, for Gmail : smtp.gmail.com
SERVER_EMAIL_PORT = "587"


# Add the name of your alert and the url of the search corresponding
URLS = {
'My-alert-name' : 'https://www.leboncoin.fr/urlofmysearchonleboncoin',
'My-super-alert-name' : 'https://www.leboncoin.fr/mysupersearch',
'save-my-life-alert' : 'https://www.leboncoin.fr/savemylifesearch'
}
