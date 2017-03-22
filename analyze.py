"""
    This code performs various analyses using python3 and pandas. 
   

    Written by Praveen NG
"""
import sys


def main():

    # if requested analysis is not in the list, 
    # program will throw an error
    avail_analyses = ['mean', 'std', 'median', 'var']
    args = sys.argv
    fname, columns, analyses, nskip, lines, sep = \
    readargs(args, avail_analyses)
    
    # read data file
    df = readfile(fname, nskip, sep)

    # slice dataframe
    df = slice_df(df,lines, columns)

    # perform analyses
    do_task(df, analyses, columns)

    # done!




def readargs(args, avail_analyses):
    # are there sufficient number of 
    # command-line arguments?
    if(len(args)<2):
        print('\nPlease specify a file name')
        printerror('help')
        exit(0)
    
    # reading the command-line arguments
    fname, columns, analyses, nskip, lines, \
    sep = myargs(args)

    # process column numbers if does not have 
    # default value (type int)
    if(type(columns) != int):
        columns = processcol(columns)
    print(columns)

    # convert header skips into an int type
    nskip = processnskip(nskip)

    # convert line numbers into a list of numbers
    # do I need to do this?
    if(type(lines) != int):
        lines = processlines(lines, nskip)

    # convert analyses into a python list
    analyses = processanalyses(analyses, avail_analyses)
 
    return (fname, columns, analyses, nskip, lines, sep)


    

def printerror(err):
    ''' Prints help and error messages.
    '''
    if(err == 'help'):
        analyses = ['mean', 'median','std (standard \
        deviation)','var (variance)']
        print('\nUsage example:')
        print('python3 analyze.py -f dir1/dir2/file.dat -s 4 -sep \'\\t\' -a median -c 2 -l 901:1000 -c 3')
        print('\nUse with the following arguments is valid:')
        print('\t-h : help (this doc)');
        print('\t-f : file name. not optional');
        print('\t-c : columns');
        print('\t     1, 1:4 are valid entries. default = all')
        print('\t-l : the lines used for analysis.')
        print('\t     1, 1:4 are valid entries. default = all')
        print('\t-a : analyses to perform on the selected column(s)')
        print('\t     to be provided within single quotes, \
        separated by comma')
        print('\t     the following analyses are doable \
        as of this version')
        print('\t    ', analyses)
        print('\t-s : number of header lines skipped (eg 10). default 0')
        print();
    elif(err == 'columns'):
        print('\nCould not read the column argument successfully')
        print('Exiting gracefully...\n')
        exit(0)
    elif(err == 'nskip'):
        print('\nCould not read the nskip argument successfully')
        print('Exiting gracefully...\n')
        exit(0)
    elif(err == 'analysis'):
        print('\nAnalysis is not available in list')
        print('make sure analyses are within quotes')
        print('or there is no space before/after commas')
        print('Exiting gracefully...\n')
        exit(0)
    elif(err == 'readfile'):
        print('\nReading file failed. Please check the path and filename')
        print('Also, make sure the -s (nskip) flag is used with appropriate')
        print('parameter\n')
        exit(0)




def myargs(args):
    #default values
    columns = -1
    analyses = 'mean'
    lines = -1 	    # all lines
    nskip = 0 	    # no skipping
    sep ='\t'

    arg_count = 0;
    while(arg_count < len(args)):
        arg = args[arg_count]
        if(arg == '-f'):
            arg_count += 1
            fname = args[arg_count]
        elif(arg == '-c'):
            arg_count += 1
            columns = args[arg_count]
        elif(arg == '-a'):
            arg_count += 1
            analyses = args[arg_count]
        elif(arg == '-s'):
            arg_count += 1
            nskip = args[arg_count]
        elif(arg == '-l'):
            arg_count += 1
            lines = args[arg_count]
        elif(arg == '-sep'):
            arg_count += 1
            sep = args[arg_count]
        elif(arg == '-h' or arg == '-help'):
            printerror('help')
        arg_count += 1
    # is the file name specified?
    if(fname == None):
        print('Please specify a file name')
        printerror('help')
        exit(0)
    return (fname, columns, analyses, nskip, lines, sep)




def processcol(columns):
    columns = columns.strip().split(':')
    if len(columns)>1:
        try:
            col_b = int(columns[0])-1
            col_e = int(columns[1])
        except:
            printerror('columns')
        columns = list(range(col_b,col_e))
    else:
        try:
            columns = int(columns[0])-1
        except:
            printerror('columns')
    return columns




def processlines(lines, nskip):
    lines = lines.strip().split(':')
    if len(lines)>1:
        try:
            lines_b = int(lines[0])-1-nskip
            lines_e = int(lines[1])-nskip
        except:
            printerror('lines')
        lines = list(range(lines_b,lines_e))
    else:
        try:
            lines = int(lines[0])-1-nskip
        except:
            printerror('lines')
    return lines




def processnskip(nskip):
    try:
        nskip = int(nskip)
    except:
        printerror('nskip')
    return nskip




def processanalyses(analyses, avail_analyses):
    analyses = analyses.split(',')
    for analysis in analyses:
        if analysis not in avail_analyses: 
            printerror('analysis')
    return analyses




def readfile(fname, nskip,  sep):
    # if no errors so far, load pandas
    import pandas as pd
    
    try:
        df = pd.read_table(fname, skiprows = nskip, \
        header=None, sep = sep, engine='python')
    except:
        printerror('readfile')

    return df




def slice_df(df,lines, columns):
    # slicing dataframe according to columns and 
    # lines parameters
    if(lines == -1 and columns == -1):
        df = df.iloc[:, :]
    elif(lines == -1):
        df = df.iloc[:, columns]
    elif(columns != -1):
        df = df.iloc[lines, :]
    else:
        df = df.iloc[lines, columns]
    return df




def do_task(df, analyses, columns):
    # analyze the sliced dataframe
    for analysis in analyses:
        if (analysis=='mean'):
            mean = []
            for col in columns:
                mean.append(df.iloc[:,col].mean())
            print('mean is   ',mean)
        elif (analysis=='median'):
            median = []
            for col in columns:
                median.append(df.iloc[:,col].median())
            print('median is ',median)
        elif (analysis=='std'):
            std = []
            for col in columns:
                std.append(df.iloc[:,col].std())
            print('std is    ',std)
        elif (analysis=='var'):
            var = []
            for col in columns:
                var.append(df.iloc[:,col].var())
            print('var is    ',var)




if __name__ == '__main__':
    main()
