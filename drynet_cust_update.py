#! /usr/bin/env python3

import imaplib # connecting to the drynet mail server
import os # navigating directories
import email # parsing the email
from email.header import decode_header
import PyPDF2 # parsing the PDF
import celery # scheduling reads of the inbox
import pprint

## authentication
imap_host = 'imap.ionos.de'
 # credentials in seperate module
imap_user = 'support@drynet.de'
 # authentication - commit after testing
imap_pass = '$uPPort2018'
imap = imaplib.IMAP4_SSL(imap_host)
imap.login(imap_user, imap_pass)

## Searching for delivery notes
imap.select('Inbox')
# email search & retrieval (from *@drynet.net, has attachment, content "delivery note")
res, msg_num = imap.search(None, '(TO "deliveries@drynet.de")')
print(res, msg_num)

# email IDs -> all email IDs from deliveries@drynet.de -> email attachment -> body contains "delivery note"
for num in msg_num[0].split():
    status, msg = imap.fetch(num, '(RFC822)')
    for response in msg:
        if isinstance(response, tuple):
            msg = email.message_from_bytes(response[1])
            if msg.is_multipart():
                print('Has an attachment')

## pdf module
# pdf parsing



## database module
# database comparison for parsed database



# database update or error report (email support with info)
