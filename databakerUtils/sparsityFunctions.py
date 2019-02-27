import pandas as pd
import datetime

def SparsityFiller(csv, DataMarker = '.'):
    '''
    Finds all the missing data (from sparsity) and writes a new file with the complete data
    Complete data means showing data markings
    pass DataMarker = '...' to chose the data marker
    '''
    
    currentTime = datetime.datetime.now()
    df = pd.read_csv(csv, dtype = str)
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
    
    #list of all combinations to fill a dict
    listsToFillDataDict = ListsToFillDataDict(uniqueListOfCodesInColumns)
    
    #dicts to fill in labels
    dictsToSortLabels = DictsToSortLabels(df, columnLabelList, columnCodeList)
    
    #creating a new dataframe
    data = DataDict(columnCodeList, listsToFillDataDict)
    newDF = pd.DataFrame(data, columns = columnList)
    newDF['Data_Marking'] = DataMarker
    
    #applying the dicts
    newDF = ApplyingTheDicts(newDF, dictsToSortLabels, columnCodeList, columnLabelList)
    
    #concating the df's
    concatDF = ReorderingDF(newDF, df, v4marker)
    
    #removing duplicates
    indexToKeep = IndexOfDuplicates(concatDF, columnCodeList)
    concatDF = concatDF.loc[indexToKeep]
    
    concatDF.to_csv(outputFile, index = False)
    
    print('SparsityFiller took {}'.format(datetime.datetime.now() - currentTime))


def UniqueListOfCodesInColumns(df, columnCodeList):
    '''
    columnCodeList is a list of column code ID names
    returns a list of lists of unique values for each dimension
    '''
    #all unique values from each code column
    if len(columnCodeList) == 3:
        firstList = list(df[columnCodeList[0]].unique())
        secondList = list(df[columnCodeList[1]].unique())
        thirdList = list(df[columnCodeList[2]].unique())
        allList = [firstList, secondList, thirdList]
        
    elif len(columnCodeList) == 4:
        firstList = list(df[columnCodeList[0]].unique())
        secondList = list(df[columnCodeList[1]].unique())
        thirdList = list(df[columnCodeList[2]].unique())
        forthList = list(df[columnCodeList[3]].unique())
        allList = [firstList, secondList, thirdList, forthList]
        
        
    elif len(columnCodeList) == 5:
        firstList = list(df[columnCodeList[0]].unique())
        secondList = list(df[columnCodeList[1]].unique())
        thirdList = list(df[columnCodeList[2]].unique())
        forthList = list(df[columnCodeList[3]].unique())
        fithList = list(df[columnCodeList[4]].unique())
        allList = [firstList, secondList, thirdList, forthList, fithList]
        
    elif len(columnCodeList) == 6:
        firstList = list(df[columnCodeList[0]].unique())
        secondList = list(df[columnCodeList[1]].unique())
        thirdList = list(df[columnCodeList[2]].unique())
        forthList = list(df[columnCodeList[3]].unique())
        fithList = list(df[columnCodeList[4]].unique())
        sixthList = list(df[columnCodeList[5]].unique())
        allList = [firstList, secondList, thirdList, forthList, fithList, sixthList]
    
    return allList
    
    
def ListsToFillDataDict(uniqueListOfCodesInColumns):
    '''
    returns a list of lists to be used to fill a dict
    each list will be as long as the unsparse version
    '''
    if len(uniqueListOfCodesInColumns) == 3:
        firstList, secondList, thirdList = [], [], []
        for first in uniqueListOfCodesInColumns[0]:
            for second in uniqueListOfCodesInColumns[1]:
                for third in uniqueListOfCodesInColumns[2]:
                    firstList.append(first)
                    secondList.append(second)
                    thirdList.append(third)
        allList = [firstList, secondList, thirdList]
        
    elif len(uniqueListOfCodesInColumns) == 4:
        firstList, secondList, thirdList, forthList = [], [], [], []
        for first in uniqueListOfCodesInColumns[0]:
            for second in uniqueListOfCodesInColumns[1]:
                for third in uniqueListOfCodesInColumns[2]:
                    for forth in uniqueListOfCodesInColumns[3]:
                        firstList.append(first)
                        secondList.append(second)
                        thirdList.append(third)
                        forthList.append(forth)
        allList = [firstList, secondList, thirdList, forthList]
        
    elif len(uniqueListOfCodesInColumns) == 5:
        firstList, secondList, thirdList, forthList, fithList = [], [], [], [], []
        for first in uniqueListOfCodesInColumns[0]:
            for second in uniqueListOfCodesInColumns[1]:
                for third in uniqueListOfCodesInColumns[2]:
                    for forth in uniqueListOfCodesInColumns[3]:
                        for fith in uniqueListOfCodesInColumns[4]:
                            firstList.append(first)
                            secondList.append(second)
                            thirdList.append(third)
                            forthList.append(forth)
                            fithList.append(fith)
        allList = [firstList, secondList, thirdList, forthList, fithList]
    
    elif len(uniqueListOfCodesInColumns) == 6:
        firstList, secondList, thirdList, forthList, fithList, sixthList = [], [], [], [], [], []
        for first in uniqueListOfCodesInColumns[0]:
            for second in uniqueListOfCodesInColumns[1]:
                for third in uniqueListOfCodesInColumns[2]:
                    for forth in uniqueListOfCodesInColumns[3]:
                        for fith in uniqueListOfCodesInColumns[4]:
                            for sixth in uniqueListOfCodesInColumns[5]:
                                firstList.append(first)
                                secondList.append(second)
                                thirdList.append(third)
                                forthList.append(forth)
                                fithList.append(fith)
                                sixthList.append(sixth)
        allList = [firstList, secondList, thirdList, forthList, fithList, sixthList]
    
    return allList


