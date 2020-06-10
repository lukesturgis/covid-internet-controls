import mysql.connector

mydb = mysql.connector.connect(
  host="129.21.183.44",
  user="root",
  password="TWCUU0Xz6TQiRUwPKZoD13Ta"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE mydatabase")
