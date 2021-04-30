#! /usr/bin/env python3

import fitz
import os
import re
import fnmatch
import datetime

### Patterns to be matched (written below because strings no worky)
# sn_pattern = 'S/N ([a-zA-Z0-9\-]+)'
# co_pattern = 'DRYNET-ID: '
# vessel_patters = 'vessel '
# imo_pattern = 'IMO: '
# sim_pattern = 'ICCID: '
# bundle_pattern = 'Airtime '
# data_volume_pattern = 'Monthly Data Volume included: '
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
                vessel = re.findall('vessel ([\'\sa-zA-Z]+)', text)
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

pdf_extract()
