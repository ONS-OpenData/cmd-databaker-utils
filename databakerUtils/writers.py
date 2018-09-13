import pandas as pd

"""
A sequence of pandas instructions to turn a pandas dataframe created by databaker
into a CSV strutured to the ONS digital publishing v4 specification.

We're going to drop old columns as we add new ones, to minimise memory footprint.
"""



# Depreciated. Just wrapping newer function for backwards compatibility
def v4Writer(OutputName, df, asFrame=False):

    obsData = ['Confidence Interval', 'CV', 'CDID']

    if not asFrame:
        v4ToCSV(OutputName, df, obsData)
    else:
        return v4ToDataFrame(df, obsData)


# Writes a v4 file to csv
def v4ToCSV(OutputName, df, obsData=[]):

    for old in obsData:
        if old not in df.columns.values:
            raise ValueError("Aborting. Column {c} specified as observation level data, but no such column present in dataset.".format(c=old))

    v4 = v4ToDataFrame(df, obsData=obsData)
    writeCSV(OutputName, v4)



# Returns a dataframe in v4 structure
def v4ToDataFrame(df, obsData=[]):

    for old in obsData:
        if old not in df.columns.values:
            raise ValueError("Aborting. Column {c} specified as observation level data, but no such column present in dataset.".format(c=old))

    # build our new dataframe
    newDf = pd.DataFrame()

    obsColCount = len(obsData)

    if "DATAMARKER" in df.columns.values:
        obsColCount += 1

    # build our new dataframe
    newDf['V4_' + str(obsColCount)] = df['OBS']
    df = df.drop('OBS', axis=1)

    if "DATAMARKER" in df.columns.values:
        newDf['Data_Marking'] = df['DATAMARKER']
        df = df.drop('DATAMARKER', axis=1)

    # Add columns of observation level data
    # iterate and output prior to time
    for obld in obsData:
        if obld in df.columns.values:
            newDf[obld] = df[obld]
            df = df.drop(obld, axis=1)

    # time unit
    newDf['Time_codelist'] = df['TIMEUNIT']
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

        return newDf


def writeCSV(OutputName, df):
    df.to_csv(OutputName, encoding='utf-8', index=False)
    print('V4 file written as:' + OutputName)

