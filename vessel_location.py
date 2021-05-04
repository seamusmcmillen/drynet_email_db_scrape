import requests, json
import urllib3
import humanize
from datetime import datetime
import csv
import os

fleet = "C:\\Users\\SeamusMcMillen\\OneDrive\\Android\\development\\data_scrape\\imo_list.txt"
ais_info = 'vesseldetails.csv'
imo_list_raw = []
imo_list = []
vessel_details_list = []

if ais_info in os.listdir('C:\\Users\\SeamusMcMillen\\OneDrive\\Android\\development\\data_scrape'):
    os.remove('C:\\Users\\SeamusMcMillen\\OneDrive\\Android\\development\\data_scrape\\vesseldetails.csv')

def list_of_imos():
    with open(fleet, 'r') as f:
        each_line = f.readlines()
        for each_imo in each_line:
            each_imo = each_imo.strip()
            imo_list_raw.append(each_imo)
        imo_list = list(filter(None, imo_list_raw))
        return imo_list


def query_api(imo_list):
    urllib3.disable_warnings()
    # function to get either IMO or MMSI
    print(imo_list)
    for each_imo in imo_list:
        try:
            search_criteria = "imo=" + each_imo
            print(search_criteria)

            # open api to pull vessel record
            url = "https://ais.spire.com/vessels?" + search_criteria
            access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjdXN0b21lciI6eyJpZCI6IjkyNyIsIm5hbWUiOiJEcnluZXQiLCJ1dWlkIjoiOTI3In0sImlzcyI6InNwaXJlLmNvbSIsImlhdCI6MTYxODU4NDY5MX0.hmzQiLqZEgWm2niQN6FbDxIvHpF4xdReG9hxNAQNCvc"
            headers = {"Authorization": 'Bearer ' +access_token }
            response = requests.get(url, headers=headers, verify=False)
            print(response)

            # pull data from Spire
            data = response.json()
            vessel_info = data['data'][0]

            # Data needed from json for export
            try:
                name = vessel_info['name'] # identifier
                imo = vessel_info['imo'] # identifier

                lat = vessel_info['last_known_position']['geometry']['coordinates'][0] # Location
                lon = vessel_info['last_known_position']['geometry']['coordinates'][1] # Location
                geom = "POINT(%s %s)"% (str(lon).strip(), str(lat).strip()) # Location
                destination = vessel_info['most_recent_voyage']['destination'] # Location

                eta_raw = vessel_info['most_recent_voyage']['eta'] # Arrivale time
                eta = eta_raw[:19].replace('T', ' ') + ' UTC' # Arrivale time

                course = vessel_info['last_known_position']['heading'] # AIS info course
                speed = vessel_info['last_known_position']['speed'] # AIS info SOG
                date_position = vessel_info['last_known_position']['timestamp'] # AIS info time

                now = datetime.now() # current time
                last_update_string = date_position[:19].replace('T', ' ') # format date_position for time object
                last_update = datetime.strptime(last_update_string, "%Y-%m-%d %H:%M:%S") # date_position made a time object

                delta_humanize = humanize.naturaltime(datetime.now() - last_update) # make last_update normal language
            except (TypeError, AttributeError):
                print('Missing element in AIS data')

            # data to export
            # print(type(name), type(imo), type(geom), type(lat), type(lon), type(destination), type(eta), type(date_position), type(course), type(speed))

            # print(vessel_details_list)
            # export data
            with open('C:\\Users\\SeamusMcMillen\\OneDrive\\Android\\development\\data_scrape\\vesseldetails.csv', 'a', newline = '', encoding='utf-8') as csv_file:
                    write = csv.writer(csv_file, quoting=csv.QUOTE_ALL, lineterminator='\n')
                    csv_file.write(name + ',' + str(imo) + ',' + str(lat) + ',' + str(lon) + ',' + str(speed) + ',' + str(course) + ',' + destination + ',' + eta + ',' + delta_humanize + ',' + '\n')
        except (TypeError, AttributeError):
            print('Missed IMO')

def main():
    query_api(list_of_imos())

main()
