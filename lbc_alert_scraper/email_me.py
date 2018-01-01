#!/usr/local/bin/python
# coding: utf-8
import os
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from chameleon import PageTemplateFile


def send_email(logger, config, offers):

    fromaddr = config['EMAIL_SENDER']
    password = config['EMAIL_SENDER_PSWD']
    toaddr = config['EMAIL_RECEIVER']
    mail_server = config['SERVER_EMAIL_SENDER']
    mail_server_port = config['SERVER_EMAIL_PORT']

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = '%s Nouvelle(s) annonce(s) détectée(s)' % len(offers)

    here = os.path.abspath(os.path.dirname(__file__))
    template = PageTemplateFile(os.path.join(here, 'templates/mail.pt'))
    body = template(offers=offers)

    msg.attach(MIMEText(body, 'html'))

    try:
        server = smtplib.SMTP(mail_server, mail_server_port)
        server.ehlo()
        if password:
            server.starttls()
            server.ehlo()
            server.login(fromaddr, password)
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        logger.info('email send to %s', toaddr)
    except smtplib.socket.error:
        logger.eroor('mail socket error')
    except smtplib.SMTPException:
        logger.error('mail smtp exception')