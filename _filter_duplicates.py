import json

def filter():
    # Access combined jobs file
    jobs_file = open('./json_files/combined_jobs.json')

    # Read into array
    jobs_arr = json.load(jobs_file)

    # Add to filtered array if it is not already in
    filtered_arr = []

    # Iterate through every job
    for job in jobs_arr:
        dup = False
        for filtered_job in filtered_arr:
            # Check against each element in filtered jobs array
            if job['title'] == filtered_job['title'] and job['company'] == filtered_job['company']:
                dup = True
                pass
        # If not in filtered jobs, append it
        if dup == False:
            filtered_arr.append(job)

    # Dump to json file
    with open('./json_files/jobs.json', 'w') as out:
        json.dump(filtered_arr, out)
