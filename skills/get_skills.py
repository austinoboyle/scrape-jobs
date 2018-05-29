import json

def get_skills():
    # Access jobs file
    jobs_file = open('../json_files/glassdoor_jobs.json')

    # Access skills file
    skills_file = open('./full_skills_list.json')

    # Read both files into independant arrays
    jobs_arr = json.load(jobs_file)
    skills_arr = json.load(skills_file)["skills"]

    # Iterate through every job
    for job in jobs_arr:
        # Instantiate an empty required skills array
        req_skills = []
        for skill in skills_arr:
            # If skill in description, add to required skills
            if skill.lower() in job['description'].lower():
                req_skills.append(skill)
        # Add to skills section of job
        job['skills'] = req_skills

    # Dump to json file
    with open('./jobs_with_skills.json', 'w') as out:
        json.dump(jobs_arr, out)

get_skills()
