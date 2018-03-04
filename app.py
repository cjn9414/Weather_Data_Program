import pandas as pd
import urllib.request
import re
import sys
from pandas import DataFrame

def main():
    userInput = GetInfo()
    stations = OrderInfo(userInput) # organizes information on stations by user request
    station = GetStation(stations) # id for station selected by user
    OutputData(station, userInput)


def GetInfo():
    year = input("What year? (yyyy)")
    year = year.strip()
    day = input("What day of " + year + " are you looking for? (mmdd)\n") 
    state = input("What state? (AB = Alabama)\n")
    userInfo = {"YEAR": year, "DAY": day, "STATE": state}
    return userInfo

def OrderInfo(userInfo):
    stationList = [] #holds all data for available stations
    count = 0
    station_url = urllib.request.urlopen("ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt")
    station_df = pd.DataFrame() #empty dataframe
    for line in station_url:
        line = str(line)[2:]
        data = {'STATION': [line[0:11].strip()], 'LAT': [line[11:21].strip()], 
                'LONG': [line[21:31].strip()], 'ELEV': [line[31:38].strip()], 
                'STATE': [line[38:41].strip()], 'NAME': [line[41:72].strip()], 
                'GSN FLAG': [line[72:76].strip()], 'HCN/CRN FLAG': [line[76:80].strip()], 
                'WMO': [line[80:86].strip()], 'STORE_VAL': [str(len(stationList)+1)]}
        if (data['STATE'][0] == userInfo["STATE"]):
            line_df = pd.DataFrame(data=data, index=[count]) #uses data from station url to make a 1 row dataframe
            stationList.append(line_df) #appends dataframe list
        count+=1
    station_df = pd.concat(stationList) #concatenates all dataframes in list
    print("done")
    return station_df



def GetStation(relevent_stations):
    print("Here are some locations that you requested:\n\n")
    for index, row in relevent_stations.iterrows(): #iterate through csv file
        print (row['STORE_VAL'] + ": " + row['NAME'])
    selected_station = input("Please choose the number of the location that you would like to see data for.\n")
    for index, row in relevent_stations.iterrows():
        if (row['STORE_VAL'] == selected_station):
                station_id = row['STATION']
    return station_id


def OutputData(stat_id, userInfo):
    url = "ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/by_year/" + userInfo["YEAR"] + ".csv.gz" #url for weather data
    try:
        weather_df = pd.read_csv(url, sep=',', compression="gzip") #reads csv file url
        weather_df.columns = ['STATION', 'DATE', 'ELEMENT', 'VALUE', # sets columns to csv
            'M-FLAG', 'Q-FLAG', 'S-FLAG', 'OBS-TIME']

    except OSError:
        print("No data exists for this year")
        sys.exit()

    dataFound=False
    dataIndex=0
    iterate = 10000
    while(not dataFound):
        try:
            dataPoint = weather_df.iloc[dataIndex]
            if (int(str(dataPoint['DATE'])[4:]) >= int(userInfo['DAY'])):
                lowerBound = dataIndex-100
                while(not dataFound):
                    if (int(str(dataPoint['DATE'])[4:]) == int(userInfo['DAY']) and
                            stat_id == dataPoint['STATION']):
                        dataFound = True
                    elif (dataIndex == lowerBound):
                        print("Sorry, no data found with this information")
                        sys.exit()
                    else:
                        dataIndex -= 1
            else:
                dataIndex += iterate

        except IndexError:
            dataIndex -= iterate
            while(not dataFound):
                try:
                    dataPoint = weather_df.iloc[dataIndex]
                    if (int(str(dataPoint['DATE'])[4:]) == int(userInfo['DAY']) and
                            stat_id == dataPoint['STATION']):
                        dataFound = True
                    else:
                        dataIndex += 1
                except IndexError:
                    print("Sorry, no data found with this information.")
                    sys.exit()
    print(weather_df.loc[dataIndex])

    















main()
