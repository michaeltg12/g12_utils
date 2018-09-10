import os
import json
from config import *

def slack_send_direct(message):
    from slackclient import SlackClient

    slack_token = SLACK_ARM_TOKEN
    sc = SlackClient(slack_token)

    api_call = sc.api_call("im.list")

    if api_call.get('ok'):
        for im in api_call.get('ims'):
            if im.get('user') == SLACK_USER_ID and im.get("is_im") == True:
                im_channel = im.get("id")
                sc.api_call("chat.postMessage",
                            channel=im_channel,
                            text=message,
                            user=SLACK_USER_ID)

def send_email(subject:str, message:str, recipients:list):
    try:
        import smtplib
        from email.mime.text import MIMEText
        executable = os.path.basename(__file__)
        host = os.uname().__getattribute__('nodename')
        sender = '{}@{}'.format(executable, host)

        stars = 100*"*"
        msg = "Sent from {0}. Variable extraction.\n\n" \
              "{2}\n\t{1}\n{2}".format(host, message, stars)
        msg = MIMEText(msg)

        msg['Subject'] = "*** {} ***".format(subject)
        msg['From'] = sender
        msg['To'] = ", ".join(recipients)
        s = smtplib.SMTP('localhost')
        s.sendmail(sender, recipients, msg.as_string())
    except Exception:
        print("Email not sent to {}".format(", ".join(recipients)))

def main():
    print('** Test some stuff\nSend a slack message to Michael')
    slack_send_direct("test message from python")


if __name__ == "__main__":
    main()