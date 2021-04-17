import imaplib
import email
from email.header import decode_header
import webbrowser
import os
import re
import pandas as pd 

# account credentials
#username = "singhpreet.19992@gmail.com"
#password = "Python_098"
username = "*******@gmail.com"
password = "*********"
imap_url = "imap.gmail.com"


def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

# Function to get email content part i.e its body part
def get_body(msg):
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None, True)
  
# Function to search for a key value pair 
def search(key, value, imap): 
    result, data = imap.search(None, key, '"{}"'.format(value))
    #print("Inside search method")
    return data
  
# Function to get the list of emails under this label
def get_emails(result_bytes):
    msgs = [] # all the email data are pushed inside an array
    #print("Inside get_emails method")
    for num in result_bytes[0].split():
        typ, data = imap.fetch(num, '(RFC822)')
        msgs.append(data)
  
    return msgs

def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)

mail_list = []
from_address_list = []
from_address_list.append('netplus@mynetplus.co.in')
from_address_list.append('no-reply@travel.e-redbus.in')
from_address_list.append('alerts@updates.swiggy.in')
from_address_list.append('noreply@mailers.zomato.com')
from_address_list.append('mail@info.paytm.com')
from_address_list.append('no-reply@amazon.com')
from_address_list.append('noreply@olamoney.com')
from_address_list.append('no-reply@zoomcar.com')

for from_address in from_address_list:
    
    # this is done to make SSL connnection with GMAIL
    imap = imaplib.IMAP4_SSL(imap_url) 
      
    # logging the user in
    imap.login(username, password) 
      
    # calling function to check for email under this label
    status, messages = imap.select('Inbox')
    
    print("="*180)
    print(str(from_address)+" - starts")
    messages = get_emails(search('FROM', from_address, imap))
    
    if 'netplus' in from_address:
        category = 'Telecom'
    elif 'redbus' in from_address or 'zoomcar' in from_address:
        category = 'Travel'
    elif 'swiggy' in from_address or 'zomato' in from_address:
        category = 'Food'
    elif 'paytm' in from_address or 'amazon' in from_address or 'olamoney' in from_address:
        category = 'Financial'
    
    # number of top emails to fetch
    N = 1
    
    # total number of emails
    print('Total mails from '+str(from_address)+': '+str(len(messages)))
    
    for msg in messages:
        try:
            for response in msg:
                if isinstance(response, tuple):
                    # parse a bytes email into a message object
                    msg = email.message_from_bytes(response[1])
                    # decode the email subject
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        # if it's a bytes, decode to str
                        subject = subject.decode(encoding)
                    # decode email sender
                    From, encoding = decode_header(msg.get("From"))[0]
                    if isinstance(From, bytes):
                        From = From.decode(encoding)
                    #print("Subject:", subject.encode("utf-8"))
                    #print("From:", From.encode("utf-8"))
                    
                    maintype = msg.get_content_maintype()
                    if maintype == 'multipart':
                        for part in msg.get_payload():
                            if part.get_content_maintype() == 'text':
                                body = part.get_payload(decode=True).decode(errors='ignore')
                                body = cleanhtml(body)
                                #print("Body:", body.encode("utf-8"))
                                break
                    elif maintype == 'text':
                        body = msg.get_payload(decode=True).decode(errors='ignore')
                        body = cleanhtml(body)
                        #print("Body:", body.encode("utf-8"))
        
                       
                    #print("="*180)
            mail_list.append([From, subject, body, category])
        except Exception as e: 
            print("Exception in mail parsing: "+str(e))
            pass
    
    # close the connection and logout
    imap.close()
    imap.logout()      
     
    print(str(from_address)+" - ends")

# Create dataframe
df = pd.DataFrame(mail_list, columns =['from', 'subject', 'body', 'category'])
#print(df)
df.to_csv('C:\\Users\\preet\\workspace-neon\\Email-Classification-Supervised\\mail_list.csv')
      

  


