import re


def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9+#.\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


def extract_jd_skills(jd_text, role_skills):
    jd_text = clean_text(jd_text)

    found_skills = []

    for skill in role_skills:
        skill_text = skill.lower()

        if skill_text in jd_text:
            found_skills.append(skill)

    return list(set(found_skills))


def calculate_jd_match(resume_skills, jd_skills):
    resume_skills_lower = [skill.lower() for skill in resume_skills]

    matched = []
    missing = []

    for skill in jd_skills:
        if skill.lower() in resume_skills_lower:
            matched.append(skill)
        else:
            missing.append(skill)

    if len(jd_skills) == 0:
        score = 0
    else:
        score = round((len(matched) / len(jd_skills)) * 100)

    return score, matched, missing