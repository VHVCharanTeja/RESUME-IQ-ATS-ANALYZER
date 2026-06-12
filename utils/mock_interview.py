
import re

def evaluate_answer(user_answer, ideal_answer):

    user_answer = user_answer.lower().strip()
    ideal_answer = ideal_answer.lower().strip()

    # Empty answer
    if not user_answer:
        return 0, "No answer entered. Score: 0/10"

    # Very short answer
    if len(user_answer) < 20:
        return 0, "Answer is too short. Explain the concept properly."

    user_words = set(re.findall(r'\w+', user_answer))
    ideal_words = set(re.findall(r'\w+', ideal_answer))

    matched_words = user_words.intersection(ideal_words)

    match_ratio = len(matched_words) / max(len(ideal_words), 1)

    score = round(match_ratio * 10)

    score = min(max(score, 0), 10)

    if score >= 8:
        feedback = "Excellent answer. You covered most important concepts."

    elif score >= 6:
        feedback = "Good answer. Add a few more technical details."

    elif score >= 4:
        feedback = "Average answer. Include examples and key terms."

    else:
        feedback = "Needs improvement. Explain the concept more clearly."

    return score, feedback

