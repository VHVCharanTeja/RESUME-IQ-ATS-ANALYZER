def calculate_resume_rating(
        ats_score,
        jd_score,
        matched_skills,
        missing_skills):

    total_skills = len(matched_skills) + len(missing_skills)

    if total_skills > 0:
        skill_score = (len(matched_skills) / total_skills) * 100
    else:
        skill_score = 0

    final_score = (
        ats_score * 0.5 +
        jd_score * 0.2 +
        skill_score * 0.3
    )

    rating = round(final_score / 10, 1)

    if rating >= 9:
        verdict = "Excellent Resume"
    elif rating >= 8:
        verdict = "Very Good Resume"
    elif rating >= 7:
        verdict = "Good Resume"
    elif rating >= 6:
        verdict = "Average Resume"
    else:
        verdict = "Needs Improvement"

    return rating, verdict


def calculate_improvement_potential(
        ats_score,
        missing_skills):

    possible_gain = min(
        len(missing_skills) * 8,
        40
    )

    improved_score = min(
        ats_score + possible_gain,
        100
    )

    return possible_gain, improved_score