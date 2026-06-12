def generate_learning_roadmap(missing_skills, selected_role):
    roadmap = []

    roadmap.append(f"Learning roadmap for {selected_role}")

    if not missing_skills:
        roadmap.append("You already match most required skills. Focus on advanced projects and interview practice.")
        return roadmap

    for skill in missing_skills[:5]:
        roadmap.append(f"Learn {skill} basics")
        roadmap.append(f"Build one small project using {skill}")
        roadmap.append(f"Add {skill} to your resume only after practicing it")

    roadmap.append("Update your resume after completing missing skills.")
    roadmap.append("Push related projects to GitHub.")
    roadmap.append("Practice interview questions for this role.")

    return roadmap