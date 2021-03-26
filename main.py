from bs4 import BeautifulSoup
import requests
import xlwt
import xlrd
from xlwt import Workbook
import tkinter as tk
from tkinter import*
from PIL import ImageTk, Image
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


# Define the window
window = tk.Tk()
window.title("QB Data Retriever")
# Frame definition
frame1 = tk.Frame(master=window, width=500,
                  height=500, bg="black")
frame1.pack(fill=tk.BOTH)

# Input label
userInput_lbl = tk.Label(master=frame1,
                         text="QB Name", bg="black",
                         fg="#D50A0A",
                         relief='solid', borderwidth=3)
userInput_lbl.place(x=250, y=200, anchor="center")

# Entry box
userEntryBox_entry = tk.Entry(master=frame1)
userEntryBox_entry.place(x=250, y=225, anchor="center")

# This function retrieves the name of the player that the user has inputted and saves it into two different variables.
# One of the variables is to be passed throughout the program, and the other is used in the next function getPlayerInfo
# Before returning the values, they are entered into a list so that they can be used in the next function.
def getName():
    playerName = userEntryBox_entry.get()
    newWindowVar = playerName
    getNameVars = [playerName, newWindowVar]
    return getNameVars

# This function scrapes the data and saves it into a file. It is highly commented within the function
def getPlayerInfo(getNameVars):
    # Changing player input for the filename used at the end
    playerName = getNameVars[0]
    newWindowVar = getNameVars[1]
    playerNameOriginal = playerName.replace(" ", "_")

    # Open file
    QBList = open('QBList.csv')
    # Create list with file
    QBListData = list(QBList)
    # Strip items of newline
    QBListData = [x.strip('\n') for x in QBListData]

     # Creating a list that is equal to QBListData to test user input against so that QBList data doesn't need to be changed
    TestList = ['Kyler Murray', 'Matt Ryan', 'Lamar Jackson', 'Josh Allen', 'Teddy Bridgewater',
                'Mitchell Trubisky', 'Brandon Allen', 'Baker Mayfield', 'Andy Dalton', 'Drew Lock',
                'Matthew Stafford', 'Aaron Rodgers', 'Deshaun Watson', 'Philip Rivers', 'Mike Glennon',
                'Chad Henne', 'Derek Carr', 'Justin Herbert', 'John Wolford', 'Wake Forest', 'Tua Tagovailoa',
                'Kirk Cousins', 'Cam Newton', 'Drew Brees', 'Daniel Jones', 'Sam Darnold', 'Jalen Hurts',
                'Mason Rudolph', 'C.J. Beathard', 'Russell Wilson', 'Tom Brady', 'Ryan Tannehill',
                'Alex Smith', 'Patrick Mahomes']
    
    # Editing the data in our TestList so that we can sanitize user input by comparing it to the currently supported list of players
    TestList = [x.replace(" ", "") for x in TestList]
    TestList = [x.lower() for x in TestList]

    # This for loop sanitizes the data and sets the playerName variable to the correct element in the supported players list
    for item in TestList:
        playerName = playerName.lower()
        playerName = playerName.replace(" ", "")
        if item == playerName:
            newIndex = TestList.index(item)
            playerName = QBListData[newIndex]
            newWindowVar = QBListData[newIndex]
            playerNameOriginal = playerName
            playerName = playerName.replace(" ", "-")
            playerName = playerName.lower()
        else:
            exit("Unsupported Player")
    
    # url is the website that we're scraping data from. It uses the sanitized user input as playerName
    url = f"https://www.nfl.com/players/{playerName}/stats/career"
    source = requests.get(url).text

    soup = BeautifulSoup(source, 'lxml')
    
    # Headers are our columns our table that we will be saving the stats in
    headers = soup.find('table',
                        class_='d3-o-table d3-o-standings--detailed d3-o-table--sortable {sortlist: [[0,1]], debug: true}').thead.text.split(
        "\n")
    headers = list(filter(None, headers))
  
    # Data consists of the statistics in the table under the headers
    data = soup.find('table',
                     class_='d3-o-table d3-o-standings--detailed d3-o-table--sortable {sortlist: [[0,1]], debug: true}').tbody.text.replace(
        " ", "").split('\n')
    newData = list(filter(None, data))

    # Creating the workbook
    wb = Workbook()
    
    
    sheet1 = wb.add_sheet(playerName, cell_overwrite_ok=True)
    
    #Style makes our headers bold during our while loop that writes them to the excel sheet
    style = xlwt.easyxf('font: bold 1')
    horizontalColumn = 1
    verticalRow = 1
    columnData = 0
    while columnData < len(headers):
        sheet1.write(verticalRow, horizontalColumn, headers[columnData], style)
        horizontalColumn = horizontalColumn + 1
        columnData = columnData + 1

    start = 0
    verticalRow = 2
    lengthOfData = [list(range(21))]
    currentRow = 1
    endPoint = (len(newData) / 17) + 1
    while currentRow < endPoint:
        dataCounter = 0
        horizontalColumn = 1
        while dataCounter < 17:
            sheet1.write(verticalRow, horizontalColumn, newData[start])
            horizontalColumn = horizontalColumn + 1
            start = start + 1
            dataCounter = dataCounter + 1
        currentRow = currentRow + 1
        verticalRow = verticalRow + 1
    
    # This sets our file name to the name in our list of supported players combined with a string and then saves the file
    fileName = f"Data/{playerNameOriginal} Passing Stats.xls"
    wb.save(fileName)

    return newWindowVar

