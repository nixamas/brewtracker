import json, sqlite3

def main():
    with open('data.js', 'w') as f:
        f.write("var datareadings = ")  #write variable declaration to javascript file
        readings = {}
        conn = sqlite3.connect("brewtrackerdb.db")
        cursor = conn.cursor()
        readings = '{"count":"%s","readings":['     #start of json object
        cnt = 0
        for row in cursor.execute("SELECT * FROM readings ORDER BY reading_time"):
            rdng = '{"id":"' + str(row[0]) + '","reading_time":"' + str(row[1]) + '","reading_brew_temp":"' + str(row[2])+ '","reading_amb_temp":"' + str(row[3]) + '"},'
            #print (rdng)
            readings = readings + rdng
            cnt += 1
           
        readings = readings[:-1]    #remove last comma
        readings = readings + ']}'
        readings = readings % cnt
        #print(str(readings))
    
        json.dump(readings, f, ensure_ascii=False)
        
        f.write("\n\r")
        f.write("function getDataReadings(){")
        f.write('   console.log("Returning data to analysis.html..."); ')
        f.write('   return datareadings; ')
        f.write("}")

	print('javascript file written!!')
        
def build_json():
    try:
        print("building json object")
        conn = sqlite3.connect("brewtrackerdb.db")
        cursor = conn.cursor()
        readings = '{"count":"%s","readings":['     #start of json object
        cnt = 0
        q = cursor.execute("SELECT * FROM readings ORDER BY reading_time")
        print("QUERY ::: " +str(q))
        for row in q:
            rdg = '{"id":"' + str(row[0]) + '","reading_time":"' + str(row[1]) + '","reading_brew_temp":"' + str(row[2])+ '","reading_amb_temp":"' + str(row[3]) + '"},'
            print(rdg)
            readings = readings + rdg 
            cnt += 1
        readings = readings[:-1]    #remove last comma
        readings = readings + ']}'
        readings = readings % cnt
    
        return json.dumps(readings)
    except Exception:
        print("EXCEPTION ::::::: " + str(Exception))
        
        
if __name__ == "__main__":
    #main()
    print("json object :::: " + str(build_json()))
