"""
 * @file logg.py
 * @authors Steven Kalapos & Ben Bellerose
 * @date May 2018
 * @modified August 11 2018
 * @modifiedby BB
 * @brief logging systems for device
 */
 """
import os
import csv
import shutil
import time
from time import gmtime,strftime

class deviceLog():

    def __init__(self):
        dirHold = os.getcwd().split("/")
        dirHold = dirHold[:-1]
        self.logDir = "/".join(dirHold) + str("/logs/")

    """Input: type - string containing error code relarted to error type
              description - string containing description of what caused error
        Function: logs what vaused the error in desired location
        Output: returns a boolean value to inform user of log state"""
    def errorLog(self,errorType,description):
        if errorType is not None:
            if description is not None:
                date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                content = str(date) + ":" + str(errorType) + ": " + str(description)
                #set location of log file
                logFile = str(self.logDir) + str("errorLog.txt")
                #attempt to read log file
                if os.path.isfile(logFile):
                    fileRead = open(logFile,"r")
                    #write error log into existing error log
                    fileHold = fileRead.readlines()
                    fileRead.close()
                    fileHold.insert(len(fileHold),content)
                    fileWrite = open(logFile,"w")
                    x = 0
                    while x < len(fileHold):
                        fileWrite.write(fileHold[x].replace("\n",""))
                        if x < len(fileHold) - 1:
                            fileWrite.write("\n")
                        x = x + 1
                    fileWrite.close()
                    return True
                else:
                    fileWrite = open(logFile,"w+")
                    fileWrite.write(content)
                    fileWrite.close()
                    return True
            else:
                return False
        else:
            return False

    """Input: fileName - string containing file adress to csv file
        Function: reads CSV file and return the contents
        Output: returns a list containing the values for the setpoints and their values"""
    def readCSV(self,fileName):
        if fileName is not None:
            fullFile = str(self.logDir) + str(fileName)
            if os.path.isfile(fullFile):
                try:
                    fileOpen = open(fullFile, "r")
                    content = list(csv.reader(fileOpen))
                    return content
                except Exception as e:
                    errCode = "ERROR READING FILE"
                    errMsg = "Error reading CSV file. The following error code appeared; " + str(e)
                    self.errorLog(errCode,errMsg)
                    print("ERROR READING FILE")
                    content = None
                    return content
            else:
                errCode = "FILE NOT FOUND"
                errMsg = "The given file adress for the CSV file does not exist."
                self.errorLog(errCode,errMsg)
                print("FILE NOT FOUND")
                content = None
                return content
        else:
            errCode = "NO FILE NAME GIVEN"
            errMsg = "No file name was given for the CSV file."
            self.errorLog(errCode,errMsg)
            print("NO FILE NAME GIVEN")
            content = None
            return content

    """Input: content - list containing data you want to input into csv
              fileName - string containing the name of the file
       Function: overwrite all data inside of the csv with chosen data
       Output: writes boolean value to show user success of csv write"""
    def inputCSV(self,content,fileName):
        if content is not None:
            if fileName is not None:
                fullFile = str(self.logDir) + str(fileName)
                if os.path.isfile(fullFile):
                    try:
                        with open(fullFile, 'wb') as csvfile:
                            spamWriter = csv.writer(csvfile, delimiter=',',quotechar=',', quoting=csv.QUOTE_MINIMAL)
                            for x in range(len(content)):
                                rowHold = []
                                for a in range(len(content[x])):
                                    rowHold.insert(len(rowHold),content[x][a])
                                spamWriter.writerow(rowHold)
                        return True
                    except Exception as e:
                        errCode = "ERROR WRITING CSV"
                        errMsg = "Unable to write the CSV file. The following error occured; " + str(e)
                        self.errorLog(errCode,errMsg)
                        print("ERROR WRITING CSV")
                        return False
                else:
                    errCode = "FILE NOT FOUND"
                    errMsg = "The given file adress for the CSV file does not exist."
                    self.errorLog(errCode,errMsg)
                    print("FILE NOT FOUND")
                    return False
            else:
                errCode = "NO FILE GIVEN"
                errMsg = "A file adress was not given as an input."
                self.errorLog(errCode,errMsg)
                print("NO FILE GIVEN")
                return False
        else:
            errCode = "NO CONTENT GIVEN"
            errMsg = "There was no content given as an input."
            self.errorLog(errCode,errMsg)
            print("NO CONTENT GIVEN")
            return False

    """Input: fileName - string containing the name of the file you wish to duplicate
              newName - string containing the name of the resultant file
       Function: duplicates a file and renames it to a name of your choice.
       Output: writes boolean value to show user success of csv write"""
    def duplicateFile(self,fileName,newName):
        if fileName is not None:
            if newName is not None:
                fullFile = str(self.logDir) + str(fileName)
                fullNew = str(self.logDir) + str(newName)
                if os.path.isfile(fullNew):
                    os.remove(newName)
                    time.sleep(0.1)
                if os.path.isfile(fullFile):
                    shutil.copyfile(fullFile,fullNew)
                    return True
                else:
                    errCode = "FILE NOT FOUND"
                    errMsg = "The given file could not be found."
                    self.errorLog(errCode,errMsg)
                    print("FILE NOT FOUND")
                    return False
            else:
                errCode = "NO NEW NAME GIVEN"
                errMsg = "There was no new file name provided as an input."
                self.errorLog(errCode,errMsg)
                print("NO NEW NAME GIVEN")
                return False
        else:
            errCode = "NO FILE NAME GIVEN"
            errMsg = "There was no file name provided as an input."
            self.errorLog(errCode,errMsg)
            print("NO FILE NAME GIVEN")
            return False

    """Input: fileName - string containing the name of the file you wish to search
              index - integer containing the current day of the schedule
       Function: gathers all setpoints for a given index.
       Output: writes list containing all setpoints for the given index"""
    def findSP(self,fileName,index):
        if fileName is not None:
            if index is not None:
                if type(index) == int:
                    fullSchedule = self.readCSV(fileName)
                    fullSP = fullSchedule[int(index)+1]
                    tempBank = [fullSP[1],fullSP[2],fullSP[3]]
                    humidBank = [fullSP[4],fullSP[5],fullSP[6]]
                    CO2Bank = [fullSP[7],fullSP[8],fullSP[9]]
                    lightBank = [fullSP[10],fullSP[11],fullSP[12],fullSP[13]]
                    curTime = time.strftime("%H")

                    if int(curTime) <= 8:
                        setpoints = [tempBank[0],humidBank[0],CO2Bank[0]]
                    elif int(curTime) > 8 and int(curTime) <= 16:
                        setpoints = [tempBank[1],humidBank[1],CO2Bank[1]]
                    elif int(curTime) > 16 and int(curTime) <= 24:
                        setpoints = [tempBank[2],humidBank[2],CO2Bank[2]]
                    for x in range(len(lightBank)):
                        setpoints.insert(len(setpoints),lightBank[x])
                    return setpoints
                else:
                    errCode = "INDEX NOT INTEGER"
                    errMsg = "The given index was not the correct data type."
                    self.errorLog(errCode,errMsg)
                    print("INDEX NOT INTEGER")
                    return ["ERROR"]
            else:
                errCode = "NO INDEX GIVEN"
                errMsg = "There was no index provided as an input."
                self.errorLog(errCode,errMsg)
                print("NO INDEX GIVEN")
                return ["ERROR"]
        else:
            errCode = "NO FILE NAME GIVEN"
            errMsg = "There was no file name as an input."
            self.errorLog(errCode,errMsg)
            print("NO FILE NAME GIVEN")
            return ["ERROR"]
