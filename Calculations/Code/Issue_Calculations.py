from datetime import datetime, timedelta
from sqlite3 import Cursor, Connection
import pandas as pd



class Logic:
    '''
This is logic to call all other classes and methods that make the program run.\n
Does very little analysis of data.
    '''

    def __init__(self, table: pd.DataFrame, cursor:Cursor=None, connection:Connection=None) ->  None:
        '''
Initalizes the class and sets class variables that are to be used only in this class instance.\n
:param table: the Issues table from the database. \n
:param cursor: The database cursor.\n
:param connection: The database connection.
        '''

        self.dbCursor = cursor
        self.dbConnection = connection
        self.data = table
    
    #--------------------------------------------------------------
    # Issue Spoilage Methods
    def issue_spoilage_min_max_avg(self, c, conn, Issues, day):
        Issue_Spoilage = []
        total = 0

        for issue in Issues:
            #print(issue)
            open_date = datetime.strptime(issue[0], "%Y-%m-%d")
            if(issue[1] == "None"):
                Issue_Spoilage.append(day - open_date)
            else:
                Issue_Spoilage.append((day - open_date).days)

        if not Issue_Spoilage:
            Min = 0
            Max = 0
            Avg = 0
        else:
            Min = min(Issue_Spoilage) 
            Max = max(Issue_Spoilage)
            
            for i in Issue_Spoilage:
                total = total + i

            Avg = total / len(Issue_Spoilage)

        return Min, Max, Avg

    def insert_into_issue_spoilage_table(self, c, conn, days):
        #First Pull down all of the values and loop through them one day at a time
        
        #Once table exists, pull down data here#

        #Now loop!
        for day in days:
            # print(day)

            Num_Of_Open_BF = "" #Fill this with the total number of open BF on that date
            Num_Of_Open_FR = "" #Fill this with the total number of open FR on that date
            Num_Of_Open_T = "" #Fill this with the total number of open T on that date
            Num_Of_Closed_BF = "" #Fill this with the total number of closed BF on that date
            Num_Of_Closed_FR = "" #Fill this with the total number of closed FR on that date
            Num_Of_Closed_T = "" #Fill this with the total number of closed T on that date
            DeDen_Open_BF = "" #Fill this with defect density of BF
            DeDen_Open_FR = "" #Fill this with defect density of FR
            DeDen_Open_T = "" #Fill this with defect density of T
            IssSpoil_Open_BF = "" #Fill this with issue spoilage of BF
            IssSpoil_Open_FR = "" #Fill this with issue spoilage of FR
            IssSpoil_Open_T = "" #Fill this with issue spoilage of BT
            Lines_Of_Code = "" #Store the lines of code on that specifc date

            day = datetime.strptime(str(day)[:10], "%Y-%m-%d")

            c.execute("SELECT date(created_at), date(closed_at) FROM ISSUES WHERE date(created_at) <= date('" + str(day) + "') AND date(closed_at) >= date('" + str(day) + "') OR date(created_at) <= date('" + str(day) + "') AND closed_at = 'None';")
            Issues = c.fetchall()
            # print(Issues)
            conn.commit()

            Min, Max, Avg = self.issue_spoilage_min_max_avg(c, conn, Issues, day)

            sql = "PRAGMA table_info('Timed_Calculations');"
            c.execute(sql)
            column_names = c.fetchall()
            current_issue_table_names = []
            for row in column_names:
                current_issue_table_names.append(row[1])
            conn.commit()

            # sql = "IF NOT EXISTS( SELECT Issue_Spoilage_Min FROM Issues ) THEN ALTER TABLE Timed_Calculations ADD Issue_Spoilage_Min varchar(3000) NOT NULL default '0'; END IF; "
            if "Issue_Spoilage_Min" not in current_issue_table_names: 
                sql = "ALTER TABLE Timed_Calculations ADD Issue_Spoilage_Min varchar(3000);"
                c.execute(sql)
                conn.commit()

            if "Issue_Spoilage_Max" not in current_issue_table_names: 
                sql = "ALTER TABLE Timed_Calculations ADD Issue_Spoilage_Max varchar(3000);"
                c.execute(sql)
                conn.commit()

            if "Issue_Spoilage_Avg" not in current_issue_table_names: 
                sql = "ALTER TABLE Timed_Calculations ADDEXISTS Issue_Spoilage_Avg varchar(3000);"
                c.execute(sql)
                conn.commit()

            sql = "INSERT INTO Timed_Calculations (calendar_date, Issue_Spoilage_Min, Issue_Spoilage_Max, Issue_Spoilage_Avg) VALUES (?,?,?,?)"
            sql += "ON CONFLICT(calendar_date) DO UPDATE SET Issue_Spoilage_Min = (?), Issue_Spoilage_Max = (?), Issue_Spoilage_Avg = (?);"
            c.execute(sql, (str(day), str(Min), str(Max), str(Avg), str(Min), str(Max), str(Avg)))
            conn.commit()

    def generate_DateTimeList(self, rCDT: datetime) -> list:
        '''
Creates a list of datetimes from the repository conception datetime till today's current datetime.\n
:param rCDT: Repository conception datetime. This is found in the root api call of a repository.
        '''
        foo = []
        today = datetime.today()
        if rCDT.strftime("%Y-%m-%d") == today.strftime("%Y-%m-%d"):
            foo.append(str(today))
        else:
            foo.append(str(today))
            while (today > rCDT):
                today = today - timedelta(days=1)
                foo.append(str(today))
        return foo

    def call_issue_spoilage_methods(self) -> None:
        '''
Calls classes and methods to analyze and interpret data.
        '''

        first_time_stamp = self.data.loc[0, "Created_At"].replace("T", " ").replace("Z", "")
        repoConcptionDateTime = datetime.strptime(first_time_stamp, "%Y-%m-%d %H:%M:%S")
        
        # Index 0 = Current datetime, Index -1 = conception datetime
        datetimeList = self.generate_DateTimeList(rCDT=repoConcptionDateTime)
        # print(datetimeList)
        # exit()

        self.insert_into_issue_spoilage_table(self.dbCursor, self.dbConnection, datetimeList)

        # # Adds all of the datetimes to the SQL database
        # # Bewary of changing
        # for foo in datetimeList:

        #     date = datetime.strptime(foo[:10], "%Y-%m-%d")
        #     date = str(date)

        #     self.dbCursor.execute(
        #         "SELECT Avg, Min, Max FROM Issue_Spoliage WHERE date(date) == date('" + date + "');")
        #     rows = self.dbCursor.fetchall()
        #     Avg = rows[0][0]
        #     Min = rows[0][1]
        #     Max = rows[0][2]

        #     sql = "INSERT INTO Master (date, issue_spoilage_avg, issue_spoilage_min, issue_spoilage_max) VALUES (?,?,?,?) ON CONFLICT(date) DO UPDATE SET issue_spoilage_avg = (?), issue_spoilage_min = (?), issue_spoilage_max = (?);"
        #     self.dbCursor.execute(
        #         sql, (date, str(Avg), str(Min), str(Max), str(Avg), str(Min), str(Max)))

        #     self.dbConnection.commit()

    # Issue Spoilage Methods Ends
    #--------------------------------------------------------------
    


