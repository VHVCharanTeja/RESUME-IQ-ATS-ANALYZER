import json

with open("datasets/roles_skills.json", "r") as file:
    roles_data = json.load(file)


def calculate_ats_score(selected_role, detected_skills):

    required_skills = roles_data[selected_role]

    matched_skills = []

    missing_skills = []

    for skill in required_skills:

        if skill in detected_skills:
            matched_skills.append(skill)

        else:
            missing_skills.append(skill)

    score = (len(matched_skills) / len(required_skills)) * 100

    return round(score, 2), matched_skills, missing_skills