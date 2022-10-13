import json

def read_json():
    "Return json data"
    f = open("./app/data/college.json")
    data = json.load(f)
    return data

def read_json_id(id:int):
    "Return json data with id"
    f = open("./app/data/college.json")
    data = json.load(f)
    return data[id-1]