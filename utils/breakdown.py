def calculate_breakdown(
        matched_skills,
        missing_skills,
        detected_skills,
        jd_score):

    total_required = len(matched_skills) + len(missing_skills)

    if total_required == 0:
        technical_score = 0
    else:
        technical_score = round(
            (len(matched_skills) / total_required) * 100
        )

    project_score = min(
        round((len(detected_skills) / 15) * 100),
        100
    )

    tool_score = min(
        round((len(detected_skills) / 10) * 100),
        100
    )

    role_match = technical_score

    return {
        "Technical Skills": technical_score,
        "Projects": project_score,
        "Tools": tool_score,
        "Role Match": role_match,
        "JD Match": jd_score
    }