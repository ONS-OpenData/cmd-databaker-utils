
"""
Useful functions when creating a transform
"""

import requests
import pandas as pd
import numpy as np


def v4Integers(value):
    '''
    treats all values in v4 column as strings
    returns integers instead of floats for numbers ending in '.0'
    '''
    newValue = str(value)
    if newValue.endswith('.0'):
        newValue = newValue[:-2]
    return newValue


def sparsity(DataFrame, isCSV = False, showVars = False):
    '''
    Investigating sparsity
    Completeness shown as a percentage
    Pass isCSV=True if the data is a csv file and pass DataFrame=input_file (string)
    Can also show which values for each dimension have sparsity ...> showVars=True
    '''
    
    if isCSV==True:
        df = pd.read_csv(DataFrame) 
    else: df = DataFrame    
    
    numberOfObservations = df.index.size
    
    #creates a list of column names and then filters down to list of labels (not the codelists)
    colNames, labelList = [], []
    v4marker = int(df.columns[0][-1])
    for i in range(v4marker + 1, len(df.columns)):
        colNames.append(df[df.columns[i]].name)
    for i in range(int(len(colNames)/2)):
        labelList.append(colNames[2 * i + 1])
    
    possibleNumberOfObservations, groupList=[], []
    #creates a list containing number of unique values for each dimension
    #creates a list of pd.Series for each dimension and shows the number of observations /
    #for each unique value (label) in that dimension
    for col in labelList:
         possibleNumberOfObservations.append(len(df[col].unique())) 
         grouped = df.groupby(col)
         groupList.append(grouped.size())
    
    #Total possible number of observations if dataset 100% complete    
    possibleNumberOfObservations = np.prod(possibleNumberOfObservations)
    
    #Calculates completeness of data
    sparsityPercent = numberOfObservations/possibleNumberOfObservations * 100
    
    print("The dataset is {:.2f}% complete".format(sparsityPercent))
    
    #Shows which values for each dimension are not 100% ie have some sparsity
    if showVars == True:
        for i in range(0, len(labelList)):
            completeData = possibleNumberOfObservations/len(groupList[i])
            for j in range(len(groupList[i])):
                if groupList[i].iloc[j] != completeData:
                    print("{} has some sparsity within {}".format(groupList[i].index[j], labelList[i]))
    #if sparsity isn't 100%, will show if a label-code pair doesn't have 
    #matching unique number of variables 
    #useful for when sparsity is greater than 100%
    #will then calculate the sparsity based on code rather than labels (which often have dupkicates)               
    if sparsityPercent != 100:
        codeList = []
        for i in range(int(len(colNames)/2)):
            codeList.append(colNames[2 * i])
        for i in range(len(codeList)):
            if df[codeList[i]].unique().size != df[labelList[i]].unique().size:
                print("\n{} and {} have different lengths of unique values.."\
                      .format(codeList[i], labelList[i]))
        possibleNumberOfObservations =[]
        for col in codeList:
            possibleNumberOfObservations.append(len(df[col].unique())) 
        possibleNumberOfObservations = np.prod(possibleNumberOfObservations)
        sparsityPercent = numberOfObservations/possibleNumberOfObservations * 100
        print("\nThe dataset is {:.2f}% complete according to codes".format(sparsityPercent))

        
    
