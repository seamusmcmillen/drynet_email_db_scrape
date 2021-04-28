#! /usr/bin/env python3
import requests, json
from datetime import datetime, timedelta
import urllib3
import humanize

urllib3.disable_warnings()
# function to get either IMO or MMSI
search_criteria = "imo=9728942"

# open api to pull vessel record
url = "https://ais.spire.com/vessels?" + search_criteria
access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjdXN0b21lciI6eyJpZCI6IjkyNyIsIm5hbWUiOiJEcnluZXQiLCJ1dWlkIjoiOTI3In0sImlzcyI6InNwaXJlLmNvbSIsImlhdCI6MTYxODU4NDY5MX0.hmzQiLqZEgWm2niQN6FbDxIvHpF4xdReG9hxNAQNCvc"
headers = {"Authorization": 'Bearer ' +access_token }
response = requests.get(url, headers=headers, verify=False)
print(response)

# pull data from Spire
data = response.json()
vessel_info = data['data'][0]

# Data to import
name = vessel_info['name']
imo = vessel_info['imo']
lon = vessel_info['last_known_position']['geometry']['coordinates'][0] # might be 1 for lat
lat = vessel_info['last_known_position']['geometry']['coordinates'][1] # might be 0 for lon
geom = "POINT(%s %s)"% (str(lon).strip(), str(lat).strip())
destination = vessel_info['most_recent_voyage']['destination']
eta_raw = vessel_info['most_recent_voyage']['eta']
eta = eta_raw[:10]
date_position = vessel_info['last_known_position']['timestamp'] # ID how to make this what the db expects
course = vessel_info['last_known_position']['heading']
speed = vessel_info['last_known_position']['speed']
now = datetime.now()
# now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
last_update_string = date_position[:19].replace('T', ' ')
last_update = datetime.strptime(last_update_string, "%Y-%m-%d %H:%M:%S")
delta_date_last_now = now - last_update
delta_humanize = humanize.naturaltime(datetime.now() - last_update)
# How to format this as 1 hour 36 minutes ago

# data to export
print("Name:", name,
    "IMO:", imo,
    "Geom:", geom,
    "Lat:", lat,
    "Long:", lon,
    "Dest.:", destination,
    "ETA:", eta,
    "Last Seen:", delta_humanize,
    "Updated:", last_update,
    "Time now:", now.strftime("%Y-%m-%d %H:%M:%S"),
    "Course:", course,
    "Speed:", speed
    )
'''
VesselLocation.objects.create(
                        name=name,
                        imo=imo,
                        lon=lon,
                        lat=lat,
                        geom=geom,
                        speed=speed,
                        course=course,
                        destination=destination,
                        eta=eta,
                        date_position=date_position
                        )
'''
