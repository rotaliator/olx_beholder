import configparser
import smtplib

config = configparser.ConfigParser()
config.read('send_email.ini')
username = config['DEFAULT']['username']
passwd = config['DEFAULT']['passwd']
smtp_host = config['DEFAULT']['smtp_host']
port = config['DEFAULT']['port']
use_tls = config['DEFAULT']['use_tls']

def send_email(receiver, sender, subject, body, bcc=''):
    print('sender: {sender}, receiver: {receiver}'.
          format(sender=sender, receiver=receiver))
    message = (
        "From: %s\nTo: %s\nBCC: %s\nSubject: %s\n\n %s"
        % (sender, receiver, bcc, subject, body))
    try:
        smtp = smtplib.SMTP(smtp_host, port)
        smtp.ehlo()
        if (use_tls == 'yes'):
            smtp.starttls()
            smtp.ehlo
        smtp.login(username, passwd)
        smtp.sendmail(sender, [receiver] + [bcc], message.encode())
        print('Successfully sent email to {receiver}'
              .format(receiver=receiver))
    except smtplib.SMTPException as e:
        print('Error sending email!', e)
