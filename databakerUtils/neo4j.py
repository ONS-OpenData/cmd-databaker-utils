import pandas as pd


# get all the codelist column headers from a v4 file
def getCodeListNamesFromV4(df):
    cols = df.columns.values
    vHeader = [x for x in cols if "v4_" in x.lower()]

    if len(vHeader) == 0:
        raise ValueError("Cannot find v4_ or V4_ header in provided csv.")
    else:
        vNum = vHeader[0].split("_")[1].strip()

    colsList = []
    for i in range(int(vNum)+1, len(cols), 2):
        codeAndLabel = {"code": cols[i], "label": cols[i + 1]}
        colsList.append(codeAndLabel)

    return colsList


# passes the name of a codelist and a list of unique codes it contains to makeCypher function
def codeListFromDimension(dimensionsPair, df):
    temp = pd.DataFrame()
    temp[dimensionsPair["code"]] = df[dimensionsPair["code"]]
    temp[dimensionsPair["label"]] = df[dimensionsPair["label"]]
    temp = temp.drop_duplicates()

    allCodes = temp[dimensionsPair["code"]].unique()
    allLabels = temp[dimensionsPair["label"]].unique()

    if len(allCodes) != len(allLabels):
        duplicates(temp)
        raise ValueError(
            "Aborting and generating info on code mismatches as nonSpecificDefinitions.txt, the number of unqiue codes is not equal to the number of unique labels for dimension: " +
            dimensionsPair["code"])

    codes = []
    for i in range(0, len(allCodes)):
        codes.append({"code": allCodes[i], "label": allLabels[i]})

    makeCypher(dimensionsPair, codes)


# Creates the required cypher as a lists of cypher lines. Passes those lines to the cypherWriter
def makeCypher(dimensionPair, codes):
    linesToWrite = []

    linesToWrite.append(
        "CREATE CONSTRAINT ON (n:`_code_{c}`) ASSERT n.value IS UNIQUE;".format(c=str(dimensionPair["code"])))

    linesToWrite.append("CREATE (node:`_code_list`:`_code_list_" + str(dimensionPair["code"]) + "` { label:'" + str(
        dimensionPair["label"]) + "', edition:'one-off' });")

    for code in codes:
        linesToWrite.append(
            "MERGE (node:`_code`:`_code_" + str(dimensionPair["code"]) + "` { value:'" + str(code["code"]) + "' });")

        # Inconsistant use of ' and " within labels. Force all to quoting as ' else Neo issues
        lab = str(code["label"]).replace("\"", "'").replace(".0", "")

        linesToWrite.append(
            "MATCH (parent:`_code_list`:`_code_list_" + str(dimensionPair["code"]) + "`),(node:`_code`" +
            ":`_code_" + str(dimensionPair["code"]) + "` { value:'" + str(
                code["code"]) + "' }) MERGE (node)-[:usedBy { label:\"" + lab + "\"}]->(parent);")

    writeCypher(linesToWrite, dimensionPair)


# Write the cypher for a codelist to a cypher file
def writeCypher(linesToWrite, dimensionPair):
    with open("CL_{c}.cypher".format(c=dimensionPair["code"]), "w") as f:
        for line in linesToWrite:
            f.write(str(line) + "\n")


# a function to create meaningful feedback when a code or label has been used multiple times to represent different concepts
def duplicates(df):
    cols = df.columns.values
    codeCol = cols[0]
    labelsCol = cols[1]

    hasNonSpecificCodes = []
    for code in df[codeCol].unique():

        tempDf = df.copy()

        # TODO - must be a less hacky way of handling this
        try:
            tempDf = tempDf[tempDf[codeCol] == code]
        except:
            tempDf = tempDf[tempDf[codeCol] == str(code)]

        if len(tempDf) > 1:
            for label in tempDf[labelsCol]:
                hasNonSpecificCodes.append(str(code) + " || " + str(label) + "\n")
            hasNonSpecificCodes.append("\n")

    hasNonSpecificLabels = []
    for label in df[labelsCol].unique():

        tempDf = df.copy()
        tempDf = tempDf[tempDf[labelsCol] == code]
        if len(tempDf) > 1:
            for label in tempDf[codeCol]:
                hasNonSpecificCodes.append(str(label) + " || " + str(code) + "\n")
            hasNonSpecificCodes.append("\n")

    with open("nonSpecificDefinitions.txt", "w") as f:

        if len(hasNonSpecificCodes) != 0:
            f.write("ERROR - the following codes are represented by more than one label\n")
            f.write("Codelist: " + str(codeCol) + "\n")
            f.write("------------------------------------------------------------------\n\n")
            f.writelines(hasNonSpecificCodes)


# Wrapper function, uses all of the above
"""
has type issues - disabling for now
def codelistsAsCypherFromV4(csv):

    df = pd.read_csv(csv)

    # creates a list of codesLabel dicts. i.e [{"label":"uk-only", "code":"K02000001"}, etc....]
    dimensionsPairs = getCodeListNamesFromV4(df)

    for dimensionPair in dimensionsPairs:
        codeListFromDimension(dimensionPair, df)
"""

# Main function, uses all of the above
# {"code": <CODE_COL_NAME>, "label": <LABEL_COL_NAME>}
def codelistCypherFromDimension(df, dimensionPair):
    codeListFromDimension(dimensionPair, df)
