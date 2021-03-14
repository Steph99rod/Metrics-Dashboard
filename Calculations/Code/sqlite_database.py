import sqlite3
import os

def open_connection(repo_name: str):
    '''
    Repo must exist in Metrics-Dashboard/Data-Collection/
    This is some SQL code that creates the tables and columns in a database named after the repository its data is holding.
    '''    
    # ex: current_cwd = '/Users/name/Desktop/Code/Metrics/Metrics-Dashboard/Calculations'
    current_cwd = os.getcwd()

    # get the numerical position of the word "Metrics-Dashboard" 
    metrics_folder = current_cwd.find("Metrics-Dashboard")

    # ex: current_cwd = '/Users/name/Desktop/Code/Metrics/Metrics-Dashboard/
    current_cwd = current_cwd[:metrics_folder + len("Metrics-Dashboard")]

    # data-collection folder is where the database will come from 
    data_collection_folder  = current_cwd + '/Data-Collection/'

    # try to connect to the database 
    try:
        connection = sqlite3.connect(data_collection_folder + repo_name + ".db")
    except sqlite3.OperationalError:
        connection = sqlite3.connect(data_collection_folder + repo_name + ".db")

    cursor = connection.cursor()

    # TODO: go to data collection and add the other create table if not exists here 

    # create the calculations table 
    cursor.execute('''CREATE TABLE IF NOT EXISTS Calculations
            (
                calculation_name VARCHAR(3000), 
                description VARCHAR(3000),
                value VARCHAR(3000),
                PRIMARY KEY (calculation_name)
            ) ;''')
    
    # columns are to be added to the table using "alter table" to add calculations as their own column 
    cursor.execute('''CREATE TABLE IF NOT EXISTS Timed_Calculations
            (
                calendar_date VARCHAR(3000),
                PRIMARY KEY (calendar_date)
            ) ;''')


    connection.commit()
    
    return cursor, connection
