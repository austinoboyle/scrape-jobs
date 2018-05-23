import json

def combine():
    # Access files
    city_file = open('./json_files/city_jobs.json')
    queens_file = open('./json_files/queens_jobs.json')
    keys_file = open('./json_files/keys_jobs.json')
    kgh_file = open('./json_files/kgh_jobs.json')
    indeed_file = open('./json_files/indeed_jobs.json')
    slc_file = open('./json_files/slc_jobs.json')

    # Read into array
    city_arr = json.load(city_file)
    queens_arr = json.load(queens_file)
    keys_arr = json.load(keys_file)
    kgh_arr = json.load(kgh_file)
    indeed_arr = json.load(indeed_file)
    slc_arr  = json.load(slc_file)

    # Join arrays
    full_arr = city_arr + queens_arr + keys_arr + kgh_arr + indeed_arr + slc_arr

    # Dump to json file
    with open('./json_files/combined_jobs.json', 'w') as out:
        json.dump(full_arr, out)

    # Build .js version
    VAR_NAME = 'data'
    file_text = 'export const {} = '.format(VAR_NAME)
    file_text += str(full_arr)
    file_text += ';'

    # Dump to .js file
    with open('./json_files/combined_jobs.js', 'w') as out:
        out.write(file_text)
