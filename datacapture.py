import sqlite3, random, datetime

conn = sqlite3.connect("mydatabase.db")

cursor = conn.cursor()

cursor.execute("""create table if not exists readings (time text, temperature text)""")

#Get Readings from the sensors
temp = random.randrange(55, 83)
temperature = str(temp)

time = str(datetime.datetime.now()).split('.')[0]
#Store Readings into the database
cursor.execute("INSERT INTO readings VALUES ('" + time + "', '" + temperature + "')")
conn.commit()

print ("\nHere's a listing of all the records in the table:\n")
for row in cursor.execute("SELECT rowid, * FROM readings ORDER BY time"):
    print (str(row))