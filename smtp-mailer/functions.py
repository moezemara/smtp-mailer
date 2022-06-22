import email, smtplib, ssl
from pathlib import Path
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
import commands

def sendemail(receiver, textbody, htmlbody):
    config = loadconfig()

    subject = config['subject']
    
    sender_email = config['username']
    receiver_email = receiver
    password = config['password']
    message = MIMEMultipart()
    message["From"] = config['from']
    message["To"] = receiver
    message["Subject"] = config['subject']

    if config['text'] == 1:
        body = textbody[0]
        if textbody[1]:
            for path in textbody[1]:
                part = MIMEBase('application', "octet-stream")
                with open(f'./files/{path}', 'rb') as file:
                    part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition',
                                'attachment; filename={}'.format(Path(path).name))
                message.attach(part)
        message.attach(MIMEText(body, 'plain'))

    if config['html'] == 1:
        body = htmlbody[0]
        if htmlbody[1]:
            for path in htmlbody[1]:
                part = MIMEBase('application', "octet-stream")
                with open(f'./files/{path}', 'rb') as file:
                    part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition',
                                'attachment; filename={}'.format(Path(path).name))
                message.attach(part)
        message.attach(MIMEText(body, 'html'))

    text = message.as_string()
    
    try:
        if (config['port'] == '465'):
            server = smtplib.SMTP_SSL(config['smtp'], config['port'])
        else:
            server = smtplib.SMTP(config['smtp'], config['port'])
            
        if (config['secure'] == 1):
            context = ssl.create_default_context()
            server.starttls(context=context)

        server.ehlo() # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
        return 'success'
    except Exception as e:
        return e


def loadconfig():
    config = eval(open('config.txt', 'r').read())
    return config

def saveconfig(config):
    open('config.txt','w').write(config)

def loadlist():
    emaillist = open('list.txt', 'r').read().split('\n')
    newlist = [email for email in emaillist if email != '']
    open('list.txt','w').write('\n'.join(newlist))
    return newlist

def loadmessage():
    return open('message.txt', 'r').read()

def loadhtmlmessage():
    return open('message.html', 'r').read()

def appenedemail(email):
    open('list.txt','a').write('\n'+email)

def clear():
    open('list.txt','w').close()

def loadfiletoloadlist(filename):
    emaillist = open(filename, 'r').read().split('\n')
    emaillist = [email for email in emaillist if email != '']
    open('list.txt','a').write('\n')
    emaillist_append = open('list.txt','a').write('\n'.join(emaillist))

def delete_loadlist(email_to_delete):
    emaillist = loadlist()

    emaillist_w = open('./list.txt','w')
    newlist = []
    for email in emaillist:
        if email != email_to_delete and email != '\n':
            newlist.append(email)
    emaillist_w.write('\n'.join(newlist))
    return loadlist()

def load_deafult_message():
    return open('message.txt','r').read()

def load_message(filename):
    return open(filename,'r').read()

def save_message(message):
    open('message.txt','w').write(message)

def load_deafult_html_message():
    return open('message.html','r').read()

def load_html_message(filename):
    return open(filename,'r').read()

def save_html_message(message):
    open('message.html','w').write(message)

def translate(email, message, htmlmessage):
    body = commands.translator(message, email)
    htmlbody = commands.translator(htmlmessage, email)
    return sendemail(email, body, htmlbody)