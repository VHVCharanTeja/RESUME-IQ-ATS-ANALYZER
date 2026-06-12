def generate_rewrite_suggestions(resume_text, missing_skills, selected_role):
    suggestions = []

    suggestions.append(
        f"Tailor your resume summary specifically for the {selected_role} role."
    )

    suggestions.append(
        "Rewrite project descriptions using action verbs like Developed, Built, Designed, Implemented, Optimized."
    )

    suggestions.append(
        "Add measurable results such as accuracy, performance improvement, number of users, or dataset size."
    )

    suggestions.append(
        "Mention technologies clearly inside each project description."
    )

    for skill in missing_skills[:5]:
        suggestions.append(
            f"If you have experience with {skill}, include it in your Skills or Projects section."
        )

    suggestions.append(
        "Add GitHub links for important projects."
    )

    suggestions.append(
        "Avoid vague lines like 'worked on project'. Use specific technical achievements."
    )

    return suggestions