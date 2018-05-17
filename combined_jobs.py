import json

city_file = open('city_jobs.json')
queens_file = open('queens_jobs.json')
keys_file = open('keys_jobs.json')
#kgh_file = open('queens_jobs.json')

city_arr = json.load(city_file)
queens_arr = json.load(queens_file)
keys_arr = json.load(keys_file)
#kgh_arr = json.load(kgh_file)

full_arr = city_arr + queens_arr + keys_arr  # +kgh_arr

with open('combined_jobs.json', 'w') as out:
    json.dump(full_arr, out)
