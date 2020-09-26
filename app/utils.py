import mysql.connector as mysql
import pandas as pd

db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "IsakonIsakon123"
)

df = pd.read_sql("select * from news.links l", db)
# cursor = db.cursor()
#
# cursor.execute("SHOW DATABASES")
print(df)