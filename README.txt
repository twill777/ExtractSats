Approach:
- In order to ensure the problem was properly approached, I treated the code as if it were to be used functionally in a larger software environment
- Because of the above, I assumed this function would be called by code and so did not set up user input or input validation.
- To make the code sclalable for future development, I expanded the scope of the filters and output to take in filters for any columns,
and to optionally change how the data is outputted so that it is not hardcoded to filter for and output the same columns every time.
- The filtering for other columns was not actually requested, so I did not implement any filtering for continuous values and instead left
it to only perform exact matches; given that all values for "Operator" and "Frequency Band" were discrete this was sufficient



How it works:
- The code is hardcoded with column titles and their indices. This could be improved upon by dynamically reading in column headers from the csv file,
but this was unecessary for the current application
- These headers are stored in dictionary as keys, with the corresponding values indicating the value of each column. This allows for the code to be
passed a column header as an argument and to know which column it is referring to
- The user can pass in a list of column headers indicating which columns are to be outputted (in this case [ "NORAD", "Operator", "FrequencyBand" ])
- When reading from the csv file, the code first adds each satellite to the dictionary. This is done so that the data can be accessed again later
and is for the scalability of the code so the file only has to be read once, however it could be improved by only adding relevant satellites after
filtering instead depending on the application
- The satellites are filtered at the same time as they are being read to a) not have to iterate through them again, and b) make it simple to change
the code to only add satellites to the dictionary that pass a filter
- If a satellite matches one of the filters, its name is added to a list of satellites that is to be outputted. This list can later be iterated over
and the names used as keys in the satellite dictionary to fetch all the relevant data



How to use it:
Change the filters list at the bottom of the file to change what columns are being filtered/values are being matched
Change the outputColumns list a the bottom of the file to change what columns are being outputted



Documentation:
- the function ExtractSats takes in 1 to 3 arguments, and prints out a subset of satellites and columns from 'csvFile'

ExtractSats(csvFile, filters=[], outputColumns=[])

csvFile: the string name of the csv satellite file (in this case 'satellites.csv')

filters: all filters are passed in a single list, comprised of lists for each column to be filtered
- Each list in the filters list has the column name at the first index, and then optionally any values to be
matched exactly in that column as the other items
- If left empty or not included, all satellites will be outputted
- If only the column name is passed, it will match any satellite that has a value in that column
ex. filters = [ ["Operator", "SES"], ["FrequencyBand", "C", "Ku"], ["Downlink"] ]
The above will output any satellite that has any one of the following:
	"SES" as an operator
	"C" or "KU" in its frequency bands
	Any value for downlink

outputColums: A list of columns to be included in the output, if left blank or not included all columns will be outputted
ex. outputColumns = [ "NORAD", "Operator", "FrequencyBand" ]
The above will print out each filtered satellite's Name, NORAD, Operator, and FrequencyBand values