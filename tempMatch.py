import os
import re
import pandas as pd
import BLS_Request
import spacy
import numpy as np
from numpy.linalg import norm
import time
from IPython.display import display, HTML
from scipy import spatial
path = str(os.path.dirname(os.path.realpath(__file__)))

punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
exceptionWords = ["excluding","except", "other_than","not"]
#Reads a csv file and turns it into pyarrow table, then .to_pandas() converts the table to a dataframe.
def readCSV(fileName):
    # - fileName: (String) The name of the csv file to be read and converted from csv to pandas.
    return pd.read_csv(fileName)

def createBLSDataFrame():
    # Gets the group labels using the BLS_Request library.
    BLS_Request.compareLatestOnlineVersionWithLatestDownloadedVersion("pcInd","groupLabels")
    # Gets the item labels using the BLS_Request library.
    BLS_Request.compareLatestOnlineVersionWithLatestDownloadedVersion("pcLRef","labels")
    # Creates the paths for the for the item labels and the group labels
    newPath = os.path.join(path,'RawData',BLS_Request.getLatestVersionFileName("pcLRef",BLS_Request.getAllFilesInDirectory("pcLRef")))
    newGroupPath = os.path.join(path,'RawData',BLS_Request.getLatestVersionFileName("pcInd",BLS_Request.getAllFilesInDirectory("pcInd")))
    # Modifies the row headers for the two data frames.
    newGroupFrame = readCSV(newGroupPath)
    newDataFrame = readCSV(newPath)
    #_____________________________________________________________________________________THIS IS THE UP TO HERE THE CODE IS WORKING WELL LINE____________________________________________________________________
    # Merges the two dataframes using a left join.
    mergeLeft = pd.merge(left=newGroupFrame,right=newDataFrame,how='left',left_on="industry_code",right_on="industry_code")
    mergeLeft = mergeLeft.rename(columns={"industry_code":"code_1","industry_name":"code_1_name","product_code":"code_2","product_name":"code_2_name"})
    # Gets the group labels using the BLS_Request library.
    BLS_Request.compareLatestOnlineVersionWithLatestDownloadedVersion("wpGrp","groupLabels")
    # Gets the item labels using the BLS_Request library.
    BLS_Request.compareLatestOnlineVersionWithLatestDownloadedVersion("wpLRef","labels")
    # Creates the paths for the for the item labels and the group labels
    newPath = os.path.join(path,'RawData',BLS_Request.getLatestVersionFileName("wpLRef",BLS_Request.getAllFilesInDirectory("wpLRef")))
    newGroupPath = os.path.join(path,'RawData',BLS_Request.getLatestVersionFileName("wpGrp",BLS_Request.getAllFilesInDirectory("wpGrp")))
    # Modifies the row headers for the two data frames.
    newGroupFrame = readCSV(newGroupPath)
    newDataFrame = readCSV(newPath)
    # Merges the two dataframes using a left join.
    mergeRight = pd.merge(left=newGroupFrame,right=newDataFrame,how='left',left_on="group_code",right_on="group_code")
    mergeRight = mergeRight.rename(columns={"group_code":"code_1","group_name":"code_1_name","item_code":"code_2","item_name":"code_2_name"})
    BLS_DataFrame = mergeLeft.append(mergeRight)
    BLS_DataFrame["combinedCodes"] = BLS_DataFrame["code_1"] + BLS_DataFrame["code_2"]
    return BLS_DataFrame

def mainDF():
    BLS_Request.compareLatestOnlineVersionWithLatestDownloadedVersion("pcCur","Current")
    newPath = os.path.join(path,'RawData',BLS_Request.getLatestVersionFileName("pcCur",BLS_Request.getAllFilesInDirectory("pcCur")))
    BLS_Request.compareLatestOnlineVersionWithLatestDownloadedVersion("wpCur","Current")
    newPath1 = os.path.join(path,'RawData',BLS_Request.getLatestVersionFileName("wpCur",BLS_Request.getAllFilesInDirectory("wpCur")))
    dataFrame = readCSV(newPath)
    dataFrame1 = readCSV(newPath1)
    dataFrame = dataFrame.append(dataFrame1)
    dataFrame = changeRowHeaders(dataFrame).drop(0)
    dataFrame["combinedCodes"] = dataFrame["series_id"].str[3:]
    return dataFrame

