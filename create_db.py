import pymysql

mydb = pymysql.connect(
    host="localhost",
    user="shavu",
    password="savitri",
)

my_cursor = mydb.cursor()
# my_cursor.execute("CREATE DATABASE sales_log")
my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)