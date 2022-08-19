# read-las
A python function for reading digital well log files

Log ASCII Standard (LAS) is a widely used format for storing digital well log data.  The read-las python function parses LAS files that are formatted according to LAS 2.0 specifications.  A copy of the LAS 2.0 specifications is available at https://www.cwls.org/wp-content/uploads/2017/02/Las2_Update_Feb2017.pdf.

To use this function, place a copy of the file 'readlas.py' into your working directory.  Import the function into your python file using the following line of code: 

#from readlas import readlas

Run the function using the following line of code:

#readlas(fileName)

where the argument 'fileName' is the name of a single LAS file in string format.  If your LAS file is located outside of your working directory, you will also need to provide the file path.  The outputs of the function can be accessed via object attribute syntax as follows:

readlas.wellname, readlas.api, readlas.uwi, readlas.strt, readlas.stop, readlas.step, readlas.null, readlas.header, readlas.curves, readlas.units, readlas.data

The output 'readlas.data' contains the curve data stored in a Pandas DataFrame.  To see an example of how this function works, open and run the file ./example/readlasExample.py.  

This function may fail in instances where the formatting of an LAS file does not strictly follow LAS 2.0 specifications. 



