import json

def clean():
    skills_file = open('./full_skills.json', encoding="utf8")
    skills_arr  = json.load(skills_file)['skills']
    filtered_arr = []


    for skill in skills_arr:
        if len(str(skill)) > 3:
            filtered_arr.append(str(skill))


    new_file = {}
    new_file['skills'] = filtered_arr
    with open('./cleaned_skills.json', 'w') as out:
        json.dump(new_file, out)

clean()
