#! /usr/bin/env python3

import imaplib # connecting to the drynet mail server
import os # navigating directories
import email # parsing the email
import PyPDF2 # parsing the PDF
import celery # scheduling reads of the inbox
