'''
Pass the filename to the SparsityFiller function and it will produce a new file with data markings
For all of the missing data
Currently takes some time if the number of observations and dimensions is high
'''

import pandas as pd
import datetime

def SparsityFiller(csv):
    '''
    Finds all the missing data (from sparsity) and writes a new file with the complete data
    Complete data means showing data markings
    '''
    currentTime = datetime.datetime.now()
    df = pd.read_csv(csv, dtype = str)
    originalDF = df.copy()
    outputFile = csv[:-4] + '-without-sparsity.csv'
    
    #first a quick check to see if dataset is actually sparse
    v4marker = int(df.columns[0][-1])   #only interested in codelist columns
    columnList = list(df.columns)
    columnCodeList = columnList[v4marker + 1::2]    #just codelist id columns
    columnLabelList = columnList[v4marker + 2::2]

    unsparseLength = 1  #total length of df if 100% complete
    for col in columnCodeList:
        unsparseLength *= df[col].unique().size
    numberOfObs = df.index.size
    if unsparseLength == numberOfObs:
        raise Exception('Dataset looks complete..')
    
    #quick check to make sure code will accept this many dimensions
    NumberOfDimensionsCheck(columnCodeList)
    
    #list of lists of unique values for each dimension
    uniqueListOfCodesInColumns = UniqueListOfCodesInColumns(df, columnCodeList)
    
    #combining all the current combinations into a new column
    df['combo'] = AddingCombinationColumnToDF(df, columnCodeList)
    
    #finds all possible combinations
    allCombos = FindAllCombinations(uniqueListOfCodesInColumns)
    
    #finding a list of all the missing combinations      
    currentCombosList = list(df['combo'].unique())                      
    missingCombos = FindMissingCombinations(allCombos, currentCombosList)
            
    #spliting each combo into a separate list
    splittingMissingCombinations = SplittingMissingCombinations(missingCombos, columnCodeList)
        
    #dicts to fill in labels
    dictsToSortLabels = DictsToSortLabels(df, columnLabelList, columnCodeList)
    
    #creating a new dataframe
    data = DataDict(columnCodeList, splittingMissingCombinations)
    newDF = pd.DataFrame(data, columns = columnList)
    newDF['Data_Marking'] = '.'
    
    #applying the dicts
    newDF = ApplyingTheDicts(newDF, dictsToSortLabels, columnCodeList, columnLabelList)
    
    #concating the df's
    concatDF = ReorderingDF(newDF, originalDF, v4marker)
    
    concatDF.to_csv(outputFile, index = False)
    
    print('SparsityFiller took {}'.format(datetime.datetime.now() - currentTime))
    
    #return concatDF
        
        
def UniqueListOfCodesInColumns(df, columnCodeList):
    '''
    columnCodeList is a list of column code ID names
    returns a list of lists of unique values for each dimension
    '''
    
    if len(columnCodeList) == 3:
        firstList = list(df[columnCodeList[0]].unique())
        secondList = list(df[columnCodeList[1]].unique())
        thirdList = list(df[columnCodeList[2]].unique())
        return [firstList, secondList, thirdList]
    
    elif len(columnCodeList) == 4:
        #all unique values from each code column
        firstList = list(df[columnCodeList[0]].unique())
        secondList = list(df[columnCodeList[1]].unique())
        thirdList = list(df[columnCodeList[2]].unique())
        forthList = list(df[columnCodeList[3]].unique())
        return [firstList, secondList, thirdList, forthList]
    
    elif len(columnCodeList) == 5:
        #all unique values from each code column
        firstList = list(df[columnCodeList[0]].unique())
        secondList = list(df[columnCodeList[1]].unique())
        thirdList = list(df[columnCodeList[2]].unique())
        forthList = list(df[columnCodeList[3]].unique())
        fithList = list(df[columnCodeList[4]].unique())
        return [firstList, secondList, thirdList, forthList, fithList]
    
    elif len(columnCodeList) == 6:
        #all unique values from each code column
        firstList = list(df[columnCodeList[0]].unique())
        secondList = list(df[columnCodeList[1]].unique())
        thirdList = list(df[columnCodeList[2]].unique())
        forthList = list(df[columnCodeList[3]].unique())
        fithList = list(df[columnCodeList[4]].unique())
        sixthList = list(df[columnCodeList[5]].unique())
        return [firstList, secondList, thirdList, forthList, fithList, sixthList]
    
