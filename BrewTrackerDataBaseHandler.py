"""

        

"""
import sqlite3, json

class HomeBrewTrackerDataBase():
    CONN = sqlite3.connect("brewtrackerdb.db")
    def __init__(self):
        print("initializing the HomeBrewTrackerDataBase")
        
    def create_new_beer(self, name, ingredients, brew_date, second_stage_date, bottle_date, abv, volume_brewed, notes):
        print("create_new_beer")
        print(str(name) + str(ingredients) + str(brew_date) + 
              str(second_stage_date) + str(bottle_date) + str(abv) + str(volume_brewed) + str(notes) )
        conn = sqlite3.connect("brewtrackerdb.db")
        cursor = conn.cursor()
        sql = "INSERT INTO mybeer (name, ingredients, brew_date, second_stage_date, bottle_date, abv, volume_brewed, notes) VALUES ('"
        sql = sql + str(name) + "', '" + str(ingredients) + "', '" + str(brew_date) + "', '" + str(second_stage_date) + "', '"
        sql = sql + str(bottle_date) + "', '" + str(abv) + "', '" + str(volume_brewed) + "', '" + str(notes) + "')"
        cursor.execute(sql)
        #file_entry = cursor.execute('last_insert_rowid()')
        conn.commit()
        return cursor.lastrowid
        
    def update_my_beer(self, brew_id, name, ingredients, brew_date, second_stage_date, bottle_date, abv, volume_brewed, notes):
        print("updating beer :: " + str(brew_id))
        print(str(name) + str(ingredients) + str(brew_date) + 
              str(second_stage_date) + str(bottle_date) + str(abv) + str(volume_brewed) + str(notes) )
        conn = sqlite3.connect("brewtrackerdb.db")
        cursor = conn.cursor()
        sql = "UPDATE mybeer SET name='" + str(name) + "', ingredients='" + str(ingredients) + "', brew_date='" + str(brew_date) + "', second_stage_date='" + str(second_stage_date) 
        sql = sql + "', bottle_date='" + str(bottle_date) + "', abv='" + str(abv) + "', volume_brewed='" + str(volume_brewed) + "', notes='" + str(notes) + "' "
        sql = sql + "WHERE id='" + str(brew_id) + "'"
        cursor.execute(sql)
        conn.commit()
    
    def get_beer_by_id(self, id):
        print("getting beer by id :: " + str(id) )
        conn = sqlite3.connect("brewtrackerdb.db")
        cursor = conn.cursor()
        query_result = cursor.execute("SELECT * FROM mybeer WHERE id='" + str(id) + "'")
        my_beer = ""
        for result in query_result:
            print(str(result[0]) + "    " + str(result[1]) + str(result[2]) + str(result[3]))
            my_beer = result
            print(str(my_beer))
        return my_beer
    
    def get_all_my_brews(self):
        print("getting all my beer")
        conn = sqlite3.connect("brewtrackerdb.db")
        cursor = conn.cursor()
        beers = []
        for beer in cursor.execute("SELECT * FROM mybeer ORDER BY id ASC"):
            #print(beer)
            b = {}
            b['id'] = beer[0]
            b['name'] = beer[1]
            b['ingredients'] = beer[2]
            b['brew_date'] = beer[3]
            b['second_stage_date'] = beer[4]
            b['bottle_date'] = beer[5]
            b['abv'] = beer[6]
            b['volume_brewed'] = beer[7]
            b['notes'] = beer[8]
            beers.append(b)
            #print(str(beer))
        return beers
    
    def parse_and_insert_gravity_readings(self, brew_id, gravity_reading_string):
        print("parse and insert gravity readings")
        conn = sqlite3.connect("brewtrackerdb.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM gravity_readings WHERE brew_id='" + str(brew_id) + "'")
        conn.commit()
        rdngs = gravity_reading_string.split('#')
        for rdng in rdngs:
            if rdng:
                params = rdng.split(';')
                if params:
                    print("inserting ~~~ " + str(params))
                    self.create_new_gravity_reading(brew_id, params[0], params[1], params[2])
        
    def create_new_gravity_reading(self, brew_id, gr_id, gravity_reading_time, gravity_reading):
        print("create_new_gravity_reading")
        print(str(gravity_reading_time) + str(gravity_reading))
        conn = sqlite3.connect("brewtrackerdb.db")
        cursor = conn.cursor()
        sql = "INSERT INTO gravity_readings (brew_id, id, gravity_reading_time, gravity_reading) VALUES ('"
        sql = sql + str(brew_id) + "', '" + str(gr_id) + "', '" + str(gravity_reading_time) + "', '" + str(gravity_reading) + "')"
        print("sql ~~ " + sql)
        cursor.execute(sql)
        conn.commit()
        
    def get_gravity_readings_for_beer(self, beer_id):
        print("getting gravity readings")
        conn = sqlite3.connect("brewtrackerdb.db")
        cursor = conn.cursor()
        gravity_readings = []
        for reading in cursor.execute("SELECT * FROM gravity_readings WHERE brew_id='" + str(beer_id) + "'"):
            rdng = {}
            rdng['id'] = reading[1]
            rdng['gravity_reading_time'] = reading[2]
            rdng['gravity_reading'] = reading[3]
            gravity_readings.append(rdng)
        return gravity_readings
            
    def delete_brew(self, brew_id):
        print("deleting brew from database :: " + str(brew_id))
        conn = sqlite3.connect("brewtrackerdb.db")
        cursor = conn.cursor()
        sql = "DELETE FROM mybeer WHERE id='" + str(brew_id) + "'"
        cursor.execute(sql)
        conn.commit()
        
if __name__ == "__main__":

    handler = HomeBrewTrackerDataBase()
    
    gr_str = "0;2013-05-27 22:18:17;1.0109#1;2013-05-28 22:18:17;1.0003#"
    
    handler.parse_and_insert_gravity_readings(1, gr_str)
    
    #myid = handler.create_new_beer("name", "ingredients", "brew_date", "second_stage_date", "bottle_date", "abv", "volume", "notes")
    #print("my id :::::::::: " + str(myid))
#    handler.create_new_beer("name1", "ingredients1", "brew_date1", "second_stage_date1", "bottle_date1", "abv1", "volume1", "notes1")
#    handler.get_beer_by_id(4)
#    handler.create_new_gravity_reading(2, "gravity_reading_time", "gravity_reading")
#    handler.create_new_gravity_reading(2, "gravity_reading_time1", "gravity_reading1")
#    handler.create_new_gravity_reading(2, "gravity_reading_time2", "gravity_reading2")
#    readings = handler.get_gravity_readings_for_beer(2)
#    print(str(readings))
    #beers = handler.get_all_my_beer()
    #print(str(json.dumps(beers)))
    
    