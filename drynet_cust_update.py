#! /usr/bin/env python3

import imaplib # connecting to the drynet mail server
import os # navigating directories
import email # parsing the email
import PyPDF2 # parsing the PDF
import celery # scheduling reads of the inbox
import pprint

## email module
imap_host = 'imap.ionos.de'
 # credentials in seperate module
imap_user = 'support@drynet.de'
 # authentication - commit after testing
imap_pass = '$uPPort2018'
imap = imaplib.IMAP4_SSL(imap_host)
imap.login(imap_user, imap_pass)

imap.select('Inbox')
# email search & retrieval (from *@drynet.net, has attachment, content "delivery note")
tmp, data = imap.search(None, 'ALL')
# email IDs -> all email IDs from deliveries@drynet.de -> email attachment -> body contains "delivery note"
for num in data[0].split():
    tmp, data = imap.fetch(num, '(RFC822)')
    pprint.pprint(data[0][1])

## pdf module
# pdf parsing



## database module
# database comparison for parsed database



# database update or error report (email support with info)
