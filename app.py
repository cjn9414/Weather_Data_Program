from interface import GetInfo, GetStation
from controller import OrderInfo, LocateData

def main():
    userInput = GetInfo()
    stations, weatherFrame = OrderInfo(userInput) #organizes information on stations by user request
    station = GetStation(stations) #id for station selected by user
    LocateData(station, userInput, weatherFrame) #finds specific data


main()
