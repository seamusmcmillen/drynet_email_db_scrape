# drynet_email_db_scrape
This is a repository for the scraping of emails for delivery notes.

We will use celery to monitor the inbox

We will extract customer information from the email and the attached PDF

After extracting the information, we check the info against the db.

If the data is not yet imported we will import the data.

Should the data not get imported, we will create an exception report and send to support@drynet.de
