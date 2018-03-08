from interface import GetInfo, GetStation, printData
from controller import OrderInfo, LocateData
def main():
    userInput = GetInfo()
    stations, weatherFrame = OrderInfo(userInput) #organizes information on stations by user request
    station = GetStation(stations) #id for station selected by user
    dataSet = LocateData(station, userInput, weatherFrame) #finds specific data
    printData(dataSet)

main()
