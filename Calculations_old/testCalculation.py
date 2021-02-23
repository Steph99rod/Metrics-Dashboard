import unittest
from IssuesCalculation import Calculations

class TestIssuesCalculation(unittest.TestCase):

    def setUp(self):
        self.testCalc = Calculations("alt-tab-macos.db")
        self.conn = self.testCalc.conn

    def test_successful_db_conn(self):
        result = self.conn
        self.assertFalse(result is None)
    def test_total_issues(self):
        expected = 645 
        result = self.testCalc.get_total_issues(self.conn)
        self.assertTrue(expected == result)

    def test_get_open_count(self):
        expected = 52 
        result = self.testCalc.get_open_count(self.conn)
        self.assertTrue(expected == result)

    def test_get_closed_count(self):
        expected = 593
        result = self.testCalc.get_closed_count(self.conn)
        self.assertTrue(expected == result)

    def test_get_closed_to_open_ratio(self):
        expected = 11.4
        result = self.testCalc.get_closed_to_open_ratio(self.conn)
        self.assertTrue(expected == result)

    def test_get_closing_efficiency(self):
        expected = "92.0%"
        result = self.testCalc.get_closing_efficiency(self.conn)
        self.assertTrue(expected == result)

    def test_get_avg_to_close_issue(self):
        expected = 16.05
        result = self.testCalc.get_avg_days_to_close_issue(self.conn)
        self.assertTrue(expected == result)


if __name__ == '__main__':
    unittest.main()
        
