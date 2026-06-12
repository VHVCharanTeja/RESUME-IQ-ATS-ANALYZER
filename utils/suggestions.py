def generate_suggestions(
        missing_skills,
        ats_score):

    suggestions = []

    if ats_score < 40:

        suggestions.append(
            "Resume has low ATS compatibility. Add more role-specific skills."
        )

        suggestions.append(
            "Improve project descriptions with technologies used."
        )

    elif ats_score < 60:

        suggestions.append(
            "Add missing skills to improve ATS score."
        )

        suggestions.append(
            "Include more relevant projects."
        )

    elif ats_score < 80:

        suggestions.append(
            "Good ATS score. Add advanced tools and certifications."
        )

    else:

        suggestions.append(
            "Excellent ATS score. Focus on interview preparation."
        )

    for skill in missing_skills:

        suggestions.append(
            f"Consider adding {skill} if you have practical experience."
        )

    suggestions.append(
        "Add measurable project achievements."
    )

    suggestions.append(
        "Include GitHub repository links."
    )

    suggestions.append(
        "Include LinkedIn profile link."
    )

    suggestions.append(
        "Add certifications relevant to your target role."
    )

    suggestions.append(
        "Use strong action verbs in project descriptions."
    )

    suggestions.append(
        "Keep resume length within 1-2 pages."
    )

    return suggestions