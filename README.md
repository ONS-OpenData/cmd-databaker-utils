
# databakerUtils

Library of ONS centric add-on functionality for databaker.


## install

You MUST first have databaker and all it's dependancies installed.
YOU MUST have git access (so have installed Git for Windows and be using the GIT command line) if you're on a windows machine.

then:

`pip install git+https://github.com/ONS-OpenData/cmd-databaker-utils.git`

## Usage

Depends on functionality. Listed below.

---

## Utility - Create V4 files

Used to output a databaker generated pandas dataframe to a v4 structured csv. 

you -MUST- be using the ConversionSegment().topandas() functionality for this to work. And if conversionSegments is a list you need need to conctenate to a single dataframe first, i.e `conversionSegments = pd.concat([conversionSegments])`


import with:

`from databakerUtils.writers import v4Writer`


then replace the line:

`writetechnicalCSV("Output.csv", conversionSegments)`


with:

`v4Writer("Output.csv", conversionSegments)`


you can also use the asFrame keyword to write the v4 to a new dataframe if further processing is required).

`myNewDataFrame = v4Writer("Output.csv", conversionSegments, asFrame=True)`


---

## Utility - Create Neo4J Graph Codelists from V4 files

Used to generate .cypher files for loading codelists into a Neo4J graph database.

When ran on a v4 style csv it will generated a cypher file for each dimension in that v4 file.

IMPORTANT  - there's no automatic checking against the API so it will create ALL codelists, even ones that
already exist with the graph (if unsure, use the cmd api to see if a codelist already exist: https://api.beta.ons.gov.uk/v1/code-lists).


import with:

`from databakerUtils.neo4j import codelistsAsCypherFromV4`

use within a python script with:

`codelistsAsCypherFromV4(<pathTOCSV>)`



