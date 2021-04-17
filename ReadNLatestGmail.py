import imaplib
import email
from email.header import decode_header
import webbrowser
import os
import re
import pandas as pd 

# account credentials

username = "*******@gmail.com"
password = "*******"
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
def search(imap):
    print("Inside search method")
    result, data = imap.search(None, '(SINCE "01-Apr-2021")')
    print("Search complete")
    return data
  
# Function to get the list of emails under this label
def get_emails(result_bytes):
    print("Inside get_emails method")
    msgs = [] # all the email data are pushed inside an array
    #print("Inside get_emails method")
    for num in result_bytes[0].split():
        print(num)
        typ, data = imap.fetch(num, '(RFC822)')
        msgs.append(data)
    print("Returning from get_emails method")
    return msgs

def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)

mail_list = []

    
# this is done to make SSL connnection with GMAIL
imap = imaplib.IMAP4_SSL(imap_url) 
  
# logging the user in
imap.login(username, password) 
  
# calling function to check for email under this label
status, messages = imap.select('Inbox')

print("="*180)
messages = get_emails(search(imap))


# total number of emails
print('Total mails fetched =  '+str(len(messages)))

index = 1
for msg in messages:
  print("*** Parsing message number = "+str(index))
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
      subject = subject.replace('|','')
      body = body.replace('|','')
      mail_list.append([index, From, subject, body, 'category'])
  except Exception as e: 
      print("Exception in mail parsing: "+str(e))
      pass
  index = index + 1
    

# close the connection and logout
imap.close()
imap.logout()      
 
print("Email Parsing Ends")

# Create dataframe
df = pd.DataFrame(mail_list, columns =['id', 'sender', 'subject', 'body', 'category'])
#print(df)
df.to_csv('mail_list_since_given_date.csv', sep='|', index=False)
      

  


