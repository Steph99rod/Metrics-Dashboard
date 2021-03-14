from datetime import datetime, timedelta
from sqlite3 import Cursor, Connection
import pandas as pd
import sqlite3 

#--------------------------------------------------------------
# Issue Spoilage Class

class Issue_Spoilage:
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

    def main(self) -> None:
        '''
Calls classes and methods to analyze and interpret data.
        '''
        first_time_stamp = self.data.loc[0, "Created_At"].replace("T", " ").replace("Z", "")
        repoConcptionDateTime = datetime.strptime(first_time_stamp, "%Y-%m-%d %H:%M:%S")
        # Index 0 = Current datetime, Index -1 = conception datetime
        datetimeList = self.generate_DateTimeList(rCDT=repoConcptionDateTime)
        self.insert_into_issue_spoilage_table(self.dbCursor, self.dbConnection, datetimeList)
    
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
        
        # get all column names of the table Time_Calculations 
        sql = "PRAGMA table_info('Timed_Calculations');"
        c.execute(sql)
        column_names = c.fetchall()
        current_issue_table_names = []
        for row in column_names:
            current_issue_table_names.append(row[1])
        conn.commit()

        # if the following names do not exist in the table, then add them as columns 
        if "Issue_Spoilage_Min" not in current_issue_table_names: 
            sql = "ALTER TABLE Timed_Calculations ADD Issue_Spoilage_Min varchar(3000);"
            c.execute(sql)
            conn.commit()

        if "Issue_Spoilage_Max" not in current_issue_table_names: 
            sql = "ALTER TABLE Timed_Calculations ADD Issue_Spoilage_Max varchar(3000);"
            c.execute(sql)
            conn.commit()

        if "Issue_Spoilage_Avg" not in current_issue_table_names: 
            sql = "ALTER TABLE Timed_Calculations ADD Issue_Spoilage_Avg varchar(3000);"
            c.execute(sql)
            conn.commit()

        for day in days:
            # print(day)

            day = datetime.strptime(str(day)[:10], "%Y-%m-%d")

            c.execute("SELECT date(created_at), date(closed_at) FROM ISSUES WHERE date(created_at) <= date('" + str(day) + "') AND date(closed_at) >= date('" + str(day) + "') OR date(created_at) <= date('" + str(day) + "') AND closed_at = 'None';")
            Issues = c.fetchall()
            conn.commit()

            Min, Max, Avg = self.issue_spoilage_min_max_avg(c, conn, Issues, day)

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

# Issue Spoilage class ends 
#--------------------------------------------------------------

class Other_Calculations:

    def __init__(self, table, dbCursor, dbConnection) -> None:
        ''' 
        Initialize class variables
        :param table: issues dataframe 
        '''
        self.conn = dbConnection
        self.table = table
        self.cur = dbCursor

    def main(self) -> None:
        
        # sql to insert calculations into table 
        sql = "INSERT INTO Calculations (calculation_name, description, value) VALUES (?,?,?)"
        sql += "ON CONFLICT(calculation_name) DO UPDATE SET description = (?), value = (?);"

        # insert total_issues into calculations table 
        total_issues = str(self.get_total_issues())
        decription = "Includes currently open and closed issues."
        self.conn.execute(sql, ("Total Number of Issues", decription, total_issues, decription, total_issues) )
        self.conn.commit()

        # insert open issues into calculations table 
        issues_open = str(self.get_open_count())
        decription = "Issues that do not have a Closed_At date."
        self.conn.execute(sql, ("Number of Open Issues", decription, issues_open, decription, issues_open) )
        self.conn.commit()

        # insert closed issues into calculations table 
        issues_closed = str(self.get_closed_count())
        decription = "Issues that have a Closed_At date."
        self.conn.execute(sql, ("Number of Closed Issues", decription, issues_closed, decription, issues_closed) )
        self.conn.commit()

        ratio = str(round((int(issues_closed) / int(issues_open)),2))
        decription = "Number of Closed Issues / Number of Open Issues"
        self.conn.execute(sql, ("Closed to Open Ratio", decription, ratio, decription, ratio) )
        self.conn.commit()

        closing_efficiency = self.get_closing_efficiency(int(total_issues), int(issues_closed))
        decription = "Number of Closed Issues / Total Number of Issues"
        self.conn.execute(sql, ("Closing Efficiency", decription, closing_efficiency, decription, ratio) )
        self.conn.commit()

    def get_total_issues(self) -> int:
        ''' 
        Returns the total number of issues
        '''
        return self.table.shape[0]


    def get_open_count(self):
        ''' 
        Returns the total number of open issues
        '''
        issues_still_open_df = self.table.astype(str)
        issues_still_open_df = issues_still_open_df.loc[issues_still_open_df.Closed_At == "None"]
        return issues_still_open_df.shape[0]

    def get_closed_count(self):
        ''' 
        Returns the total number of closed issues
        :param conn: The db connection
        '''
        issues_closed_df = self.table.astype(str)
        issues_closed_df = issues_closed_df.loc[issues_closed_df.Closed_At != "None"]
        return issues_closed_df.shape[0]


    def get_closing_efficiency(self, total, closed_count) -> str:
        ''' 
        Returns efficiency, based on the principle of efficiency in physics, efficiency = output/input, where output = closed issues, input = total issues
        :param conn: The db connection
        '''
        closing_efficiency = round((closed_count / total),2)
        closing_efficiency_percent = closing_efficiency * 100
        result = str(closing_efficiency_percent) + "%"
        return result

    # def get_avg_days_to_close_issue(self,conn: Connection) -> float:
    #     ''' 
    #     Returns average number of days it takes to close an Issue
    #     :param conn: The db connection
    #     '''
    #     cur = conn.cursor()
    #     query = "SELECT julianday(closed_at) - julianday(created_at) from ISSUES where state='closed'"
    #     cur.execute(query)
    #     result = cur.fetchall()
    #     days = [i[0] for i in result]
    #     avg = round((sum(days) / len(days)),2)
    #     cur.close()
    #     return avg
        


