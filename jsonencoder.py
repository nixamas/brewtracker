import json, sqlite3

def main():
    with open('data.js', 'w') as f:
        f.write("var datareadings = ")  #write variable declaration to javascript file
        readings = {}
        conn = sqlite3.connect("mydatabase.db")
        cursor = conn.cursor()
        readings = '{"count":"%s","readings":['     #start of json object
        cnt = 0
        for row in cursor.execute("SELECT rowid, * FROM readings ORDER BY time"):
            rdng = '{"id":"' + str(row[0]) + '","time":"' + str(row[1]) + '","value":"' + str(row[2]) + '"},'
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
        
if __name__ == "__main__":
    main()