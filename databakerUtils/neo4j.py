import pandas as pd


# passes the name of a codelist and a list of unique codes it contains to makeCypher function
def codeListFromDimension(df, dimensionsPair):
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


def useSingleQuote(code, label):

    if "'" not in code and "'" not in label:
        return True
    else:
        return False


# Creates the required cypher as a lists of cypher lines. Passes those lines to the cypherWriter
def makeCypher(dimensionPair, codes):
    linesToWrite = []

    linesToWrite.append(
        "CREATE CONSTRAINT ON (n:`_code_{c}`) ASSERT n.value IS UNIQUE;".format(c=str(dimensionPair["code"])))

    linesToWrite.append("CREATE (node:`_code_list`:`_code_list_" + str(dimensionPair["code"]) + "` { label:'" + str(
        dimensionPair["label"]) + "', edition:'one-off' });")

    for code in codes:

        # always use single quotes - unless they're in use in the code or label value
        if useSingleQuote(code["code"], code["label"]):

            linesToWrite.append(
                'MERGE (node:`_code`:`_code_' + str(dimensionPair["code"]) + '` { value:"' + str(code["code"]) + '" });')

            linesToWrite.append(
                'MATCH (parent:`_code_list`:`_code_list_' + str(dimensionPair["code"]) + '`),(node:`_code`' +
                ':`_code_' + str(dimensionPair["code"]) + '` { value:"' +
                str(code["code"]) + '" }) MERGE (node)-[:usedBy { label:"' + code["label"] + '"}]->(parent);')
        else:

            linesToWrite.append(
                "MERGE (node:`_code`:`_code_" + str(dimensionPair["code"]) + "` { value:'" + str(code["code"]) + "' });")

            linesToWrite.append(
                "MATCH (parent:`_code_list`:`_code_list_" + str(dimensionPair["code"]) + "`),(node:`_code`" +
                ":`_code_" + str(dimensionPair["code"]) + "` { value:'" +
                str(code["code"]) + "' }) MERGE (node)-[:usedBy { label:'" + code["label"] + "'}]->(parent);")


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


# Main function, uses all of the above
# {"code": <CODE_COL_NAME>, "label": <LABEL_COL_NAME>}
def codelistCypherFromDimension(df, dimensionPair):
    codeListFromDimension(df, dimensionPair)
