# all the imports
import os
import sys
import sqlite3
import pandas as pd
from flask import Flask, g, render_template
from contextlib import closing


'''
TODO: put all tables into a master table?
for path, subdirs, files in os.walk("../../../Metrics-Dashboard"):
    for name in files:
        if name.lower().endswith(".db"):
            ...
'''

# Extracting name from args
##dbname = sys.argv[1].split("/")[-1]
with open("TestTestDatabase.db", "r") as foo:
    print("Hello World")
    foo.close()


# create our little application :)
app = Flask(__name__)

# configuration
app.config.update(
    dict(
        DATABASE=str("TestTestDatabase.db"),
    )
)


def connect_db():
    return sqlite3.connect(app.config["DATABASE"])


def init_db():
    with closing(connect_db()) as db:
        db.commit()


@app.route("/")
def stacked_bar_chart():
    # Read query results into a pandas DataFrame
    con = connect_db()
    df = pd.read_sql_query("SELECT * from Calculations ORDER BY date DESC", con)
    # df = data[0:1]

    # verify that result of SQL query is stored in the dataframe
    print(df.to_json())

    con.close()

    date = df["Date"].values.tolist()  # x axis
    defect_density = df["Defect Density"].values.tolist()
    commits = df["Commits per Week"].values.tolist()
    #issues = df["issues"].values.tolist()
    #lines_of_code = df["lines_of_code"].values.tolist()
    issue_spoilage_avg = df["Issue Spoilage"].values.tolist()
    # issue_spoilage_min = df['issue_spoilage_min'].values.tolist()
    # issue_spoilage_max = df["issue_spoilage_max"].values.tolist()
   

    return render_template(
        "charts.html",
        date=date,
        commits=commits,
       # issues=issues,
       # lines_of_code=lines_of_code,
        defect_density=defect_density,
        issue_spoilage_avg=issue_spoilage_avg,
    )


if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0")

# first build the docker image
# then run 'docker run -v metrics:/metrics -p 5000:5000 <name_of_image>'
# this opens a port for the flask server to run in
