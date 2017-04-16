import pandas
import random

class Utility:

    @staticmethod
    def __getValueFromFile(directory, key):
        value = None

        with open(directory) as file:
            for line in file:
                if line.startswith(key):
                    value = line[len(key) + 1:]

                    break
        
        return str.strip(value)
    
    @staticmethod
    def getValueFromConfigurationFile(key):
        return Utility.__getValueFromFile(".\\configuration.ini", key)
    
    @staticmethod
    def getDataFrame(fileName):
        fileName = Utility.getValueFromConfigurationFile("data-directory") + fileName
        dataFrame = None

        if fileName.endswith(".xlsx"):
            dataFrame = pandas.read_excel(fileName)
        elif fileName.endswith(".csv"):
            dataFrame = pandas.read_csv(fileName)
        
        return dataFrame
    
    @staticmethod
    def getData(scanFor, dataFrame):
        columnHeaders = list(dataFrame)

        if (scanFor in columnHeaders):
            return random.choice(dataFrame[columnHeaders[columnHeaders.index(scanFor)]].dropna())
        else:
            for columnHeader in columnHeaders:
                    for data in dataFrame[columnHeader]:
                        if scanFor == data:
                            return random.choice(dataFrame[columnHeader].dropna())
        
        return random.choice(dataFrame["default-response"].dropna())