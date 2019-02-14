import configparser
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


config = configparser.ConfigParser()
config.read('olx_beholder.ini')
username = config['Smtp']['username']
passwd = config['Smtp']['passwd']
smtp_host = config['Smtp']['smtp_host']
port = config['Smtp']['port']
use_tls = config['Smtp']['use_tls']

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


def send_email_two_part(receiver, sender, subject, body_text, body_html, bcc=''):
    print('sender: {sender}, receiver: {receiver}'.
          format(sender=sender, receiver=receiver))

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver

    part1 = MIMEText(body_text, 'plain')
    part2 = MIMEText(body_html, 'html')

    msg.attach(part1)
    msg.attach(part2)

    try:
        smtp = smtplib.SMTP(smtp_host, port)
        smtp.ehlo()
        if (use_tls == 'yes'):
            smtp.starttls()
            smtp.ehlo
        smtp.login(username, passwd)
        smtp.sendmail(sender, [receiver] + [bcc], msg.as_string())
        print('Successfully sent email to {receiver}'
              .format(receiver=receiver))
    except smtplib.SMTPException as e:
        print('Error sending email!', e)
