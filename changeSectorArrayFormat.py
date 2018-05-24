import json

with open('./sectors.json', 'r') as f:
    sectorsDict = json.load(f)

sectors = []
for key in sectorsDict:
    sectors.append({
        'name': key,
        'relevantWords': sectorsDict[key]
    })

with open('./sector_list.json', 'w') as f:
    json.dump(sectors, f)
