#! /usr/bin/env python3

import imapclient # connecting to the drynet mail server
import os # navigating directories
import email # parsing the email
import logging #
import fitz
import os
import re
import fnmatch
import datetime

## authentication # create a function here
imap_host = 'imap.ionos.de'
# credentials in seperate module
imap_user = 'support@drynet.de'
# authentication - commit after testing
imap_pass = '$uPPort2018'
# attachments folder
attachments_folder = "C:/Users/SeamusMcMillen/OneDrive/Android/development/data_scrape/ScrapingEmails/attachments"

'''# This should happen as part of the PDF module (and not delelete but archive)
for file in os.listdir(attachments_folder):
    os.remove(os.path.join(attachments_folder, file))
#####'''

# Connect to server
server = imapclient.IMAPClient(imap_host, ssl=True)
server.login(imap_user, imap_pass)
server.select_folder('Inbox', readonly=True)

# Server idle for monitoring in box

def get_email():
    # Connect to server
    server = imapclient.IMAPClient(imap_host, ssl=True)
    server.login(imap_user, imap_pass)
    server.select_folder('Inbox', readonly=False)
    ## Identifying new delivery notes
    correct_to = server.search(['TO', 'deliveries@drynet.de']) # only emails to deliveries
    correct_from = server.search(['FROM', 'seamus.mcmillen@drynet.net']) # only emails from holger.ritter
    # print(set.intersection(set(correct_to), set(correct_from))) # visaul validation of emails with two criteria
    correct_to_from = set.intersection(set(correct_to), set(correct_from)) # intersection of from and to addresses

    # create functions here (fetching, reading, finding attachments, writing pdfs)
    for uid, msg_data in server.fetch(correct_to_from, 'RFC822').items():
        email_message = email.message_from_bytes(msg_data[b'RFC822'])
        if email_message.get_content_maintype() == 'multipart':
            for part in email_message.walk():
                attachment_filename = part.get_filename()
                if attachment_filename is not None:
                    print("File name: ", part.get_filename())      # visual confirmation
                    attachment_path = f'{attachments_folder}/{attachment_filename}'
                    with open(attachment_path, 'wb') as fp:
                        fp.write(part.get_payload(decode=True))
                        fp.close()
                    pdf_extract()
            server.move(uid, 'Delivery_Archive')

# pdf extract from attachments
def pdf_extract():
    pdf_dir = 'C:/Users/SeamusMcMillen/OneDrive/Android/development/data_scrape/ScrapingEmails/attachments/'
    import_folder = 'C:/Users/SeamusMcMillen/OneDrive/Android/development/data_scrape/ScrapingEmails/import_data/'
    # filename = '3500211_DRYNET_Delivery_Note_WMO_Zephyr.pdf'
    filename_pattern = '*DRYNET_Delivery_Note*'
    current_date_and_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    cdt_string = str(current_date_and_time)
    extension = '.csv'

    for filename in os.listdir(pdf_dir):
        if fnmatch.fnmatch(filename, filename_pattern):
            print(filename)

            full_filename = os.path.join(pdf_dir, filename)

            doc = fitz.open(full_filename)
            for page in doc:
                text = page.get_text("text")
                company = re.findall('DRYNET-ID: ([a-zA-Z]+)', text)
                vessel = re.findall('vessel ([\'\sa-zA-Z]+)', text) # will be gotten from AIS not from PDF
                imo = re.findall('IMO ([0-9]+)', text)
                serial_no = re.findall('S/N ([a-zA-Z0-9\-]+)', text)
                iccid = re.findall('ICCID: ([0-9]+)', text)
                bundle = re.findall('Airtime ([a-zA-Z0-9]+)', text)
                monthly_volume = re.findall('Monthly Data Volume incuded: ([a-zA-Z0-9]+)', text)
                # monthly_volume = re.findall('Monthly Data Volume included: ([a-zA-Z0-9]+)', text)
                import_list = company + vessel + imo + serial_no + iccid + bundle + monthly_volume
                import_string = str(import_list).strip('[]').replace(" ", "")
                data_filename = str(company).strip('[]').strip("''") + cdt_string + extension
                import_path = f'{import_folder}/{data_filename}'
                with open(import_path, 'wt') as il:
                    il.write(import_string)
                    il.close()
                # we should also attach the pdf to the record in db
            continue
        else:
            continue

# database update or error report (email support with info)

## Enter an idle mode to monitor inbox
# Start IDLE mode
server.idle()
print("Connection is now in IDLE mode, send yourself an email or quit with ^c")

while True:
    try:
        # Wait for up to 30 seconds for an IDLE response
        responses = server.idle_check(timeout=30)
        if responses:
            get_email()
        else:
            print('No new emails')
    except KeyboardInterrupt:
        server.idle_done()
        break

server.logout()