def CodelistCheckFromURL(df, url):   
    '''
    Check to see if the codes & labels match the codelist in the API (dev)
    Pass the URL of the codelist and the dataframe
    (The codelist name/label will be extracted from the URL)
    '''
    import requests
    #quick test to make sure codelist has been imported to api
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception('url - "{}" is not returning a 200 response'.format(url))
    
    #find out label of the codelist
    r = requests.get('/'.join(url.split('/')[:-2]))
    myDict = r.json()
    codelistLabelName = myDict['items'][0]['label']
    
    #find out codelist name
    codelistName = url.split('/')[5]
    
    #codelist id's and labels into a dict
    r = requests.get(url)
    wholeDict = r.json()
    myDict = {}
    
    for item in wholeDict['items']:
            myDict.update({item['code']:item['label']}) 
    
    if codelistName not in df.columns:
        raise Exception('''
Dataframe does not have columns that match this codelist
{}
                        '''.format(codelistName))
            
    #find missing codes
    missingCodes = []
    for code in df[codelistName].unique():
        if code not in myDict.keys():
            missingCodes.append(code)
            
    if len(missingCodes) == 0:
        print('All codes match the API')
    elif len(missingCodes) == 1:
        print('1 code does not match the API')
    else:
        print('{} codes do not match the API'.format(len(missingCodes)))
     
    #find missing labels
    missingLabels = []
    codelistName_index = list(df.columns).index(codelistName)
    codelistLabelName = list(df.columns)[codelistName_index + 1]
    for label in df[codelistLabelName].unique():
        if label not in myDict.values():
            missingLabels.append(label)
            
    if len(missingLabels) == 0:
        print('All labels match the API')
    elif len(missingLabels) == 1:
        print('1 label does not match the API')
    else:
        print('{} labels do not match the API'.format(len(missingLabels)))
        
    #showing any missing codes/labels
    if len(missingCodes) != 0 or len(missingLabels) != 0:
        showMissingValues = input('Would you like to see the incorrect codes/labels? [y/n]: ')
        if showMissingValues == 'y':
            if len(missingCodes) != 0:
                print('"Codes"\n')
                for code in missingCodes:
                    print(code)
            if len(missingLabels) != 0:
                print('\n"Labels"\n')
                for label in missingLabels:
                    print(label)
                    
                    
def ColumnsToIgnore(columnCodeList, columnsToIgnore):
    '''
    Takes in columnCodeList (df.columns) and some columns to ignore/remove
    Returns new list of columns
    '''
    if type(columnsToIgnore) != list:
        raise Exception('Columns that you are ignoring need to be in a list')
    newColumns = []
    for column in columnCodeList:
        if column not in columnsToIgnore:
            newColumns.append(column)
    return newColumns


def AllCodelistCheck(df, columnsToIgnore=None, useDev=True):
    '''
    uses CodelistCheckFromURL() to check all codelists in the v4 file against the api (cmd-dev or beta)
    pass columnsToIgnore as a list of codelists to be ignored
    pass useDev = False to check against beta api
    useful if you know the code list already exists and you just want to check labels and codes
    '''
    ObsChecker(df)  #check observations for any incorrect
    if useDev == True:
        devOrBeta = 'develop.onsdigital.co.uk'
    else:
        devOrBeta = 'beta.ons.gov.uk'
    v4marker = int(df.columns[0][-1])   #only interested in codelist columns
    columnList = list(df.columns)
    columnCodeList = columnList[v4marker + 1::2]
    if columnsToIgnore != None:
        columnCodeList = ColumnsToIgnore(columnCodeList, columnsToIgnore)
    for col in columnCodeList:
        url = 'https://api.' + devOrBeta + '/v1/code-lists/' + col + '/editions/one-off/codes'
        if requests.get(url).status_code != 200:
            print('{} does not appear to be in the api'.format(url.split('/')[5]))
            continue
        print('\t"{}"'.format(col))
        CodelistCheckFromURL(df, url)


def ObsChecker(v4):
    '''
    Checks the observations column in a v4 
    to make sure no data markings are left in the wrong column
    returns nothing if all okay
    '''
    df = v4.copy()
    obsColumn = df.columns[0]
    df[obsColumn] = df[obsColumn].apply(v4Integers)
    
    missingDM = False
    dataMarkings = []
    for ob in df[obsColumn].unique():
        try:
            float(ob)
        except ValueError as e:
            dataMarkings.append(ob)
            missingDM = True
    if missingDM:
        print('There are data markings in {}'.format(obsColumn))
        print(dataMarkings)

    
