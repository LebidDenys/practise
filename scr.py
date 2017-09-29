import string
import math
import re
import copy

INPUT_DATA_FILENAME = '002_.t22'
OUTPUT_DATA_FILENAME = 'result.t22'


def checker(index, column, delta, data):
    return True if (math.fabs(float(data[index+1][column]) - float(data[index][column])) != delta) else False


def timeChecker(time, timeBigger, maximum):
    if (time >= maximum):
        time = 0 + float(time) % 1
        timeBigger = str(int(timeBigger) + 1)
    return (time, timeBigger)


def errorFixer(data, index, start, finish):
    """
    Take parammetrs of error and fix it
    """
    finish = 1 if start + finish == 0 else finish

    for k in range(start + finish):
        x = index - start
        data.pop(x)

    for k in range(4):
        x = index + k - start
        temp = copy.copy(data[x - 4])
        temp[5] = float(temp[5]) + 1
        temp[5] = str(timeChecker(temp[5], temp[4], 60.0)[0])

        temp[5] = temp[5] + '0' if (len(temp[5]) == 4 and temp[5][0] != '0' and temp[5][1] != '.') else temp[5]
        temp[5] = temp[5] + '0' if ((temp[5][0] == '0' and temp[5][2] == '0') or len(temp[5]) == 3) else temp[5]
        temp[4] = temp[4] + '0' if len(temp[4]) == 1 else temp[4]
        temp[3] = temp[3] + '0' if len(temp[3]) == 1 else temp[3]
        data.insert(x, temp)


def loadLines():
    """
    Loads file and returns a embedded list of values in file
    """
    print "Loading file..."
    # inFile: file
    inFile = open(INPUT_DATA_FILENAME, 'r', 0)
    linesList = inFile.readlines()
    for i in range(len(linesList)):
         linesList[i] = string.split(linesList[i])
    print "  ", len(linesList), "lines loaded."
    return linesList


def dataCleaner(linesList):
    """
    Search errors in data file and fix it using function,
    then search and fix duplicates
    """
    for i in range(len(linesList) - 1):

        if (checker(i, 5, 0.25, linesList) and (checker(i, 4, 1, linesList)) and (checker(i, 3, 1, linesList)) and (checker(i, 2, 1, linesList))):
            print "error in ", i+1, " line"
            #print linesList[i][1], linesList[i][2], linesList[i][3], linesList[i][4], linesList[i][5], linesList[i+1][5]

            start = int(float(linesList[i][5]) % 1 * 4)

            for j in range(20):
                if (float(linesList[i+j][5]) % 1 == 0):
                    finish = j
                    break
            errorFixer(linesList, i, start, finish)

    duplicatsList = []
    for i in range(len(linesList) - 1):
        if (float(linesList[i][5]) - float(linesList[i - 4][5]) == 0):
            duplicatsList.append(i)

    for i in range(len(duplicatsList)):
        linesList.pop(duplicatsList[i / 4])

    cleanData = linesList
    return cleanData


def dataPreparer(cleanData):
    """
    Preparing data for writting in file
    returns data in string
    """
    preparedData = ''

    for i in range(len(cleanData)):

        cleanData[i][5] = (5 - len(str(cleanData[i][5]))) * ' ' + cleanData[i][5]
        for j in range (7, 13):
            j = j+1 if (j == 8) else j
            cleanData[i][j] = 3 * ' ' + cleanData[i][j]
            if cleanData[i][j][4] == ' ':
                 cleanData[i][j] = cleanData[i][j][3:len(str(cleanData[i][j]))]
        cleanData[i][14] = 2 * ' ' + cleanData[i][14]

        ' '.join(cleanData[i])
        cleanData[i] = str(cleanData[i])
        cleanData[i] = re.sub(',', '', cleanData[i])
        cleanData[i] = re.sub("'", '', cleanData[i])
        cleanData[i] = cleanData[i][1:-1] + '\n'
        preparedData += cleanData[i]

    return preparedData


def dataWritter(preparedData):
    """
    Creates file and write result in it
    """
    outFile = open(OUTPUT_DATA_FILENAME, 'w')
    outFile.write(preparedData)
    outFile.close()


linesList = loadLines()
cleanData = dataCleaner(linesList)
preparedData = dataPreparer(cleanData)
dataWritter(preparedData)