def DataDict(columnCodeList, listsToFillDataDict):
    '''
    Creates a dict to fill a dataframe
    '''
    if len(columnCodeList) == 3:
        data = {
                columnCodeList[0]:listsToFillDataDict[0],
                columnCodeList[1]:listsToFillDataDict[1],
                columnCodeList[2]:listsToFillDataDict[2]
                }
    elif len(columnCodeList) == 4:
        data = {
                columnCodeList[0]:listsToFillDataDict[0],
                columnCodeList[1]:listsToFillDataDict[1],
                columnCodeList[2]:listsToFillDataDict[2],
                columnCodeList[3]:listsToFillDataDict[3]
                }
    elif len(columnCodeList) == 5:
        data = {
                columnCodeList[0]:listsToFillDataDict[0],
                columnCodeList[1]:listsToFillDataDict[1],
                columnCodeList[2]:listsToFillDataDict[2],
                columnCodeList[3]:listsToFillDataDict[3],
                columnCodeList[4]:listsToFillDataDict[4]
                }
    elif len(columnCodeList) == 6:
        data = {
                columnCodeList[0]:listsToFillDataDict[0],
                columnCodeList[1]:listsToFillDataDict[1],
                columnCodeList[2]:listsToFillDataDict[2],
                columnCodeList[3]:listsToFillDataDict[3],
                columnCodeList[4]:listsToFillDataDict[4],
                columnCodeList[5]:listsToFillDataDict[5]
                }
    
    return data


def DictsToSortLabels(df, columnLabelList, columnCodeList):
    '''
    creates a list of dicts that will be used to fill in the labels 
    (using the existing data from the v4)
    '''
    if len(columnCodeList) == 3:
        firstDict = dict(zip(df[columnCodeList[0]], df[columnLabelList[0]]))
        secondDict = dict(zip(df[columnCodeList[1]], df[columnLabelList[1]]))
        thirdDict = dict(zip(df[columnCodeList[2]], df[columnLabelList[2]]))
        allList = [firstDict, secondDict, thirdDict]
    
    elif len(columnCodeList) == 4:
        firstDict = dict(zip(df[columnCodeList[0]], df[columnLabelList[0]]))
        secondDict = dict(zip(df[columnCodeList[1]], df[columnLabelList[1]]))
        thirdDict = dict(zip(df[columnCodeList[2]], df[columnLabelList[2]]))
        forthDict = dict(zip(df[columnCodeList[3]], df[columnLabelList[3]]))
        allList = [firstDict, secondDict, thirdDict, forthDict]
        
    elif len(columnCodeList) == 5:
        firstDict = dict(zip(df[columnCodeList[0]], df[columnLabelList[0]]))
        secondDict = dict(zip(df[columnCodeList[1]], df[columnLabelList[1]]))
        thirdDict = dict(zip(df[columnCodeList[2]], df[columnLabelList[2]]))
        forthDict = dict(zip(df[columnCodeList[3]], df[columnLabelList[3]]))
        fithDict = dict(zip(df[columnCodeList[4]], df[columnLabelList[4]]))
        allList = [firstDict, secondDict, thirdDict, forthDict, fithDict]
        
    elif len(columnCodeList) == 6:
        firstDict = dict(zip(df[columnCodeList[0]], df[columnLabelList[0]]))
        secondDict = dict(zip(df[columnCodeList[1]], df[columnLabelList[1]]))
        thirdDict = dict(zip(df[columnCodeList[2]], df[columnLabelList[2]]))
        forthDict = dict(zip(df[columnCodeList[3]], df[columnLabelList[3]]))
        fithDict = dict(zip(df[columnCodeList[4]], df[columnLabelList[4]]))
        sixthDict = dict(zip(df[columnCodeList[5]], df[columnLabelList[5]]))
        allList = [firstDict, secondDict, thirdDict, forthDict, fithDict, sixthDict]
        
    return allList


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


def ReorderingDF(newDF, df, v4marker):
    '''
    checks if Data_Marking column already exists and changes name of V4 column if required
    concatenates the original df with the newDF (df of missing combinations)
    reorders the columns if required
    returns concated df
    '''
    originalDF = df.copy()
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
    concatDF = concatDF.reset_index(drop = True)
    return concatDF  
  

def IndexOfDuplicates(concatDF, columnCodeList):
    '''
    returns a list of all duplicate lines of the concated df
    ignoring observations and data markings
    '''
    newDF = concatDF.copy()
    newDF = newDF.reset_index(drop = True)
    newDF = newDF[columnCodeList]
    newDF = newDF.drop_duplicates()
    indexToKeep = list(newDF.index)
    return indexToKeep
    

def NumberOfDimensionsCheck(columnCodeList):
    '''
    code has been written to incorperate v4 files with this many dimensions
    '''
    if len(columnCodeList) not in [3, 4, 5, 6]:
        raise Exception('Program not yet complete for {} dimensions'.format(len(columnCodeList)))
