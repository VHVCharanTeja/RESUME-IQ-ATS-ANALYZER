import json
from collections import defaultdict

# Load role skills
with open("datasets/roles_skills.json", "r", encoding="utf-8") as file:
    roles_data = json.load(file)

# Load skill synonyms
with open("datasets/skill_synonyms.json", "r", encoding="utf-8") as file:
    skill_synonyms = json.load(file)

# Collect all skills from all roles
all_skills = set()

for skills in roles_data.values():
    for skill in skills:
        all_skills.add(skill)

all_skills = list(all_skills)

# Project/domain pattern detection
project_patterns = {

    "Machine Learning": [
        "classification",
        "regression",
        "clustering",
        "recommendation system",
        "prediction system",
        "fraud detection",
        "customer churn",
        "forecasting"
    ],

    "Deep Learning": [
        "cnn",
        "rnn",
        "lstm",
        "transformer",
        "neural network",
        "image classification",
        "speech recognition"
    ],

    "Computer Vision": [
        "object detection",
        "image processing",
        "image segmentation",
        "face detection",
        "face recognition",
        "vehicle tracking",
        "vehicle detection",
        "video analytics",
        "surveillance"
    ],

    "NLP": [
        "chatbot",
        "sentiment analysis",
        "fake news detection",
        "text classification",
        "question answering",
        "text summarization",
        "language model"
    ],

    "Generative AI": [
        "llm",
        "gpt",
        "gemini",
        "claude",
        "prompt engineering",
        "image generation",
        "text generation",
        "rag"
    ],

    "Data Analysis": [
        "dashboard",
        "reporting",
        "business intelligence",
        "data visualization",
        "power bi",
        "tableau"
    ],

    "Backend Development": [
        "rest api",
        "microservices",
        "authentication",
        "backend development",
        "server side"
    ],

    "Frontend Development": [
        "responsive website",
        "ui development",
        "frontend development",
        "web application",
        "responsive design"
    ],

    "Cloud Computing": [
        "aws",
        "azure",
        "gcp",
        "cloud deployment",
        "serverless"
    ],

    "DevOps": [
        "docker",
        "kubernetes",
        "ci/cd",
        "terraform",
        "jenkins"
    ],

    "Cybersecurity": [
        "penetration testing",
        "vulnerability assessment",
        "threat detection",
        "security analysis",
        "owasp"
    ],

    "Mobile Development": [
        "android application",
        "ios application",
        "flutter app",
        "mobile app"
    ],

    "Database": [
        "database design",
        "sql optimization",
        "data modeling",
        "stored procedures"
    ],

    "QA Testing": [
        "manual testing",
        "automation testing",
        "selenium",
        "test cases",
        "bug tracking"
    ],

    "Business Analysis": [
        "requirement gathering",
        "stakeholder management",
        "process analysis",
        "business requirements"
    ],

    "Product Management": [
        "product roadmap",
        "market research",
        "feature prioritization",
        "product strategy"
    ]
}


def extract_skills(text):

    text = text.lower()

    skill_scores = defaultdict(int)

    # Direct skill matching
    for skill in all_skills:

        count = text.count(skill.lower())

        if count > 0:
            skill_scores[skill] += count

    # Synonym matching
    for main_skill, synonyms in skill_synonyms.items():

        for synonym in synonyms:

            count = text.count(synonym.lower())

            if count > 0:
                skill_scores[main_skill] += count

    # Project/domain pattern matching
    for skill_name, patterns in project_patterns.items():

        for pattern in patterns:

            if pattern.lower() in text:
                skill_scores[skill_name] += 2

    # Sort skills by score
    detected_skills = sorted(
        skill_scores.keys(),
        key=lambda x: skill_scores[x],
        reverse=True
    )

    return detected_skills