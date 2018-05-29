import json

def sort_skills():
    # Access skills file
    skills_file = open('./full_skills_list.json')

    # Read both files into independant arrays
    skills_arr = json.load(skills_file)["skills"]

    # List of all skills
    skills = []
    # Iterate through every skill
    for skill in skills_arr:
        # Add to list if not already
        if skill not in skills:
            skills.append(skill)

    # Sort list alphabetically
    skills.sort()
    skills_dict = {}
    skills_dict["skills"] = skills

    # Dump to json file
    with open('./full_skills_list.json', 'w') as out:
        json.dump(skills_dict, out)

sort_skills()
