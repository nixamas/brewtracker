import json, sqlite3

data = {"firstName": "John","lastName": "Smith","age": 25,
                "address": {
                    "streetAddress": "21 2nd Street",
                    "city": "New York",
                    "state": "NY",
                    "postalCode": 10021
                }
            }
with open('data.js', 'w') as f:
    f.write("var datareadings = ")  #write variable declaration to javascript file
    readings = {}
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
    readings = '{"count":"%s","readings":['     #start of json object
    cnt = 0
    for row in cursor.execute("SELECT rowid, * FROM readings ORDER BY time"):
        rdng = '{"id":"' + str(row[0]) + '","time":"' + str(row[1]) + '","value":"' + str(row[2]) + '"},'
        print (rdng)
        readings = readings + rdng
        cnt += 1
       
    readings = readings[:-1]    #remove last comma
    readings = readings + ']}'
    readings = readings % cnt
    print(str(readings))

    json.dump(readings, f, ensure_ascii=False)
    
    f.write("\n\r")
    f.write("function getDataReadings(){")
    f.write('   console.log("Returning data to analysis.html..."); ')
    f.write('   return datareadings; ')
    f.write("}")