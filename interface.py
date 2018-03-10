import pandas as pd
import sys
import curses, time
import os

def GetInfo():
    year = input("What year? (yyyy)")
    year = year.strip()
    day = input("What day of " + year + " are you looking for? (mmdd)") 
    state = input("What state? (NY = New York)")
    userInfo = {"YEAR": year, "DAY": day, "STATE": state}
    return userInfo


def GetStation(relevent_stations):
    rowCount = relevent_stations.shape[0] #first row of dataframe
    currentRow = 1
    rowIncrement = 10
    numbers = ['0','1','2','3','4','5','6','7','8','9']
    userSelection = ""
    station_id = None
    if (rowCount < rowIncrement): #if increment would result in error
        printChoices(currentRow, rowCount, relevent_stations, rowCount)
    else: #print normally
        printChoices(currentRow, rowIncrement, relevent_stations, rowCount)
    while (True): #break will exit loop
        character = GetInput()
        if character in range(48, 58): #character is a number
            userSelection += str(chr(character)) #add number to string
        elif (character == 32): #space bar
            break
        elif (rowCount > rowIncrement): #if there is need for scroll
            if (character == "up"): #up arrow
                if (currentRow < rowCount-2*rowIncrement): #check for bounds error
                    currentRow += rowIncrement #change row
                else: #bounds error
                    currentRow = 1+rowCount-rowIncrement #go to last row
            elif (character == "down"): #down arrow
                if (currentRow > rowIncrement): #check bounds error
                    currentRow -= rowIncrement
                else: #lower bound error
                    currentRow = 1 #start from beginning
            printChoices(currentRow, rowIncrement, relevent_stations, rowCount)

    for index, row in relevent_stations.iterrows(): #loop through dataframe
        if (row['STORE_VAL'] == userSelection): #finds the station number the user chose
            print("You chose " + row['NAME'])
            station_id = row['STATION'] #get id of station
    if (station_id == None): #invalid user input
        print("Sorry, that was not a possible number")
        sys.exit()
    return station_id


def GetInput():
    try:
        inp = curses.initscr()
        curses.noecho() #disable user input to show on terminal
        k = 0
        while True:
            ch = inp.getch() #character input
            if ch in range(48, 58): #if number
                return ch
            if (ch == 32): #if space bar
                return ch
            #checks for arrows; if letter is followed by bracket is followed by esc key
            if (ch == 27):
                k = 1
            elif (ch == 91 and k ==1):
                k = 2
            elif (ch == 65 and k == 2):
                return "up"
            elif (ch==66 and k == 2):
                return "down"
            elif (ch != 27 and ch != 91):
                k = 0
            time.sleep(0.05) #take a break
    except: 
        raise
    finally:
        curses.endwin() #close window


def printChoices(rowNumber, inc, df, df_length):
    stdscr = curses.initscr() #open window
    stdscr.erase() #clear terminal

    for index in range(rowNumber, rowNumber+inc): #loop through rows
        row = df.iloc[index-1] #get row
        stdscr.addstr(row['STORE_VAL'] + ": " + row['NAME'] + "\n") #print row to terminal
    stdscr.addstr("Showing " + str(rowNumber) + "-" + str(rowNumber+inc-1) + "/" + str(df_length) + "\n")
    stdscr.addstr("Please select a station. Enter the number next to the station, then press SPACE.")
    stdscr.addstr("Use the UP/DOWN arrows to scroll")

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
