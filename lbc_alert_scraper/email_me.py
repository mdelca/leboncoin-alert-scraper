#!/usr/local/bin/python
# coding: utf-8
import os
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from chameleon import PageTemplateFile



def send_email(logger, config, recipients, offers):

    fromaddr = config['EMAIL_SENDER']
    password = config['EMAIL_SENDER_PSWD']
    toaddr = ','.join(recipients)
    mail_server = config['SERVER_EMAIL_SENDER']
    mail_server_port = config['SERVER_EMAIL_PORT']

    total_offers = 0
    for o_ in offers.values():
        total_offers += len(o_)

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = '%s Nouvelle(s) annonce(s) détectée(s)' % total_offers

    here = os.path.abspath(os.path.dirname(__file__))
    template = PageTemplateFile(os.path.join(here, 'templates/mail.pt'))
    body = template(offers=offers)

    msg.attach(MIMEText(body, 'html'))

    server = smtplib.SMTP(mail_server, mail_server_port)
    server.ehlo()
    if password:
        server.starttls()
        server.ehlo()
        server.login(fromaddr, password)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    logger.info('email send to %s', toaddr)
