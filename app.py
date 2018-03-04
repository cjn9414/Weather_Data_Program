import pandas as pd
import urllib.request
import re
import sys
from pandas import DataFrame

def main():
    stationList = [] #holds all data for available stations
    count = 0
    year = input("What year? (yyyy)")
    year = year.strip()
    day = input("What day of " + year + " are you looking at? (mmdd)\n")
    state = input("What state? (AB = Alabama)\n")
    url = "ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/by_year/" + year + ".csv.gz" #url for weather data
    weather_df = pd.read_csv(url, sep=',', compression="gzip") #reads csv file url
    weather_df.columns = ['STATION', 'DATE', 'ELEMENT', 'VALUE', # sets columns to csv
            'M-FLAG', 'Q-FLAG', 'S-FLAG', 'OBS-TIME']
    station_url = urllib.request.urlopen("ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt")
    station_df = pd.DataFrame() #empty dataframe
    for line in station_url:
        line = str(line)[2:]
        data = {'STATION': [line[0:11].strip()], 'LAT': [line[11:21].strip()], 'LONG': [line[21:31].strip()], 'ELEV': [line[31:38].strip()], 'STATE': [line[38:41].strip()], 'NAME': [line[41:72].strip()], 'GSN FLAG': [line[72:76].strip()], 'HCN/CRN FLAG': [line[76:80].strip()], 'WMO': [line[80:86].strip()]}
        line_df = pd.DataFrame(data=data, index=[count]) #uses data from station url to make a 1 row dataframe
        stationList.append(line_df) #appends dataframe list
        count+=1
        if (count%1000 == 0):
            print(count)
    station_df = pd.concat(stationList) #concatenates all dataframes in list
    print("done")
    station_csv = station_df.to_csv(sep=',') #dataframe to csv
    

main()
