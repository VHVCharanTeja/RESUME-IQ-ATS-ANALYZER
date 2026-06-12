import json
import os

ROLE_FILE_MAP = {
    "AI Engineer": "ai_engineer.json",
    "Machine Learning Engineer": "ml_engineer.json",
    "Data Scientist": "data_scientist.json",
    "Data Analyst": "data_analyst.json",
    "NLP Engineer": "nlp_engineer.json",
    "Computer Vision Engineer": "computer_vision_engineer.json",
    "Generative AI Engineer": "generative_ai_engineer.json",
    "Python Developer": "python_developer.json",
    "Java Developer": "java_developer.json",
    "Frontend Developer": "frontend_developer.json",
    "Backend Developer": "backend_developer.json",
    "Full Stack Developer": "fullstack_developer.json",
    "DevOps Engineer": "devops_engineer.json",
    "Cloud Engineer": "cloud_engineer.json",
    "Site Reliability Engineer": "sre_engineer.json",
    "Cybersecurity Analyst": "cybersecurity_analyst.json",
    "Ethical Hacker": "ethical_hacker.json",
    "SQL Developer": "sql_developer.json",
    "Database Administrator": "database_administrator.json",
    "Android Developer": "android_developer.json",
    "Flutter Developer": "flutter_developer.json",
    "QA Engineer": "qa_engineer.json",
    "Automation Tester": "automation_tester.json",
    "Business Analyst": "business_analyst.json",
    "Product Manager": "product_manager.json"
}

def get_answers(role):

    file_name = ROLE_FILE_MAP.get(role)

    if not file_name:
        return {}

    file_path = os.path.join(
        "datasets",
        "interview_answers",
        file_name
    )

    if not os.path.exists(file_path):
        return {}

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data