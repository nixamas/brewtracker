"""
BEERS
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

BREWERY
{ "page"      : 1,
  "pages"     : 2,
  "total"     : 55,
  "breweries" : [
    { "id"         : 1,
      "name"       : "Abita",
      "url"        : "http://abita.com",
      "created_at" : "2010-01-01T00:00:00Z",
      "updated_at" : "2010-02-02T12:30:00Z"
    },
    ...
  ]
}
"""

import urllib, json

class Beer_Database_Api:
    BEERS_DATABASE = {}
    BREWERIES_DATABASE = {}
    API_URL = "http://api.openbeerdatabase.com/v1/"
    PUBLIC_TOKEN = "900836b50d0021a3e28231767f4f66b4b2e76746d0f5eab80e095adb113a8316"
    PRIVATE_TOKEN = "3876ff0ca2967532f3512366fbb863b309b5e11cf4e05c7c8e760ce099bf9418"
    def __init__(self):
        print("initiating Beer Database Api Object")
        self.fetch_beers()
        self.fetch_breweries()
        #url = "http://api.openbeerdatabase.com/v1/beers/1.json"
        #url = "http://api.openbeerdatabase.com/v1/beers.json"
        #response = urllib.urlopen(API_URL + "beers.json");
        #BEERS_DATABASE = json.loads(response.read())
        #print(str(BEERS_DATABASE["total"]))
        #print(str( BEERS_DATABASE["beers"][0]["name"] ))
        
    def fetch_beers(self):
        print("fetching all beers")
        response = urllib.urlopen(self.API_URL + "beers.json");
        self.BEERS_DATABASE = json.loads(response.read())
        #print(str( self.BEERS_DATABASE ))
        #return BEERS_DATABASE
    
    def fetch_beer(self, beer_id):
        print("fetching beer with id of " +str(beer_id))
        response = urllib.urlopen(self.API_URL + "beers/" + str(beer_id) + ".json");
        return json.loads(response.read())
    
    def fetch_breweries(self):
        print("fetching all breweries")
        response = urllib.urlopen(self.API_URL + "breweries.json")
        self.BREWERIES_DATABASE = json.loads(response.read())
        
    def fetch_brewery(self, brewery_id):
        print("fetching brewery with id of " +str(brewery_id))
        response = urllib.urlopen(self.API_URL + "breweries/" + str(brewery_id) + ".json");
        return json.loads(response.read())
    
    def get_beers(self):
        print("getting beers...")
        return self.BEERS_DATABASE

    def get_beer(self, beer_id):
        print("getting beer with id of " + str(beer_id))
        for beer in self.BEERS_DATABASE["beers"]:
            if beer["id"] == beer_id:
                return beer
            
    def get_breweries(self):
        print("getting beers...")
        return self.BEERS_DATABASE

    def get_brewery(self, brewery_id):
        print("getting beer with id of " + str(brewery_id))
        for brewery in self.BREWERIES_DATABASE['breweries']:
            if brewery["id"] == brewery_id:
                return brewery
            
    def get_beers_from_brewery(self, brewery_id):
        print("getting the beers for brewery :: " + str(brewery_id))
        beers = []
        for beer in self.BEERS_DATABASE["beers"]:
            if beer['brewery']['id'] == brewery_id:
                print("found a match :: " + beer['name'])
                beers.append(beer)
        return beers
        
if __name__ == "__main__":
    bda = Beer_Database_Api()
    b_id = 4
    print("brewery with id " + str(b_id))
    print(str(bda.get_beers_from_brewery(b_id)))
    
    
    
    
    
    