def getBLSFormatted():
    blsDF = createBLSDataFrame()
    dataFrame = mainDF()
    dataFrame = pd.merge(left=dataFrame,right=blsDF,how='left',left_on="combinedCodes",right_on="combinedCodes")
    dataFrame = dataFrame.drop(['combinedCodes',"year","period","value","footnote_codes"],axis=1)    
    dataFrame = dataFrame.drop_duplicates()
    return dataFrame

def readNAPCS():
    filePath = os.path.join(path,"NAPCS-SCPAN-2017-Structure-V1-eng.csv")
    dataFrame = pd.read_csv(filePath,encoding="iso8859_15")
    return changeRowHeaders(dataFrame)

def changeRowHeaders(dataFrame):
    dfList = dataFrame.values.tolist()
    for i in range(0,len(dfList[0])):
        dataFrame = dataFrame.rename(columns = {i:dfList[0][i]})
    return dataFrame

def removeExceptions(inputString):
    if "Inputs to stage" in inputString:
        inputString = inputString[17:]
    for i in exceptionWords:
        if i in inputString:
            inputString = inputString.split(i)[0]
    return inputString

def removeComprise(string):
    if "comprises" in string:
        string = string.split("comprises")
        return string[1].strip()
    return string

def prepString(rows):
    string = removeComprise(rows)
    string = string.replace("mfg","manufacturing")
    string = string.replace(", n.e.c.",".")
    string = string.replace("other than","other_than")
    string = removeExceptions(string)
    string = re.sub("[\(\[].*?[\)\]]", "", string)
    string = string.lower()
    for i in string:
        if i in punctuations:
            string = string.replace(i,"")
    string = string.replace("  "," ")
    return convertToVector(string)

def convertToVector(string):
    doc = nlp(string)
    c = np.zeros([300])
    for token in doc:
        c += token.vector
    return c

def nNearestBLStoNAPCS(blsNumber, numberToReturn):
    dataFrame = comparisonBLS(blsNumber)
    dataFrame = dataFrame.sort_values(by="similarity", ascending=False)
    dataFrame = dataFrame.head(numberToReturn)
    dataFrame = dataFrame.drop(columns=["vector"])
    dataFrame = dataFrame.reset_index(drop=True)
    pd.set_option('display.max_colwidth', None)
    return dataFrame
    
def nNearestNAPCStoBLS(napcsNumber, numberToReturn):
    dataFrame = comparisonNAPCS(napcsNumber)
    dataFrame = dataFrame.sort_values(by="similarity", ascending=False)
    dataFrame = dataFrame.head(numberToReturn)
    dataFrame = dataFrame.drop(columns=["vector"])
    dataFrame = dataFrame.reset_index(drop=True)
    pd.set_option('display.max_colwidth', None)
    return dataFrame

def formattedVector(inputArr):
    inputArr = inputArr.split()
    for i in range(0,len(inputArr)):
        if "[" in inputArr[i]  or "]" in inputArr[i]:
            inputArr[i] = inputArr[i].replace("[","").replace("]","")
        if inputArr[i] == "":
            inputArr[i] = float(0)
 
    inputArr = list(map(float, inputArr))
    return inputArr

def comparisonBLS(blsNumber):
    blsNumber = blsNumber.strip()
    tempBLS = blsDF.loc[blsDF.series_id == blsNumber,"vector"]
    tempBLS = tempBLS.tolist()[0]
    tempBLS = tempBLS[1:-1]
    tempBLS = tempBLS.replace("\n"," ").replace("  "," ").replace("  "," ")
    #blsDFRes = blsDF[blsDF["series_id"]==blsNumber].values.tolist()[0]
    tempBLS = np.fromstring(tempBLS,dtype="float64",sep=' ')
    tempDF["similarity"] = tempDF["vector"].apply(lambda x: np.dot(np.fromstring(x[1:-1].replace("\n"," ").replace("  "," ").replace("  "," "),dtype="float64",sep=' '),tempBLS)/(norm(np.fromstring(x[1:-1].replace("\n"," ").replace("  "," ").replace("  "," "),dtype="float64",sep=' '))*norm(tempBLS)))
    return tempDF

