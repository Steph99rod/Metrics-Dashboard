import json
import os
import sys
import unittest
from json import load

from requests import Response

sys.path.append("../")

from issues import Issues
from libs.databaseConnector import DatabaseConnector
from libs.githubConnector import GitHubConnector


class TestCommits(unittest.TestCase):
    def setUp(self) -> None:
        self.dbConnection = DatabaseConnector(databaseFileName="temp.db")
        self.dbConnection.createDatabase()
        self.dbConnection.openDatabaseConnection()
        commitsSQL = "CREATE TABLE Commits (SHA TEXT,Commit_Date TEXT, Author TEXT, Message TEXT, Comment_Count INTEGER, PRIMARY KEY(SHA));"
        self.dbConnection.executeSQL(sql=commitsSQL, commit=True)

        with open("jsonResponses.json", "r") as file:
            self.issuesResponse = load(file)["issues"]
            file.close()

        with open("jsonResponseHeaders.json", "r") as file:
            self.issuesResponseHeaders = load(file)["issues"]
            file.close()

        self.issuesCollector = Issues(
            dbConnection=self.dbConnection,
            oauthToken="CHANGE ME",
            repository="Metrics-Dashboard",
            username="SoftwareSystemsLaboratory",
        )

    def test_Commits(self):
        assert self.issuesCollector.currentPage == 1
        assert self.issuesCollector.repository == "Metrics-Dashboard"
        assert self.issuesCollector.username == "SoftwareSystemsLaboratory"

    def test_getData(self):
        data = self.issuesCollector.getData()
        assert data[1].status_code == 200
        self.assertIsInstance(data[0], list)

    def test_insertData(self):
        self.issuesCollector.insertData(dataset=self.issuesResponse)

    # TODO: Create a proper test for this function
    # def test_IterateNext(self):

    def tearDown(self) -> None:
        os.remove("temp.db")