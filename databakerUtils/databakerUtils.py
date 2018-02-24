import pandas as pd
import os
import importlib.util

"""
Allows the importing of a specified script from /structures for restructurng the databaker output csv.
This is setup to import dynamically, so we only import what we need (so we can have as many output-structures as we want).
"""

# Wrapper
def customWriter(OutputName, data, selectedWriter):

    # build a writer with an appropriately imported method
    writer = allWriters(OutputName, data, selectedWriter)

    # import it
    writer.importWriter()



# principle class, used to police input and create appropriate writer
class allWriters(object):

    def __init__(self, outputName, dataframesIn, selectedWriter):

        # Listify dataframes_in if there's only one ConversionSegment
        if type(dataframesIn) != list:
            dataframesIn = [dataframesIn]


        # Make sure we're only being passed pandas dataframes
        for df in dataframesIn:
            if type(df) != pd.DataFrame:
                raise ValueError("Input to Writer must always be pandas dataframes.")

        # Concatentate those dataframes
        dflist = pd.concat(dataframesIn)

        # Create a list of output structures for each .py script in /structures.
        files = [f for f in os.listdir('structures/.')]

        # Make sure they're asking for a writer that actually exists
        if selectedWriter not in [x[:-3] for x in files]:
            raise ValueError("Output format {of} not present. Have only got: ".format(of=selectedWriter), ",".join([f[:-3] for f in files]))

        # Store everything ready to run
        self.selectedWriter = selectedWriter
        self.outputName = outputName
        self.dflist = dflist


    # Import whatever the chosen writer was
    def importWriter(self):

        print("Importing Writer:", self.selectedWriter)
        spec = importlib.util.spec_from_file_location(self.selectedWriter, "structures/{file}.py".format(file=self.selectedWriter))
        run = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(run)
        run.run(self.outputName, self.dflist)

