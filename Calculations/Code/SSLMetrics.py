from sqlite3 import Cursor, Connection  # Need these for determining type
import Issue_Calculations
import sqlite_database
import sys
import pandas as pd 

# have MetricsDashboard as a db in Data-Collection then: 
# python SSLMetrics.py MetricsDashboard $(pwd)

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
            self.db_output_location = self.args[1]
        except IndexError:
            sys.exit("No Database Output Location Arg")


    def launch(self) -> None:
        '''
This is a REQUIRED method.\n
Logic to actually begin the analysis.
        '''
        self.dbCursor, self.dbConnection = sqlite_database.open_connection(self.db_input_location)

    def obtainTable(self, table: str) -> pd.DataFrame:
        '''
This is a REQUIRED method.\n
Logic to read in Issues table from user-selected database. 
        '''
        self.dbCursor.execute("SELECT * FROM " + table)
        self.table_df = pd.DataFrame(self.dbCursor.fetchall())
        column_names = [x[0] for x in self.dbCursor.description]
        self.table_df.columns = column_names
        return self.table_df
    
    def conductIssuesCalc(self, table: pd.DataFrame) -> None:
        '''
Passes the table given to the Issue_Calculations class. 
Add calculations to the Calculations table in the database. 
        '''
        Issue_Calculations.Issue_Spoilage(table, self.dbCursor, self.dbConnection).main()
        Issue_Calculations.Other_Calculations(table, self.dbCursor, self.dbConnection).main()

        
    

s = SSLMetrics()
s.parseArgs()
s.launch()
issues_df = s.obtainTable("Issues")
s.conductIssuesCalc(issues_df)
sys.exit(0)