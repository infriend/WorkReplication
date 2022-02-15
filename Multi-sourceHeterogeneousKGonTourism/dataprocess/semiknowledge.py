import json


with open("./data/testdata/semi_structure_test.json") as f:
    text = f.read()
    jsondata = json.loads(text)

def semi_extract():
    triples = set()
    entities = set()
    keys = list(jsondata)
    for k in keys:
        if "scenic" in jsondata[k]:
            sceniclist = jsondata[k]["scenic"]
            for s in sceniclist:
                if "scenic" in s:
                    scenic = s["scenic"].replace(" ", "").replace("\n", "")
                    triples.add(scenic + ' ' + 'at' + ' ' + k + '\n')
                    entities.add(scenic+'\n')
                    if "location" in s:
                        location = s["location"].replace(" ", "").replace("\n", "")
                        triples.add(scenic + ' ' + 'at' + ' ' + location + '\n')
                        entities.add(location+'\n')
        if "food" in jsondata[k]:
            foodlist = jsondata[k]["food"]
            for f in foodlist:
                if "name" in f:
                    food = f["name"].replace(" ", "").replace("\n", "")
                    triples.add(food + ' ' + 'at' + ' ' + k + '\n')
                    entities.add(food+'\n')
        if "restaurant" in jsondata[k]:
            restaurantlist = jsondata[k]["restaurant"]
            for r in restaurantlist:
                if "name" in r:
                    restaurant = r["name"].replace(" ", "").replace("\n", "")
                    triples.add(restaurant + ' ' + 'at' + ' ' + k + '\n')
                    entities.add(restaurant+'\n')

        return triples, entities
