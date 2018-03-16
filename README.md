
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

you -MUST- be using the ConversionSegment().topandas() functionality for this to work.


import with:

`from databakerUtils.writers import v4Writer`


then replace the line:

`writetechnicalCSV("Output.csv", conversionsegments)`

with:

`v4Writer("Output.csv", conversionsegments)`

where "v4" is the output structure you want.

you can also use the asFrame keyword to write the v4 to a new dataframe if further processing is required).

`v4Writer("Output.csv", conversionsegments, asFrame=True)`





