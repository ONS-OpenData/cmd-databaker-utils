
"""
Simple example writer that just prints all the dataframes
"""

def run(OutputName, dfList):

    # Listify if needed
    if not isinstance(dfList, list):
        dfList = [dfList]

    for dataframe in dfList:
      print(dataframe)