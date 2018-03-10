import pandas as pd
import urllib.request
import re
import sys

def OrderInfo(userInfo):
    url = "ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/by_year/" + userInfo["YEAR"] + ".csv.gz" #url for weather data
    print("Finding data...\n")
    try:
        activeStations = []
        foundStationRange = False #conditional for data-sifting loop
        appendStart = False
        appendFinish = False
        weather_df = pd.read_csv(url, sep=',', compression="gzip", usecols=[0,1,2,3]) #reads csv file url
        weather_df.columns = ['STATION', 'DATE', 'ELEMENT', 'VALUE'] # sets columns to csv file]
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


def LocateData(stat_id, userInfo, weather_df):
    print("Sorting data...")
    dataFound=False #conditional for data-sifting loops
    dataIndex=0 #row of data
    iterate = 1000 #used to 
    dataList = []
    while(not dataFound):
        try: #chance for bound error
            dataPoint = weather_df.iloc[dataIndex] #could except
            if (int(str(dataPoint['DATE'])[4:]) > int(userInfo['DAY'])): #passed over data
                while(not dataFound):
                    dataPoint = weather_df.iloc[dataIndex]
                    userDate = int(userInfo['DAY']) #user input date
                    tempDate = int(str(dataPoint['DATE'])[4:]) #iterator date
                    temp_id = dataPoint['STATION']
                    if (tempDate == userDate and
                            stat_id == temp_id): #data we are looking for
                        dataList.append(dataPoint)
                    elif (tempDate < userDate): #no more data to find
                        dataFound = True #loops will exit 
                    dataIndex -= 1
                    if (dataIndex < 0):
                        dataFound = True
            else:
                dataIndex += iterate
        except IndexError: #exceeded bounds for dataframe
            dataIndex -= iterate
            while(not dataFound):
                try: #similar chance for bounds error
                    dataPoint = weather_df.iloc[dataIndex]
                    userDate = int(userInfo['DAY']) #user input date
                    tempDate = int(str(dataPoint['DATE'])[4:]) #iterator date
                    temp_id = dataPoint['STATION']
                    if (tempDate == userDate and
                            stat_id == dataPoint['STATION']): #data
                        dataList.append(dataPoint)
                    elif (tempDate > userDate): #all data for day is found
                        dataFound = True
                    dataIndex += 1
                except IndexError: #csv file ends, all data found
                    dataFound = True
    
    return dataList

