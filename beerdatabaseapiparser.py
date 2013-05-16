# { "page"  : 1,
  # "pages" : 2,
  # "total" : 55,
  # "beers" : [
    # { "id"          : 1,
      # "name"        : "Strawberry Harvest",
      # "description" : "Strawberry Harvest Lager is a wheat beer ...",
      # "abv"         : 4.2,
      # "created_at"  : "2010-01-01T00:00:00Z",
      # "updated_at"  : "2010-02-02T12:30:00Z",
      # "brewery"     : {
        # "id"   : 1,
        # "name" : "Abita"
      # }
    # },
    # ...
  # ]
# }

import urllib, json

class Beer_Database_Api:
    DATABASE_OBJ = {}
    API_URL = "http://api.openbeerdatabase.com/v1/"
    PUBLIC_TOKEN = "900836b50d0021a3e28231767f4f66b4b2e76746d0f5eab80e095adb113a8316"
    PRIVATE_TOKEN = "3876ff0ca2967532f3512366fbb863b309b5e11cf4e05c7c8e760ce099bf9418"
    def __init__(self):
        print("initiating Beer Database Api Object")
        self.fetch_beers()
        #url = "http://api.openbeerdatabase.com/v1/beers/1.json"
        #url = "http://api.openbeerdatabase.com/v1/beers.json"
        #response = urllib.urlopen(API_URL + "beers.json");
        #DATABASE_OBJ = json.loads(response.read())
        #print(str(DATABASE_OBJ["total"]))
        #print(str( DATABASE_OBJ["beers"][0]["name"] ))
        
    def fetch_beers(self):
        print("fetching all beers")
        response = urllib.urlopen(self.API_URL + "beers.json");
        self.DATABASE_OBJ = json.loads(response.read())
        #print(str( self.DATABASE_OBJ ))
        #return DATABASE_OBJ
    
    def fetch_beer(self, id):
        print("fetching beer with id of " +str(id))
        response = urllib.urlopen(self.API_URL + "beers/" + str(id) + ".json");
        return json.loads(response.read())
        
    def get_beers(self):
        print("getting beers...")
        return self.DATABASE_OBJ

    def get_beer(self, id):
        print("getting beer with id of " + str(id))
        for beer in self.DATABASE_OBJ["beers"]:
            if beer["id"] == id:
                return beer
    
if __name__ == "__main__":
    bda = Beer_Database_Api()
    #bda.fetch_beers();
    #print(str(bda.fetch_beer(2)))
    print(str(bda.get_beer(2).description))
    
    
    
    
    
    