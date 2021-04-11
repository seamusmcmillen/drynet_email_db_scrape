#! /usr/bin/env python3

import imapclient # connecting to the drynet mail server
import os # navigating directories
import email # parsing the email
from email.header import decode_header
import PyPDF2 # parsing the PDF
import celery # scheduling reads of the inbox
import pprint

## authentication # create a function here
imap_host = 'imap.ionos.de'
 # credentials in seperate module
imap_user = 'support@drynet.de'
 # authentication - commit after testing
imap_pass = '$uPPort2018'
imap = imapclient.IMAPClient(imap_host, ssl=True)
imap.login(imap_user, imap_pass)

## Searching for delivery notes
imap.select_folder('Inbox', readonly=True)
# email search & retrieval (from *@drynet.net, has attachment, content "delivery note")
to_deliveries = imap.search(['TO', 'deliveries@drynet.de'])
 # Visual check to see it working

# email IDs -> all email IDs from deliveries@drynet.de -> email attachment -> body contains "delivery note"
# create a function here
for uid, msg_data in imap.fetch(to_deliveries, 'RFC822').items():
    email_message = email.message_from_bytes(msg_data[b'RFC822'])
    print(uid, email_message.get('From')) # visual confirmation
    



## pdf module
# pdf parsing



## database module
# database comparison for parsed database



# database update or error report (email support with info)
