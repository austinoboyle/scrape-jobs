import json
from datetime import datetime

def resume():
    print("Started at "+ str(datetime.now()))

    # Access resume file
    # resume = open('./examples/ck_resume.txt')
    with open('./examples/ck_resume.txt', 'r') as resumefile:
        resume = resumefile.read() #.replace('\n', '')

    # Access skills file
    skills_file = open('../skills/full_skills.json')
    skills_arr = json.load(skills_file)["skills"]

    req_skills = []
    # Iterate through resume
    for skill in skills_arr:
        # If skill in resume, add to required skills
        if skill in resume:
            req_skills.append(skill)

    # Access jobs file
    jobs_file = open('../skills/jobs_with_skills.json')
    jobs_arr = json.load(jobs_file)

    # Find jobs' similarity
    jobs = []
    for job in jobs_arr:
        closeness = 0
        divisor = 0
        for req in req_skills:
            if req in job['description']:
                closeness += len(req)
                divisor += 1
        if divisor > 5:
            job['similarity'] = (closeness/divisor)
        else:
            job['similarity'] = 0
        jobs.append(job)

    # Sort jobs on decreasing similarity
    sorted_jobs = sorted(jobs, key=lambda k: k['similarity'])
    sorted_jobs.reverse()

    # Print the first 5 jobs
    # for i in range(0, 5):
    #     print("Job Title: " + sorted_jobs[i]['title'])
    #     print("Job Description: " + sorted_jobs[i]['description'])
    #     print("Job Similarity: " + str(sorted_jobs[i]['similarity']))
    #     print("")



    # Dump to json file
    with open('./sorted_jobs.json', 'w') as out:
        json.dump(sorted_jobs[0:10], out)

    print("Finished at "+ str(datetime.now()))

resume()