def FindAllCombinations(uniqueListOfCodesInColumns):
    '''
    finds and returns all possible combinations
    each combination is a string, separated by a '^'
    '''
    if len(uniqueListOfCodesInColumns) == 3:
        allCombos = []  #list of all combinations
        for first in uniqueListOfCodesInColumns[0]:
            for second in uniqueListOfCodesInColumns[1]:
                for third in uniqueListOfCodesInColumns[2]:
                    allCombos.append(first + '^' + second + '^' + third)
                    
    elif len(uniqueListOfCodesInColumns) == 4:
        allCombos = []  #list of all combinations
        for first in uniqueListOfCodesInColumns[0]:
            for second in uniqueListOfCodesInColumns[1]:
                for third in uniqueListOfCodesInColumns[2]:
                    for forth in uniqueListOfCodesInColumns[3]:
                        allCombos.append(first + '^' + second + '^' + third + '^' +forth)
    
    elif len(uniqueListOfCodesInColumns) == 5:
        allCombos = []  #list of all combinations
        for first in uniqueListOfCodesInColumns[0]:
            for second in uniqueListOfCodesInColumns[1]:
                for third in uniqueListOfCodesInColumns[2]:
                    for forth in uniqueListOfCodesInColumns[3]:
                        for fith in uniqueListOfCodesInColumns[4]:
                            allCombos.append(first + '^' + second + '^' + third + '^' +\
                                          forth + '^' + fith)
                            
    elif len(uniqueListOfCodesInColumns) == 6:
        allCombos = []  #list of all combinations
        for first in uniqueListOfCodesInColumns[0]:
            for second in uniqueListOfCodesInColumns[1]:
                for third in uniqueListOfCodesInColumns[2]:
                    for forth in uniqueListOfCodesInColumns[3]:
                        for fith in uniqueListOfCodesInColumns[4]:
                            for sixth in uniqueListOfCodesInColumns[5]:
                                allCombos.append(first + '^' + second + '^' + third + '^' +\
                                          forth + '^' + fith + '^' + sixth)
    return allCombos

def FindMissingCombinations(allCombos, currentCombosList):
    '''
    finds and returns a list of all combinations not currently found in the v4
    '''
    missingCombos = []
    for combo in allCombos:
        if combo in currentCombosList:
            currentCombosList.remove(combo)
        else:
            missingCombos.append(combo)    
    return missingCombos

def SplittingMissingCombinations(missingCombos, columnCodeList):
    '''splits the missing combinations into separate lists for each dimension'''
    if len(columnCodeList) == 3:
        firstCombo, secondCombo, thirdCombo = [], [], []
        for code in missingCombos:
            newValue = code.split('^')
            firstCombo.append(newValue[0])
            secondCombo.append(newValue[1])
            thirdCombo.append(newValue[2])
        return [firstCombo, secondCombo, thirdCombo]
    
    elif len(columnCodeList) == 4:
        firstCombo, secondCombo, thirdCombo, forthCombo = [], [], [], []
        for code in missingCombos:
            newValue = code.split('^')
            firstCombo.append(newValue[0])
            secondCombo.append(newValue[1])
            thirdCombo.append(newValue[2])
            forthCombo.append(newValue[3])
        return [firstCombo, secondCombo, thirdCombo, forthCombo]
    
    elif len(columnCodeList) == 5:
        firstCombo, secondCombo, thirdCombo, forthCombo, fithCombo = [], [], [], [], []
        for code in missingCombos:
            newValue = code.split('^')
            firstCombo.append(newValue[0])
            secondCombo.append(newValue[1])
            thirdCombo.append(newValue[2])
            forthCombo.append(newValue[3])
            fithCombo.append(newValue[4])
        return [firstCombo, secondCombo, thirdCombo, forthCombo, fithCombo]
    
    elif len(columnCodeList) == 6:
        firstCombo, secondCombo, thirdCombo, forthCombo, fithCombo, sixthCombo = [], [], [], [], [], []
        for code in missingCombos:
            newValue = code.split('^')
            firstCombo.append(newValue[0])
            secondCombo.append(newValue[1])
            thirdCombo.append(newValue[2])
            forthCombo.append(newValue[3])
            fithCombo.append(newValue[4])
            sixthCombo.append(newValue[5])
        return [firstCombo, secondCombo, thirdCombo, forthCombo, fithCombo, sixthCombo]
    
