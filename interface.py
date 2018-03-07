from pandas import DataFrame

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


