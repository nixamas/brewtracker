import sqlite3, random, datetime

def main():
    conn = sqlite3.connect("mydatabase.db")

    cursor = conn.cursor()

    cursor.execute("""create table if not exists readings (time text, temperature text)""")
    #Get Readings from the sensors
    
    try:
        with open('/sys/bus/w1/devices/28-000004b5fbb9/w1_slave') as f: 
            print("found file...")
            content = f.readlines()
            lVal = str(content[1])  #get 2nd line of file
            temp = lVal.rsplit('=',1)   #split temp value out
            tC = ( int(temp[1])/1000)   #find C
            tF = ( tC * (9/5) + 32 )    #find F
            print("file line 2 :: " + str(tC) + "^C -- " + str(tF) + "^F ")
    except IOError:
        print ("No Temperatue Sensor was found... Storing Random data...")  
        tF = random.randrange(55, 83)
    
    temperature = str(tF)

    time = str(datetime.datetime.now()).split('.')[0]
    #Store Readings into the database
    cursor.execute("INSERT INTO readings VALUES ('" + time + "', '" + temperature + "')")
    print("sql ~ INSERT INTO readings VALUES ('" + time + "', '" + temperature + "')")
    conn.commit()

    #print ("\nHere's a listing of all the records in the table:\n")
    #for row in cursor.execute("SELECT rowid, * FROM readings ORDER BY time"):
        #print (str(row))
        
    #print("writing data to javascript file...")
    #jsonencoder.main()
    
def get_temperature():
    try:
        with open('/sys/bus/w1/devices/28-000004b5fbb9/w1_slave') as f: 
            print("found file...")
            content = f.readlines()
            lVal = str(content[1])  #get 2nd line of file
            temp = lVal.rsplit('=',1)   #split temp value out
            tC = ( int(temp[1])/1000)   #find C
            tF = ( tC * (9/5) + 32 )    #find F
            print("file line 2 :: " + str(tC) + "^C -- " + str(tF) + "^F ")
    except IOError:
        print ("No Temperatue Sensor was found... Storing Random data...")  
        tC = random.randrange(30, 40)
        tF = random.randrange(55, 83)
        
    return "Fahrenheit :: " + str(tF) + " ---- Celsius :: " + str(tC)

if __name__ == "__main__":
    main()