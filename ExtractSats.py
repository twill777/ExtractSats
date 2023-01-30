import csv
from enum import Enum

# Columns values for a given satellite at satDict[satName]
Col = {}
Col ["Line1"] = 0
Col ["Line2"] = 1
Col ["NORAD"] = 2
Col ["Status"] = 3
Col ["Orbit"] = 4
Col ["Uplink"] = 5
Col ["Downlink"] = 6
Col ["Frequency"] = 7
Col ["FrequencyBand"] = 8
Col ["Operator"] = 9
Col ["Details"] = 10
Col ["Reference"] = 11
Col ["Notes"] = 12



def ParseFilters(filters, params):
    # The following code block provides only the requested functionality to filter by FrequencyBand and Operator
    # It is commented out in favour of broader filter options
    # ---
    if False:
        for arg in params:
            if arg[0] == "FrequencyBand" or arg[0] == "Operator":
                # Allow each argument to pass any number of matches for a given column
                for i in range(len(arg) - 1):
                    filters.append( [ Col[arg[0]], arg[i+1] ] )
        return
    # ---

    for arg in params:
        # Ignore empty lists
        if(len(arg)==0):
            continue
        # Passing just a column name will cause the output to include any satellite that has data in that column
        if(len(arg)==1):
            filters.append( [ Col[arg[0]], '*' ] )
            continue

        # Allow each argument to pass any number of matches for a given column
        for i in range(len(arg) - 1):
            filters.append( [ Col[arg[0]], arg[i+1] ] )



# Format outputs
def OutputSats(satOut, satDict, outCols=[]):
    outIdxs = []
    for col in outCols:
        outIdxs.append( Col[col] )

    for sat in satOut:
        outStr = sat + " : "   
        if len(outIdxs) > 0:
            for col in outIdxs:
                outStr += satDict[sat][col] + ", "
            # Trim the trailing comma and space
            outStr = outStr[:-2]
        else:
            outStr += ', '.join(map(str, satDict[sat]))
        
        print(outStr)



def ExtractSats(csvFile, in_filters=[], in_outputs=[]):
    # Dictionary of satellites, indexed by name
    satDict = {}
    # List of satellite names to output, sorted by filters
    satOut = []

    filters = []
    ParseFilters(filters, in_filters)
    print("Filtering satellites against: " + ' | '.join(map(str, in_filters)))

    print("Output Format...")
    outStr = "Name : "
   # Add each output column header to a string to be printed for clarity
    if in_outputs != []:
        for op in in_outputs:
            outStr += op + ", "
    # If no output formatting was passed, output all columns
    else:
        for k, v in Col:
            outStr += k + ", "
    # Trim the trailing comma and space
    outStr = outStr[:-2]
    print(outStr + "\n")

    with open(csvFile, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        # Start at index 1 to skip column names
        next(reader)
        for row in reader:
            satDict[row[0]] = row [1:]

            if len(filters) > 0:
                # Check each filter agains the satellite
                for f in filters:
                    # f+1 because the filter columns are shifted left 1,
                    #  assuming that the name is used for indexing
                    col = (f[0])+1

                    colVals = row[col].split("/")
                    # If not missing filtered data and scanning for any match (*), or matching filtered data
                    if ( f[1] == '*' and row[col] != '' ) or f[1] in colVals:
                        satOut.append(row[0])
                        continue
            else:
                satOut.append(row[0])

    OutputSats(satOut, satDict, in_outputs)

# Paramters for filtering
# All filters are passed in a single list, comprised of lists for each column to be filtered
# Each list in the filters list has the column name at the first index, and then optionally any values to be
#   matched exactly in that column
# If only a column name is passed, it instead matches for all rows with data in that column

# ie. [ ColumnName, optionalMatch1, optionalMatch2... ]

filters = [
    ["Operator", "SES"],
    ["FrequencyBand", "C"]
    ]

# Colums to include in output - can be changed to include any column
# Will include all columns if left empty
outputColumns = [ "NORAD", "Operator", "FrequencyBand" ]

ExtractSats('satellites.csv', filters, outputColumns)