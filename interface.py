import pandas as pd

def GetInfo():
    year = input("What year? (yyyy)")
    year = year.strip()
    day = input("What day of " + year + " are you looking for? (mmdd)\n") 
    state = input("What state? (AB = Alabama)\n")
    userInfo = {"YEAR": year, "DAY": day, "STATE": state}
    return userInfo


def GetStation(relevent_stations):
    print("Here are some locations that you requested:\n")
    for index, row in relevent_stations.iterrows(): #iterate through csv file
        print (str(index+1) + ": " + row['NAME'])
    selected_station = input("Please choose the number of the location that you would like to see data for.\n")
    for index, row in relevent_stations.iterrows():
        if (row['STORE_VAL'] == selected_station):
                station_id = row['STATION']
    return station_id


def printData(dataList): #prints data found from controller
    printNonCore = False
    coreResponse = False
    if (not dataList): #no data was recorded
        print("No data to report")
    else:
        translator = pd.read_csv("./ghcn_translator.csv", header = None, sep=",")
        for data in dataList:
            for index, row in translator.iterrows():
                if (str(row[0]).strip() == str(data['ELEMENT'])):
                    if (str(row[2]) == "True"):
                        print(row[1].strip() + " " + str(data['VALUE'])) #print data
                    else:
                        if (not coreResponse):
                            response = input("This data contains elements that are not core elements. Would you like these elements printed as well? (y/n)")
                            if (response == 'y' or response == 'Y'):
                                printNonCore = True
                            coreResponse = True
                        if (printNonCore):
                            print(row[1].strip() + " " + str(data['VALUE']))
