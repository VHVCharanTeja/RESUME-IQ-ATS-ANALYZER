def get_strengths_weaknesses(
        matched_skills,
        missing_skills):

    strengths = matched_skills[:5]
    weaknesses = missing_skills[:5]

    return strengths, weaknesses