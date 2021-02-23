from datetime import datetime, timedelta
from sqlite3 import Cursor, Connection
import Issue_Spoilage
import pandas as pd


class Logic:
    '''
This is logic to call all other classes and methods that make the program run.\n
Does very little analysis of data.
    '''

    def __init__(self, table: pd.DataFrame, cursor:Cursor=None, connection:Connection=None) ->  None:
        '''
Initalizes the class and sets class variables that are to be used only in this class instance.\n
:param username: The GitHub username.\n
:param repository: The GitHub repository.\n
:param token: The personal access token from the user who initiated the program.
:param tokenList: A list of tokens that will be iterated through.\n
:param data: The dictionary of data that is returned from the API call.\n
:param responseHeaders: The dictionary of data that is returned with the API call.\n
:param cursor: The database cursor.\n
:param connection: The database connection.
        '''

        self.dbCursor = cursor
        self.dbConnection = connection
        self.data = table


    def program(self) -> None:
        '''
Calls classes and methods to analyze and interpret data.
        '''

        first_time_stamp = self.data.loc[0, "Created_At"].replace("T", " ").replace("Z", "")
        repoConcptionDateTime = datetime.strptime(first_time_stamp, "%Y-%m-%d %H:%M:%S")
        
        # Index 0 = Current datetime, Index -1 = conception datetime
        datetimeList = self.generate_DateTimeList(rCDT=repoConcptionDateTime)
        # print(datetimeList)
        # exit()

        Issue_Spoilage.Main(self.dbCursor, self.dbConnection, datetimeList)

        # Adds all of the datetimes to the SQL database
        # Bewary of changing
        for foo in datetimeList:

            date = datetime.strptime(foo[:10], "%Y-%m-%d")
            date = str(date)

            self.dbCursor.execute(
                "SELECT Avg, Min, Max FROM ISSUE_SPOILAGE WHERE date(date) == date('" + date + "');")
            rows = self.dbCursor.fetchall()
            Avg = rows[0][0]
            Min = rows[0][1]
            Max = rows[0][2]

            sql = "INSERT INTO MASTER (date, issue_spoilage_avg, issue_spoilage_min, issue_spoilage_max) VALUES (?,?,?,?) ON CONFLICT(date) DO UPDATE SET issue_spoilage_avg = (?), issue_spoilage_min = (?), issue_spoilage_max = (?);"
            self.dbCursor.execute(
                sql, (date, str(Avg), str(Min), str(Max), str(Avg), str(Min), str(Max)))

            self.dbConnection.commit()

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
