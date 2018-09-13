import pandas as pd


# Validate the provded arguments
def validate(df, dimensionPair):

    # Validate input
    if "code" not in dimensionPair:
        raise ValueError("Aborting. Requires a dictionary with 'code' and 'label' keys as argument 2.")

    if "label" not in dimensionPair:
        raise ValueError("Aborting. Requires a dictionary with 'code' and 'label' keys as argument 2.")

    if "edition" not in dimensionPair:
        raise ValueError("Aborting. Requires a dictionary with 'code' and 'label' keys as argument 2.")

    if type(df) != pd.DataFrame:
        raise ValueError("Aborting. Requires a pandas dictionary as argument 1.")


# passes the name of a codelist and a list of unique codes it contains to makeCypher function
# dimensionPair example = {"code": <CODE_COL_NAME>, "label": <LABEL_COL_NAME>}
def codelistCypherFromDimension(df, instructions):

    validate(df, instructions)

    temp = pd.DataFrame()
    temp[instructions["code"]] = df[instructions["code"]]
    temp[instructions["label"]] = df[instructions["label"]]
    temp = temp.drop_duplicates()

    allCodes = temp[instructions["code"]].unique()
    allLabels = temp[instructions["label"]].unique()

    if len(allCodes) != len(allLabels):
        duplicates(temp)
        raise ValueError(
            "Aborting and generating info on code mismatches as nonSpecificDefinitions.txt, the number of unqiue codes is not equal to the number of unique labels for dimension: " +
            instructions["code"])

    codes = []
    for i in range(0, len(allCodes)):
        codes.append({"code": allCodes[i], "label": allLabels[i]})

    makeCypher(instructions, codes, instructions["edition"])


def useSingleQuote(code, label):

    if "'" not in code and "'" not in label:
        return True
    else:
        return False


# Creates the required cypher as a lists of cypher lines. Passes those lines to the cypherWriter
def makeCypher(instructions, codes, edition):
    linesToWrite = []

    linesToWrite.append(
        "CREATE CONSTRAINT ON (n:`_code_{c}`) ASSERT n.value IS UNIQUE;".format(c=str(instructions["code"])))

    linesToWrite.append("CREATE (node:`_code_list`:`_code_list_" + str(instructions["code"]) + "` { label:'" + str(
        instructions["label"]) + "'edition':'" + edition + "' });")

    for code in codes:

        # always use single quotes - unless they're in use in the code or label value
        if useSingleQuote(code["code"], code["label"]):

            linesToWrite.append(
                'MERGE (node:`_code`:`_code_' + str(instructions["code"]) + '` { value:"' + str(code["code"]) + '" });')

            linesToWrite.append(
                'MATCH (parent:`_code_list`:`_code_list_' + str(instructions["code"]) + '`),(node:`_code`' +
                ':`_code_' + str(instructions["code"]) + '` { value:"' +
                str(code["code"]) + '" }) MERGE (node)-[:usedBy { label:"' + code["label"] + '"}]->(parent);')
        else:

            linesToWrite.append(
                "MERGE (node:`_code`:`_code_" + str(instructions["code"]) + "` { value:'" + str(code["code"]) + "' });")

            linesToWrite.append(
                "MATCH (parent:`_code_list`:`_code_list_" + str(instructions["code"]) + "`),(node:`_code`" +
                ":`_code_" + str(instructions["code"]) + "` { value:'" +
                str(code["code"]) + "' }) MERGE (node)-[:usedBy { label:'" + code["label"] + "'}]->(parent);")


    writeCypher(linesToWrite, instructions)


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
        tempDf = tempDf[tempDf[labelsCol] == label]
        if len(tempDf) > 1:
            for label in tempDf[codeCol]:
                hasNonSpecificLabels.append(str(label) + " || " + str(code) + "\n")
            hasNonSpecificCodes.append("\n")

    with open("nonSpecificDefinitions_{c}.txt".format(codeCol), "w") as f:

        if len(hasNonSpecificCodes) != 0:
            f.write("ERROR - the following codes are represented by more than one label\n")
            f.write("Codelist: " + str(codeCol) + "\n")
            f.write("------------------------------------------------------------------\n\n")
            f.writelines(hasNonSpecificCodes)

