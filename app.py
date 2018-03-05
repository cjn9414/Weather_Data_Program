import pandas as pd
import urllib.request
import re
import sys
from pandas import DataFrame

def main():
    userInput = GetInfo()
    stations, weatherFrame = OrderInfo(userInput) #organizes information on stations by user request
    station = GetStation(stations) #id for station selected by user
    LocateData(station, userInput, weatherFrame) #finds specific data


def GetInfo():
    year = input("What year? (yyyy)")
    year = year.strip()
    day = input("What day of " + year + " are you looking for? (mmdd)\n") 
    state = input("What state? (AB = Alabama)\n")
    userInfo = {"YEAR": year, "DAY": day, "STATE": state}
    return userInfo

def OrderInfo(userInfo):
    url = "ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/by_year/" + userInfo["YEAR"] + ".csv.gz" #url for weather data
    print("Finding data...\n")
    try:
        activeStations = []
        foundStationRange = False #conditional for data-sifting loop
        appendStart = False
        appendFinish = False
        weather_df = pd.read_csv(url, sep=',', compression="gzip") #reads csv file url
        weather_df.columns = ['STATION', 'DATE', 'ELEMENT', 'VALUE', # sets columns to csv
            'M-FLAG', 'Q-FLAG', 'S-FLAG', 'OBS-TIME']

        dataIndex = 0 #row in dataframe
        iterate = 1000 #used to speed up loop
        while (not foundStationRange): #finds range of data
            try:
                row = weather_df.iloc[dataIndex] #get row
                if (int(str(row['DATE'])[4:]) >= int(userInfo['DAY'])): #if correct date
                    if (dataIndex >= iterate): #prevents potential index error
                        dataIndex -= iterate
                    foundStationRange = True
                else:
                    dataIndex += iterate
            except IndexError:
                if (dataIndex >= iterate):
                    dataIndex -= iterate
                foundStationRange = True
        print("Collecting data. May take a few seconds...\n")
        print(dataIndex)
        while (not appendStart or not appendFinish): #sifts through data range to gather station info
            try:
                row = weather_df.iloc[dataIndex]
            except IndexError:
                break
            if (not appendStart): #if previously wrong date
                if (int(str(row['DATE'])[4:]) == int(userInfo['DAY'])): #if iterated into right date
                    appendStart = True
            if (appendStart): #if set as right date
                if (int(str(row['DATE'])[4:]) == int(userInfo['DAY'])): #if still right date
                        if (row['STATION'] not in activeStations):
                            activeStations.append(row['STATION'])
                else: #wrong date, end data search
                    appendFinish = True
            dataIndex += 1
            if(dataIndex%10000 == 0):
                print(dataIndex)
        if not activeStations:
            print("Sorry, no active stations in this state on this day.")
            sys.exit()
    except OSError: #can't find csv file for user-defined year
        print("No data exists for this year")
        sys.exit()

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
            if (line_df.loc[count]['STATION'] in activeStations):
                stationList.append(line_df) #appends dataframe list
                count+=1
    if (not stationList):
        print("Sorry, no data to report.")
        sys.exit()
    station_df = pd.concat(stationList) #concatenates all dataframes in list
    print("Data collected.\n")
    return station_df, weather_df



def GetStation(relevent_stations):
    print("Here are some locations that you requested:\n")
    for index, row in relevent_stations.iterrows(): #iterate through csv file
        print (str(index+1) + ": " + row['NAME'])
    selected_station = input("Please choose the number of the location that you would like to see data for.\n")
    for index, row in relevent_stations.iterrows():
        if (row['STORE_VAL'] == selected_station):
                station_id = row['STATION']
    return station_id


def LocateData(stat_id, userInfo, weather_df):
    dataFound=False #conditional for data-sifting loops
    dataIndex=0 #row of data
    iterate = 1000 #used to 
    while(not dataFound):
        try: #chance for bound error
            dataPoint = weather_df.iloc[dataIndex] #could except
            if (int(str(dataPoint['DATE'])[4:]) > int(userInfo['DAY'])): #passed over data
                while(not dataFound):
                    dataPoint = weather_df.iloc[dataIndex]
                    userDate = int(userInfo['DAY'])
                    tempDate = int(str(dataPoint['DATE'])[4:])
                    temp_id = dataPoint['STATION']
                    if (dataIndex%1000 == 0):
                        print(dataIndex)
                    if (tempDate == userDate and
                            stat_id == temp_id): #data we are looking for
                        dataFound = True #loops will exit
                    elif (tempDate < userDate): #data doesn't exist
                        print("Sorry, no data found with this information")
                        sys.exit()
                    else:
                        dataIndex -= 1
            else:
                dataIndex += iterate
        except IndexError: #exceeded bounds for dataframe
            dataIndex -= iterate
            while(not dataFound):
                try: #similar chance for bounds error
                    dataPoint = weather_df.iloc[dataIndex]
                    if (int(str(dataPoint['DATE'])[4:]) == int(userInfo['DAY']) and
                            stat_id == dataPoint['STATION']): #data
                        dataFound = True
                    else:
                        dataIndex += 1
                except IndexError: #bound error again, data doesn't exist
                    print("Sorry, no data found with this information..")
                    sys.exit()
    print(weather_df.loc[dataIndex])















main()
