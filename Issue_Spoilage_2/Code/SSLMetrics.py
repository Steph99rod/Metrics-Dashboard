from sqlite3 import Cursor, Connection  # Need these for determining type
# import Master
# from TokenHandler import TokenHandler
import sqlite_database
import sys
import pandas as pd 


class SSLMetrics:
    '''
This is what should be called to actually run the SSL Metrics tool.\n
Call this tool in the command line as: python SSLMetrics.py {GitHub URL} {Optional Token}
    '''

    def __init__(self) -> None:
        '''
Initializes the program and sets class variables that are going to be used as the initial values across the program.\n
Required command line arguements:\n
GitHub URL (https://github.com/{Username}/{Repository})\n
Optional command line arguements:\n
GitHub Personal Access Token
        '''
        self.args = sys.argv[1:]  # All of the command line args excluding the filename
        self.dbCursor = None  # Database specific variable
        self.dbConnection = None  # Database specific variables

    def parseArgs(self) -> None:
        '''
This is a REQUIRED method.\n
Logic to parse the list of command line arguements to make sure that they meet program requirements.\n
Will also generate the keys.txt file, get data from it, and potentially write data to it as well.
        '''
        if len(self.args) > 2:
            sys.exit("Too Many Args")
        try:
            self.db_input_location = self.args[0]
        except IndexError:
            sys.exit("No Database Input Location Arg")
        try:
            self.db_input_location = self.args[1]
        except IndexError:
            sys.exit("No Database Output Location Arg")


    def launch(self) -> None:
        '''
This is a REQUIRED method.\n
Logic to actually begin the analysis.
        '''
        self.dbCursor, self.dbConnection = sqlite_database.open_connection(self.db_input_location)

    def obtainIssuesTable(self) -> None:
        get_issues_table = self.dbCursor.execute("SELECT * FROM Issues")
        issues_df = pd.Dataframe(get_issues_table.fetchall())
        issues_df.columns = get_issues_table.keys()
        print(issues_df)

s = SSLMetrics()
s.parseArgs()
s.launch()
s.obtainIssuesTable()
print("hey SSL Metrics")
sys.exit(0)