def DictsToSortLabels(df, columnLabelList, columnCodeList):
    '''
    creates a list of dicts that will be used to fill in the labels 
    (using the existing data from the v4)
    '''
    if len(columnCodeList) == 3:
        firstDict = dict(zip(df[columnCodeList[0]], df[columnLabelList[0]]))
        secondDict = dict(zip(df[columnCodeList[1]], df[columnLabelList[1]]))
        thirdDict = dict(zip(df[columnCodeList[2]], df[columnLabelList[2]]))
        return [firstDict, secondDict, thirdDict]
    
    elif len(columnCodeList) == 4:
        firstDict = dict(zip(df[columnCodeList[0]], df[columnLabelList[0]]))
        secondDict = dict(zip(df[columnCodeList[1]], df[columnLabelList[1]]))
        thirdDict = dict(zip(df[columnCodeList[2]], df[columnLabelList[2]]))
        forthDict = dict(zip(df[columnCodeList[3]], df[columnLabelList[3]]))
        return [firstDict, secondDict, thirdDict, forthDict]
    
    elif len(columnCodeList) == 5:
        firstDict = dict(zip(df[columnCodeList[0]], df[columnLabelList[0]]))
        secondDict = dict(zip(df[columnCodeList[1]], df[columnLabelList[1]]))
        thirdDict = dict(zip(df[columnCodeList[2]], df[columnLabelList[2]]))
        forthDict = dict(zip(df[columnCodeList[3]], df[columnLabelList[3]]))
        fithDict = dict(zip(df[columnCodeList[4]], df[columnLabelList[4]]))
        return [firstDict, secondDict, thirdDict, forthDict, fithDict]
    
    elif len(columnCodeList) == 6:
        firstDict = dict(zip(df[columnCodeList[0]], df[columnLabelList[0]]))
        secondDict = dict(zip(df[columnCodeList[1]], df[columnLabelList[1]]))
        thirdDict = dict(zip(df[columnCodeList[2]], df[columnLabelList[2]]))
        forthDict = dict(zip(df[columnCodeList[3]], df[columnLabelList[3]]))
        fithDict = dict(zip(df[columnCodeList[4]], df[columnLabelList[4]]))
        sixthDict = dict(zip(df[columnCodeList[5]], df[columnLabelList[5]]))
        return [firstDict, secondDict, thirdDict, forthDict, fithDict, sixthDict]
    
def DataDict(columnCodeList, splittingMissingCombinations):
    '''
    creates a dict to pass into pd.DataFrame
    '''
    if len(columnCodeList) == 3:
        firstLabel, secondLabel, thirdLabel = columnCodeList
        data = {
                firstLabel:splittingMissingCombinations[0],
                secondLabel:splittingMissingCombinations[1],
                thirdLabel:splittingMissingCombinations[2]
                }
    
    elif len(columnCodeList) == 4:
        firstLabel, secondLabel, thirdLabel, forthLabel = columnCodeList
        data = {
                firstLabel:splittingMissingCombinations[0],
                secondLabel:splittingMissingCombinations[1],
                thirdLabel:splittingMissingCombinations[2],
                forthLabel:splittingMissingCombinations[3]
                }
    
    elif len(columnCodeList) == 5:
        firstLabel, secondLabel, thirdLabel, forthLabel, fithLabel = columnCodeList
        data = {
                firstLabel:splittingMissingCombinations[0],
                secondLabel:splittingMissingCombinations[1],
                thirdLabel:splittingMissingCombinations[2],
                forthLabel:splittingMissingCombinations[3],
                fithLabel:splittingMissingCombinations[4]
                }
    
    elif len(columnCodeList) == 6:
        firstLabel, secondLabel, thirdLabel, forthLabel, fithLabel, sixthLabel = columnCodeList
        data = {
                firstLabel:splittingMissingCombinations[0],
                secondLabel:splittingMissingCombinations[1],
                thirdLabel:splittingMissingCombinations[2],
                forthLabel:splittingMissingCombinations[3],
                fithLabel:splittingMissingCombinations[4],
                sixthLabel:splittingMissingCombinations[5]
                }
    return data
    
