
# databakerUtils

Library of ONS centric add-on functionality for databaker.


## install

You MUST first have databaker and all it's dependancies installed.
YOU MUST have git access (so have installed Git for Windows and be using the GIT command line) if you're on a windows machine.

then:

`pip install git+https://github.com/ONS-OpenData/cmd-databaker-utils.git`

`pip install requests`

## Usage

Depends on functionality. Listed below.

---

## 1. Utility - Create V4 files

Used to output a databaker generated pandas dataframe to a v4 structured csv. 

you -MUST- be using the ConversionSegment().topandas() functionality for this to work. And if conversionSegments is a list you MUST concatenate to a single dataframe first, i.e `conversionSegments = pd.concat([conversionSegments])`


import with:

`from databakerUtils.writers import v4ToDataFrame, v4ToCSV`


then replace the line:

`writetechnicalCSV("Output.csv", conversionSegments)`


with either:

`v4Writer("Output.csv", conversionSegments)` to write a v4 structured CSV.

or

`df = v4ToDataFrame(conversionSegments)` to return a v4 structured dataframe (df) for further processing.


#### 1.1 Creating Observation Level Data

You can also specify dimensions to become observation level data (the additional columns denoted by the number in column A) by passing in an `obsData=` keyword list.

Example using v4Writer - assuming you want "Measure" as an additional column.

`v4Writer("Output.csv", conversionSegments, obsData=["Measure")`

the `obsData=` keyword also works for v4ToDataFrame

---

## 2. Utility - Create Neo4J Graph Codelists from V4 files

Used to generate .cypher files for loading codelists into a Neo4J graph database.

When given the column name for a codelist and its associated labels column, it will generate a cypher file to generate that codelist.

import with:

`from databakerUtils.neo4j import codelistCypherFromDimension`

use within a python script as follows.

```
instructions = {
"code":<NAME OF CODELIST COLUMN>,
"label":<NAME OF LABEL COLUMN>,
"edition":<EDITION>
}
codelistCypherFromDimension(<DATAFRAME>, instructions)

```


---

## 3. Utility - Codelist API

Some helper functions for working with codes and codelists that already exist on the api

import with:

`from databakerUtils.api import findCodelists, getAllCodes, getAllLabels, getCodeLookup, getLabelLookup`


### Scanning the codelist api:

NOTE - `list(df[" <V4_COL_HEADER> "].unique())` returns a list of unique codes from a dataframe column.

```
checkDict = {
  "geography":list(df["Geography_codelist"].unique()),
  "time":list(df["Time_codelist"].unique())
}
results = findCodelistByCodes(checkDict) 

# note - you can also 'findCodelistByLabels'

```

The result item will contain the best matching codelist from the api, or will be blank (in which case no codes from the api, match any codes in the lists provided".

Additional helper functions:

* `data = getAllCodes(<URL>)`         # returns a list
* `data = getAllLabels(<URL>)`        # returns a list
* `data = getCodeLookup(<URL>)`       # returns a dictionary
* `data = getLabelLookup(<URL>)`      # returns a dictionary

A <URL> in this context is a code-list api endpoint ending in /codes.
example: https://api.beta.ons.gov.uk/v1/code-lists/cpi1dim1aggid/editions/one-off/codes
