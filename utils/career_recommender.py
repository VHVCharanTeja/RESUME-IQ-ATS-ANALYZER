def recommend_roles(skills):

    skills = [s.lower() for s in skills]

    role_scores = {}

    def add_score(role, score):
        role_scores[role] = role_scores.get(role, 0) + score

    # AI / ML
    if "machine learning" in skills:
        add_score("Machine Learning Engineer", 10)

    if "deep learning" in skills:
        add_score("Deep Learning Engineer", 10)

    if "generative ai" in skills:
        add_score("Generative AI Engineer", 10)

    if "nlp" in skills:
        add_score("NLP Engineer", 10)

    if "computer vision" in skills:
        add_score("Computer Vision Engineer", 10)

    if "machine learning" in skills and "deep learning" in skills:
        add_score("AI Engineer", 15)

    # Data
    if "python" in skills:
        add_score("Python Developer", 8)

    if "sql" in skills:
        add_score("Database Developer", 8)

    if "analytics" in skills:
        add_score("Data Analyst", 8)

    if "analytics" in skills and "machine learning" in skills:
        add_score("Data Scientist", 12)

    # Cloud
    if "aws" in skills or "azure" in skills:
        add_score("Cloud Engineer", 8)

    if "docker" in skills or "kubernetes" in skills:
        add_score("DevOps Engineer", 8)

    if len(role_scores) == 0:
        return ["Software Engineer"]

    sorted_roles = sorted(
        role_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return [role for role, score in sorted_roles[:5]]