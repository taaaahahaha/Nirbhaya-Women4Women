import json

a = {"SOS": [
        {
            "name": "a",
            "mobile_number": "b",
            "relation": "c"
        },
        {
            "name": "e",
            "mobile_number": "f",
            "relation": "g"
        }
    ]}

for i in a["SOS"]:
    print(i)

x = json.loads(a["SOS"])
print(x)