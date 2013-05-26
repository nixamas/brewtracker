import sqlite3, random, datetime

def main():
    conn = sqlite3.connect("brewtrackerdb.db")

    cursor = conn.cursor()

    #cursor.execute("""create table if not exists readings (time text, temperature text)""")
    #Get Readings from the sensors
    
    try:
        with open('/sys/bus/w1/devices/28-000004b5fbb9/w1_slave') as f: 
            print("found temperature sensor file...")
            content = f.readlines()
            lVal = str(content[1])  #get 2nd line of file
            temp = lVal.rsplit('=',1)   #split temp value out
	    print("parsed data ::: " + str(temp[1]))
            tC = ( int(temp[1])/1000)   #find C
            tF = ( tC * (9/5) + 32 )    #find F
            print("temperatures :: " + str(tC) + "^C -- " + str(tF) + "^F ")
    except IOError:
        print ("No Temperatue Sensor was found... Storing Random data...")  
        tF = random.randrange(55, 83)
    
    temperature = str(tF)

    time = str(datetime.datetime.now()).split('.')[0]
    #Store Readings into the database
    cursor.execute("INSERT INTO readings (reading_time, reading_brew_temp, reading_amb_temp) VALUES ('" + time + "', '" + temperature + "')")
    print("sql ~ INSERT INTO readings VALUES ('" + time + "', '" + temperature + "')")
    conn.commit()

    
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

def insert_dummy_data(day):
    try:
        conn = sqlite3.connect("brewtrackerdb.db")
    
        cursor = conn.cursor()
        brewT = random.randrange(50, 65)
        ambT = random.randrange(66, 80)
        
        #time = str(datetime.datetime.now()).split('.')[0]
        time = str( datetime.datetime(2013,2,day) )
        cursor.execute("INSERT INTO readings (reading_time, reading_brew_temp, reading_amb_temp) VALUES ('" + time + "', '" + str(brewT) + "', '" + str(ambT) + "')")
        print("sql ~~ INSERT INTO readings VALUES ('" + time + "', '" + str(brewT) + "', '" + str(ambT) + "')")
        conn.commit()
    except Exception:
        print("EXCEPTION ::::::: " + str(Exception))

if __name__ == "__main__":
    #main()
    for x in range(1,25):
        insert_dummy_data(x)