#! /usr/bin/env python3

import fitz
import os
import re
import fnmatch

sn_pattern = 'S/N ([a-zA-Z0-9\-]+)'
co_pattern = 'DRYNET-ID: '
vessel_patters = 'vessel '
imo_pattern = 'IMO: '
sim_pattern = 'ICCID: '
bundle_pattern = 'Airtime '
data_volume_pattern = 'Monthly Data Volume included: '
pdf_dir = 'C:/Users/SeamusMcMillen/OneDrive/Android/development/data_scrape/ScrapingEmails/attachments/'
# filename = '3500211_DRYNET_Delivery_Note_WMO_Zephyr.pdf'
filename_pattern = '*DRYNET_Delivery_Note*'

for filename in os.listdir(pdf_dir):
    if fnmatch.fnmatch(filename, filename_pattern):
        print(filename)
        filename = filename

        full_filename = os.path.join(pdf_dir, filename)

        doc = fitz.open(full_filename)
        for page in doc:
            text = page.get_text("text")
            company = re.findall('DRYNET-ID: ([a-zA-Z]+)', text)
            vessel = re.findall('vessel ([\'\sa-zA-Z]+)', text)
            imo = re.findall('IMO ([0-9]+)', text)
            serial_no = re.findall('S/N ([a-zA-Z0-9\-]+)', text)
            iccid = re.findall('ICCID: ([0-9]+)', text)
            print(company, vessel, imo, serial_no, iccid)