# This is the function our button executes later on
def getAll():
    getPlayerInfo(getName())

# This is the command our clear button executes that allows the user to quickly clear the text box in case they want to input multiple players
def clearEntry():
    userEntryBox_entry.delete(0, tk.END)

# This is the command that our exit button executes to allow the user to close the program
def exitClient():
    window.destroy()


# Instruction
instruction = tk.Text(master=frame1, height=10,
                      width=52, bg="black", padx=0, pady=0,
                      fg="#D50A0A", relief='ridge',
                      highlightthickness=0, borderwidth=0)

instruction_lbl = "INSTRUCTIONS\n" \
                  "To find a single QB, type in the name\n" \
                  "of the QB, and press Submit.\n" \
                  "If you would like to find multiple\n" \
                  "QBs, click Clear after clicking submit\n" \
                  "and enter the next QB until done.\n" \
                  "When complete, click Exit and the spreadsheets\n" \
                  "with the QB data will be in the current\n" \
                  "directory in the Data folder."

instruction.insert(tk.END, instruction_lbl)

instruction.place(x=250, y=375, anchor='center')

exitButton_btn = tk.Button(master=frame1, text="Exit", command=exitClient)
exitButton_btn.place(x=295, y=475, anchor='center')

# Defines and places the image in the main window
img = Image.open('tom-brady-patriots-nfl-wachira-kacharat.png')
img2 = img.resize((200, 150), Image.ANTIALIAS)
img3 = ImageTk.PhotoImage(img2)

img4 = Label(image=img3, border=0)
img4.place(x=250, y=0, anchor='n')

userEntrySubmit_btn = tk.Button(master=frame1,
                                text="Get Stats", command=getAll)
userEntrySubmit_btn.place(x=210, y=255, anchor="center")


# This is what the charts button executes and is currently a work in progress. It will display all of our data in a nice, visually pleasing and easy to read chart.
def getCharts():

    newWindowVar = getPlayerInfo(getName())
    chartWindow = tk.Tk()
    chartWindowTitle = f"Stats Chart"
    chartWindow.title(chartWindowTitle)
    frame2 = tk.Frame(master=chartWindow, width=500, height=500, bg='black')
    frame2.pack(fill=tk.BOTH)

    def exitChartWindow():
        chartWindow.destroy()
    chartExitButton_btn = tk.Button(master=frame2, text="Exit", command=exitChartWindow)
    chartExitButton_btn.place(x=250, y=475, anchor='center')

    chartFileName = f"Data/{newWindowVar} Passing Stats.xls"
    df = pd.read_excel(chartFileName, header=1, usecols="B,D:R")

    # x axis values
    xAxVals = [column for column in df]
    xAxVals.pop(0)
    xAxVals = np.arange(len(df))
    # y axis values
    yAxVals = df.iloc[:, 0].tolist()
    yAxVals = np.arange(len(df))
    z = [xAxVals, yAxVals]
    z = np.arange(len(df))

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(range(len(xAxVals)), range(len(yAxVals)), z)
    plt.yticks(range(len(yAxVals)), yAxVals)
    plt.xticks(range(len(xAxVals)), xAxVals)
    plt.show()

    chartWindow.mainloop()


clearEntry_btn = tk.Button(master=frame1, text="   Clear ", command=clearEntry)
clearEntry_btn.place(x=295, y=255, anchor="center")

currentCharts = tk.Button(text="Charts", command=getCharts)
currentCharts.place(x=210, y=475, anchor='center')

# Loop the window
window.mainloop()
