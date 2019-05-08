import pandas as pd

"""
A sequence of pandas instructions to turn a pandas dataframe created by databaker
into a CSV strutured to the ONS digital publishing v4 specification.

We're going to drop old columns as we add new ones, to minimise memory footprint.
"""

def v4Writer(OutputName, df, asFrame=False):

    print('Extracting data structured as v4.')

    obsLevelData = ['Confidence Interval', 'CV', 'CDID', 'DATAMARKER']

    # additional column count
    addColCount = len([x for x in df.columns.values if x in obsLevelData])

    if "DATAMARKER" in df.columns.values:
        hasDataMarker = True
    else:
        hasDataMarker = False

    # Lets build our new dataframe
    newDf = pd.DataFrame()
    newDf['V4_' + str(addColCount)] = df['OBS']
    df = df.drop('OBS', axis=1)

    if hasDataMarker:
        newDf['Data_Marking'] = df['DATAMARKER']
        df = df.drop('DATAMARKER', axis=1)

    # Add quality measures
    # iterate and look for column headers to output prior to time
    for qm in obsLevelData:
        if qm in df.columns.values:
            newDf[qm] = df[qm]
            df = df.drop(qm, axis=1)

    # time unit - no longer needed
    newDf['Time_codelist'] = df['TIME']
    df = df.drop('TIMEUNIT', axis=1)

    # time
    newDf['Time'] = df['TIME']
    df = df.drop('TIME', axis=1)

    # Geography
    newDf["Geography_codelist"] = df["GEOG"]
    newDf["Geography"] = ''
    df = df.drop("GEOG", axis=1)

    for topic in df.columns.values:
        newDf[topic + '_codelist'] = ''
        newDf[topic] = df[topic]

    # Optional return as dataframe, need keyword argument: asFrame=True
    if asFrame:
        return newDf

    newDf.to_csv(OutputName, encoding='utf-8', index=False)
    print('V4 file written as:' + OutputName)

