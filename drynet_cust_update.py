#! /usr/bin/env python3

import imapclient # connecting to the drynet mail server
import os # navigating directories
import email # parsing the email
import PyPDF2 # parsing the PDF
import pprint

## authentication # create a function here
imap_host = 'imap.ionos.de'
 # credentials in seperate module
imap_user = 'support@drynet.de'
# authentication - commit after testing
imap_pass = '$uPPort2018'
server = imapclient.IMAPClient(imap_host, ssl=True)
server.login(imap_user, imap_pass)

## Enter an idle mode to monitor inbox
# Start IDLE mode
''' server.idle()
print("Connection is now in IDLE mode, send yourself an email or quit with ^c")

while True:
    try:
        # Wait for up to 30 seconds for an IDLE response
        responses = server.idle_check(timeout=30)
        print("Server sent:", responses if responses else "nothing")
    except KeyboardInterrupt:
        break
'''
## Searching for delivery notes
server.select_folder('Inbox', readonly=True)
# email search & retrieval (from *holger.ritter@drynet.net', to 'deliveries@drynet.de' has attachment, content "delivery note")
correct_to = server.search(['TO', 'deliveries@drynet.de'])
correct_from = server.search(['FROM', 'holger.ritter@drynet.net'])
print(correct_to)
print(correct_from)
print(set.intersection(set(correct_to), set(correct_from)))
correct_to_from = set.intersection(set(correct_to), set(correct_from))
# correct_to_from = correct_to, correct_from
# Visual check to see it working

# email IDs -> all email IDs from deliveries@drynet.de -> email attachment -> body contains "delivery note"
# create a function here
for uid, msg_data in server.fetch(correct_to_from, 'RFC822').items():
    email_message = email.message_from_bytes(msg_data[b'RFC822'])
    if email_message.get_content_maintype() == 'multipart':
        for part in email_message.walk():
            print(uid, part.get_filename())      # visual confirmation
            attachments = part.get_filename()




## pdf module
# pdf parsing



## database module
# database comparison for parsed database



# database update or error report (email support with info)

# logout of email server
server.logout()
