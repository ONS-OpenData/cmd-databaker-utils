# databakerUtils

Library of databaker add-on functionality. The intention to move away from ad-hoc branches and local-only scripts
towards something more reusable.

Initial commit is to add a custom csvWriter, so we can change the structure of the output CSV with a parameter.

you -MUST- be using the ConversionSegment().topandas() functionality for this to work.


## install

You MUST first have databaker and all it's dependancies installed.

`pip3 install databakerUtils`


## Usage (csvWriter)

import with:

`from databakerUtils import customWriter`


then replace the line:

`writetechnicalCSV("Output.csv", conversionsegments)`

with:

`customWriter("Output.csv", conversionsegments, "v4")`

where "v4" is the output structure you want.


## Adding additional output structures

Iv'e initially only added the v4 structure used by cmd. We can add more as follows.

Add a new .py file with a single function to the /structures directory. This file must contain one function called run that takes the name of the file to be output and variable representing a list of pandas dataframes.

The name of the file is the parameter by which you specify that output structure.

example:

..with this file called example.py in structures

`def run(OutputName, dfList):

    for dataframe in dfList:
      print(dataframe)
`

you could use the command:

`customWriter("Output.csv", conversionsegments, "example")`

to make your "output" functionality into printing each dataframe to screen in turn.

what the scripts actually do is at the authors discretion (you should be able to get to any strcuture from pandas), but just be aware there is no return. Whatever and however you output the data its a one-way process.
