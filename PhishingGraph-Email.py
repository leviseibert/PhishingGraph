#https://thepythoncode.com/article/reading-emails-in-python

import imaplib
import email
from email.header import decode_header
import webbrowser
import os
from openai import OpenAI

# account credentials
username = "Email Address"
password = "Email Password"
imap_server = "Email Server"
client = OpenAI(
  api_key='Your API Key' 
)

email_text = ""
    
# create an IMAP4 class with SSL 
imap = imaplib.IMAP4_SSL(imap_server)
# authenticate
imap.login(username, password)

status, email_messages = imap.select("INBOX")

number_of_emails = int(input("How many messages do you want to analyze? "))
while (number_of_emails <= 0 and number_of_emails > 5):
    number_of_emails = int(input("Invalid number!  Please try again: "))

# number of top emails to fetch
N = number_of_emails
# total number of emails
total_messages = int(email_messages[0])

for i in range(total_messages, total_messages-N, -1):
    # fetch the email message by ID
    res, msg = imap.fetch(str(i), "(RFC822)")
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
            print("Subject:", subject)
            print("From:", From)
            # if the email message is multipart
            if msg.is_multipart():
                # iterate over email parts
                for part in msg.walk():
                    # extract content type of email
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    try:
                        # get the email body
                        body = part.get_payload(decode=True).decode()
                    except:
                        pass
                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        # print text/plain emails and skip attachments
                        print(body)
                        email_text = body
            else:
                # extract content type of email
                content_type = msg.get_content_type()
                # get the email body
                body = msg.get_payload(decode=True).decode()
                if content_type == "text/plain":
                    email_text += body
# close the connection and logout
imap.close()
imap.logout()

messages = [ {"role": "system", "content":  
              """You are PhishingGraph: PhishingGraph-Email analyzes an email message and determines the likelihood of the message being a phish 
as a percentage, followed by a succinct message tailored to the assessed risk level. 
The response is clear and straightforward, designed to quickly inform the user of the potential threat: 
- Under 20%: "Unlikely to be phishing." 
- 20% to 60%: "Could be phishing." 
- 60% to 70%: "Shows signs of phishing." 
- 70% to 80%: "Highly likely to be phishing." 
- 80% to 90%: "Very high confidence of phishing." 
- Over 90%: "Almost certainly phishing." 
Directly following this message, users are presented with a multiple-choice menu, 
inviting them to: A) See detailed reasons for the analysis, B) Get tips on avoiding phishing, 
or C) Take a quiz question related to phishing. This combination of a simple initial 
assessment with optional in-depth exploration respects the user's time and interest level, 
offering a tailored experience based on their immediate needs and curiosity.  Specific
focus is given on identifying the following: authority, likability, reciprocation, consistency, social validation, and scarcity, as well as 
identifying and indicating areas where humans may be inaccurate."""} ] 
              
#message = """ """
#messages.append( {"role": "user", "content": message}, ) 
#chat = client.chat.completions.create( model="gpt-3.5-turbo", messages=messages )    
          
message = email_text

messages.append( {"role": "user", "content": message}, ) 
chat = client.chat.completions.create( model="gpt-3.5-turbo", messages=messages ) 
reply = chat.choices[0].message.content 
print(f"ChatGPT: {reply}") 
messages.append({"role": "assistant", "content": reply})
while True: 
    message = input("User : ") 
    if message: 
        messages.append( {"role": "user", "content": message}, ) 
        chat = client.chat.completions.create( model="gpt-3.5-turbo", messages=messages ) 
    reply = chat.choices[0].message.content 
    print(f"ChatGPT: {reply}") 
    messages.append({"role": "assistant", "content": reply})