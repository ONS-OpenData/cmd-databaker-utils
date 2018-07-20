
# databakerUtils

Library of ONS centric add-on functionality for databaker.


## install

You MUST first have databaker and all it's dependancies installed, then:

`pip install git+https://github.com/ONS-OpenData/databakerUtils.git`

## Usage

Depends on functionality. Listed below.

---

## Utility - V4Writer

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





