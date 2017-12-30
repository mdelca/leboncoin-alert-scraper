#!/usr/local/bin/python
# coding: utf-8


def send_email(config, subject, body):
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    fromaddr = config['EMAIL_SENDER']
    password = config['EMAIL_SENDER_PSWD']
    toaddr = config['EMAIL_RECEIVER']
    mail_server = config['SERVER_EMAIL_SENDER']
    mail_server_port = config['SERVER_EMAIL_PORT']
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    import smtplib
    try:
        server = smtplib.SMTP(mail_server, mail_server_port)
        server.ehlo()
        if password:
            server.starttls()
            server.ehlo()
            server.login(fromaddr, password)
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
    except smtplib.socket.error:
        print('mail socket error')
    except smtplib.SMTPException:
        print('mail smtp exception')