def comparisonNAPCS(NAPCSNumber):
    NAPCSNumber = int(NAPCSNumber.strip())
    print(NAPCSNumber)
    print(tempDF)
    tempNAPCS = tempDF.loc[tempDF.Code == NAPCSNumber,"vector"]
    tempNAPCS = tempNAPCS.tolist()[0]
    tempNAPCS = tempNAPCS[1:-1]
    tempNAPCS = tempNAPCS.replace("\n"," ").replace("  "," ").replace("  "," ")
    tempNAPCS = np.fromstring(tempNAPCS,dtype="float64",sep=' ')
    blsDF["similarity"] = blsDF["vector"].apply(lambda x: np.dot(np.fromstring(x[1:-1].replace("\n"," ").replace("  "," ").replace("  "," "),dtype="float64",sep=' '),tempNAPCS)/(norm(np.fromstring(x[1:-1].replace("\n"," ").replace("  "," ").replace("  "," "),dtype="float64",sep=' '))*norm(tempNAPCS)))
    print(blsDF)
    return blsDF

def getValidCodes(blsORNAPCSvar, inputCode):
    inputCode = inputCode.strip()
    if blsORNAPCSvar == "BLS":
        temp = blsDF["series_id"].tolist()
        if inputCode in temp:
            return True
        else:
            print(str(inputCode) + " is an invalid BLS Code.")
            return False
    else:
        temp = tempDF["Code"].tolist()
        if inputCode in temp:
            return True
        else:
            print(str(inputCode) + " is an invalid NAPCS Code.")
            return False

def main(dataSet,codeToCompare,numMatches):
    if dataSet == "BLS":
        return nNearestBLStoNAPCS(codeToCompare, int(numMatches))
    else:
        return nNearestNAPCStoBLS(codeToCompare, int(numMatches))


def vectorStoragePathCreation():
    newPath = os.path.join(path,'RawData')
    # Checks if "newPath" exists and creates it if it doesn't
    if not os.path.exists(newPath):
        os.makedirs(newPath)
    vectorTableStoragePath = os.path.join(newPath,'VectorTables')
    # Checks if "newPath" exists and creates it if it doesn't
    if not os.path.exists(vectorTableStoragePath):
        os.makedirs(vectorTableStoragePath)
    return vectorTableStoragePath

def checkForBLS(path):
    blsPath = os.path.join(path,'BLSVectors.csv')
    if not os.path.exists(blsPath):
        print("Current BLSVector.csv not found. Creating new BLSVector.csv...")
        blsDF = getBLSFormatted()
        blsDF["series_id"] = blsDF["series_id"].astype(str)
        blsDF["code_2_name"] = blsDF["code_2_name"].astype(str)
        blsDF["code_1_name"] = blsDF["code_1_name"].astype(str)
        blsDF["combinedCodes"] = blsDF["code_1_name"] + " " + blsDF["code_2_name"]
        blsDF["vector"] = blsDF["combinedCodes"].map(prepString)
        print("THIS IS IN CHECKFORBLS")
        print(blsDF)
        blsDF = blsDF.dropna()
        blsDF = blsDF.drop(columns=["code_1","code_2","combinedCodes"])
        blsDF.to_csv(blsPath,index=False)
        print("BLSVector.csv created...")
        return blsDF
    else:
        print("BLSVector.csv found...")
        return pd.read_csv(blsPath)

def checkForNAPCS(path):
    napcsPath = os.path.join(path,'NAPCSVectors.csv')
    if not os.path.exists(napcsPath):
        print("Current NAPCSVectors.csv not found. Creating new NAPCSVectors.csv...")
        napcsDF = readNAPCS()
        napcsDF["Code"] = napcsDF["Code"].astype(str)
        napcsDF["Class title"] = napcsDF["Class title"].astype(str)
        napcsDF["Class definition"] = napcsDF["Class definition"].astype(str)
        napcsDF["combinedCodes"] = napcsDF["Class title"] + " " + napcsDF["Class definition"]
        napcsDF["vector"] = napcsDF["combinedCodes"].map(prepString)
        napcsDF = napcsDF.drop(columns=["Level","Hierarchical structure","combinedCodes"])
        napcsDF.to_csv(napcsPath,index=False)
        print("NAPCSVectors.csv created...")
        return napcsDF
    else:
        print("NAPCSVectors.csv found...")
        return pd.read_csv(napcsPath)

def convertToVectorWithWeightedValues(string, weights):
    doc = nlp(string)
    c = np.zeros([300])
    for token in range(0,len(doc)):
        c += (doc[token].vector * weights[token])
    return c