def ApplyingTheDicts(df, dictsToSortLabels, columnCodeList, columnLabelList):
    '''
    applys the dicts to populate the label columns
    '''
    newDF = df.copy()
    if len(dictsToSortLabels) == 3:
        firstLabel, secondLabel, thirdLabel = columnCodeList
        newDF[columnLabelList[0]] = newDF[firstLabel].apply(lambda x:dictsToSortLabels[0][x])
        newDF[columnLabelList[1]] = newDF[secondLabel].apply(lambda x:dictsToSortLabels[1][x])
        newDF[columnLabelList[2]] = newDF[thirdLabel].apply(lambda x:dictsToSortLabels[2][x])
        
    elif len(dictsToSortLabels) == 4:
        firstLabel, secondLabel, thirdLabel, forthLabel = columnCodeList
        newDF[columnLabelList[0]] = newDF[firstLabel].apply(lambda x:dictsToSortLabels[0][x])
        newDF[columnLabelList[1]] = newDF[secondLabel].apply(lambda x:dictsToSortLabels[1][x])
        newDF[columnLabelList[2]] = newDF[thirdLabel].apply(lambda x:dictsToSortLabels[2][x])
        newDF[columnLabelList[3]] = newDF[forthLabel].apply(lambda x:dictsToSortLabels[3][x])
        
    elif len(dictsToSortLabels) == 5:
        firstLabel, secondLabel, thirdLabel, forthLabel, fithLabel = columnCodeList
        newDF[columnLabelList[0]] = newDF[firstLabel].apply(lambda x:dictsToSortLabels[0][x])
        newDF[columnLabelList[1]] = newDF[secondLabel].apply(lambda x:dictsToSortLabels[1][x])
        newDF[columnLabelList[2]] = newDF[thirdLabel].apply(lambda x:dictsToSortLabels[2][x])
        newDF[columnLabelList[3]] = newDF[forthLabel].apply(lambda x:dictsToSortLabels[3][x])
        newDF[columnLabelList[4]] = newDF[fithLabel].apply(lambda x:dictsToSortLabels[4][x])
        
    elif len(dictsToSortLabels) == 6:
        firstLabel, secondLabel, thirdLabel, forthLabel, fithLabel, sixthLabel = columnCodeList
        newDF[columnLabelList[0]] = newDF[firstLabel].apply(lambda x:dictsToSortLabels[0][x])
        newDF[columnLabelList[1]] = newDF[secondLabel].apply(lambda x:dictsToSortLabels[1][x])
        newDF[columnLabelList[2]] = newDF[thirdLabel].apply(lambda x:dictsToSortLabels[2][x])
        newDF[columnLabelList[3]] = newDF[forthLabel].apply(lambda x:dictsToSortLabels[3][x])
        newDF[columnLabelList[4]] = newDF[fithLabel].apply(lambda x:dictsToSortLabels[4][x])
        newDF[columnLabelList[5]] = newDF[sixthLabel].apply(lambda x:dictsToSortLabels[5][x])
    
    return newDF
        
def ReorderingDF(newDF, originalDF, v4marker):
    '''
    checks if Data_Marking column already exists and changes name of V4 column if required
    concatenates the original df with the newDF (df of missing combinations)
    reorders the columns if required
    returns concated df
    '''
    if 'Data_Marking' in originalDF.columns:
        concatDF = pd.concat([originalDF, newDF])
    else:
        originalDF['Data_Marking'] = ''
        concatDF = pd.concat([originalDF, newDF])
        concatDF = concatDF.rename(columns = {'V4_' + str(v4marker):'V4_' + str(v4marker + 1)})
    
    #reordering columns in case data markings in wrong place
    if concatDF.columns[1] != 'Data_Marking':
        newColsOrder = [concatDF.columns[0],'Data_Marking']
        for col in concatDF.columns:
            if col not in newColsOrder:
                newColsOrder.append(col)
            
        concatDF = concatDF[newColsOrder]  
    return concatDF    
        
def AddingCombinationColumnToDF(df, columnCodeList):
    '''creates a new column which is a combination of all other code ID dimensions'''
    if len(columnCodeList) == 3:
        return df[columnCodeList[0]] + '^' + df[columnCodeList[1]] + '^' + df[columnCodeList[2]]
    
    elif len(columnCodeList) == 4:
        return df[columnCodeList[0]] + '^' + df[columnCodeList[1]] + '^' + df[columnCodeList[2]] \
                    + '^' + df[columnCodeList[3]]
    
    elif len(columnCodeList) == 5:
        return df[columnCodeList[0]] + '^' + df[columnCodeList[1]] + '^' + df[columnCodeList[2]] \
                    + '^' + df[columnCodeList[3]] + '^' + df[columnCodeList[4]]
                    
    elif len(columnCodeList) == 6:
        return df[columnCodeList[0]] + '^' + df[columnCodeList[1]] + '^' + df[columnCodeList[2]] \
                    + '^' + df[columnCodeList[3]] + '^' + df[columnCodeList[4]] \
                    + '^' + df[columnCodeList[5]]
        
def NumberOfDimensionsCheck(columnCodeList):
    '''
    code has been written to incorperate v4 files with this many dimensions
    5
    '''
    if len(columnCodeList) not in [3, 4, 5, 6]:
        raise Exception('Program not yet complete for {} dimensions'.format(len(columnCodeList)))
        
        
        
        
        