import json

def combine():
    # Access files
    city_file = open('./json_files/city_jobs.json')
    queens_file = open('./json_files/queens_jobs.json')
    keys_file = open('./json_files/keys_jobs.json')
    kgh_file = open('./json_files/kgh_jobs.json')
    indeed_file = open('./json_files/indeed_jobs.json')
    slc_file = open('./json_files/slc_jobs.json')
    glassdoor_file = open('./json_files/glassdoor_jobs.json')

    # Read into array
    city_arr = json.load(city_file)
    queens_arr = json.load(queens_file)
    keys_arr = json.load(keys_file)
    kgh_arr = json.load(kgh_file)
    indeed_arr = json.load(indeed_file)
    slc_arr  = json.load(slc_file)
    glassdoor_arr  = json.load(glassdoor_file)

    # Join arrays
    full_arr = city_arr + queens_arr + keys_arr + kgh_arr + indeed_arr + slc_arr + glassdoor_arr

    # Dump to json file
    with open('./json_files/combined_jobs.json', 'w') as out:
        json.dump(full_arr, out)