def parseEntry(userInput):
    # ++cattle cows beefalo -beef -meat --manufacturing
    entryArr = userInput.split(" ")
    weightsArr = []
    for i in entryArr:
        if "++" in i:
            weightsArr.append(3)
        elif "+" in i:
            weightsArr.append(2)
        elif "--" in i:
            weightsArr.append(-2)
        elif  "-" in i:
            weightsArr.append(-1)
        else:
            weightsArr.append(1)
    userInput = userInput.replace("+","").replace("-","")
    return convertToVectorWithWeightedValues(userInput,weightsArr)

def exactSearch(dataSet,exactWord,lencode,firstdig):
    if dataSet == "BLS":
        exactWord = " " + exactWord + " "
        dataFrame = blsDF
        
        dataFrame["combinedCodes"] = " " + dataFrame["code_1_name"] + " " + dataFrame["code_2_name"] + " "
        dataFrame["combinedCodes"] = dataFrame["combinedCodes"].str.lower()
        dataFrame = dataFrame.dropna()
        dataFrame = dataFrame[dataFrame["combinedCodes"].str.contains(exactWord.lower())]
        dataFrame = dataFrame.drop(columns=["combinedCodes","vector"])
        dataFrame = dataFrame.reset_index(drop=True)
        pd.set_option('display.max_colwidth', None)
        if "combinedCodes" in dataFrame:
            dataFrame = dataFrame.drop(columns=["combinedCodes"])
        return dataFrame
    elif dataSet == "NAPCS":
        exactWord = " " + exactWord + " "
        dataFrame = tempDF
        dataFrame = dataFrame.dropna()
        dataFrame["combinedCodes"] = " " + dataFrame["Class title"] + " " + dataFrame["Class definition"]+ " "
        dataFrame["combinedCodes"] = dataFrame["combinedCodes"].str.lower()
        dataFrame = dataFrame[dataFrame["combinedCodes"].str.contains(exactWord.lower())]
        if lencode == "3" or lencode == "5" or lencode == "6" or lencode == "7":
            dataFrame = dataFrame[dataFrame.Code.str.len() == int(lencode)]
        if firstdig != "":
            dataFrame = dataFrame[dataFrame.Code.astype(str).str[:1] == firstdig]
        dataFrame = dataFrame.drop(columns=["combinedCodes","vector"])
        dataFrame = dataFrame.reset_index(drop=True)
        pd.set_option('display.max_colwidth', None)
        return dataFrame

def parseResult(dataSet,entry,lencode,firstdig):
    if dataSet == "BLS":
        vectorResult = parseEntry(entry)
        dataFrame = blsDF
        dataFrame["similarity"] = dataFrame["vector"].apply(lambda x: 1 - spatial.distance.cosine(np.fromstring(x[1:-1].replace("\n"," ").replace("  "," ").replace("  "," "),dtype="float64",sep=' '), vectorResult))
        dataFrame = dataFrame.sort_values(by="similarity", ascending=False)
        dataFrame = dataFrame.head(20)
        dataFrame = dataFrame.drop(columns=["vector"])
        dataFrame = dataFrame.reset_index(drop=True)
        pd.set_option('display.max_colwidth', None)
        if "combinedCodes" in dataFrame:
            dataFrame = dataFrame.drop(columns=["combinedCodes"])
        return dataFrame 
    elif dataSet == "NAPCS":
        vectorResult = parseEntry(entry)
        dataFrame = tempDF
        dataFrame["similarity"] = dataFrame["vector"].apply(lambda x: 1 - spatial.distance.cosine(np.fromstring(x[1:-1].replace("\n"," ").replace("  "," ").replace("  "," "),dtype="float64",sep=' '), vectorResult))
        if lencode == "3" or lencode == "5" or lencode == "6" or lencode == "7":
            dataFrame = dataFrame[dataFrame.Code.str.len() == int(lencode)]
        if firstdig != "":
            dataFrame = dataFrame[dataFrame.Code.astype(str).str[:1] == firstdig]
        dataFrame = dataFrame.sort_values(by="similarity", ascending=False)
        dataFrame = dataFrame.head(20)
        dataFrame = dataFrame.drop(columns=["vector"])
        dataFrame = dataFrame.reset_index(drop=True)
        pd.set_option('display.max_colwidth', None)
        if "combinedCodes" in dataFrame:
            dataFrame = dataFrame.drop(columns=["combinedCodes"])
        return dataFrame 


vectorStoragePath = vectorStoragePathCreation()
nlp = spacy.load("en_core_web_lg")
blsDF = checkForBLS(vectorStoragePath)
tempDF = checkForNAPCS(vectorStoragePath)