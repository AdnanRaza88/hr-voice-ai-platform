from typing import Dict, List, Tuple

SCREENING_QUESTIONS: List[Tuple[str, str]] = [
    ("full_name", "May I have your full name please?"),
    ("experience_years", "How many years of relevant experience do you have?"),
    ("current_location", "Which city are you currently based in?"),
    ("expected_salary", "What is your expected monthly salary in PKR?"),
    ("availability", "What is your notice period or earliest availability?"),
]


def get_question(index: int) -> Tuple[str, str] | None:
    if 0 <= index < len(SCREENING_QUESTIONS):
        return SCREENING_QUESTIONS[index]
    return None


def extract_field(field: str, answer: str) -> str:
    cleaned = answer.strip()
    if field == "experience_years":
        digits = "".join(ch if ch.isdigit() or ch == "." else " " for ch in cleaned)
        parts = [p for p in digits.split() if p]
        return parts[0] if parts else cleaned
    return cleaned


def next_screening_step(
    current_index: int,
    user_answer: str,
    collected: Dict[str, str],
) -> Tuple[int, Dict[str, str], str, bool]:
    data = dict(collected)
    if current_index < 0:
        current_index = 0
    if current_index < len(SCREENING_QUESTIONS) and user_answer:
        field, _ = SCREENING_QUESTIONS[current_index]
        data[field] = extract_field(field, user_answer)
        current_index += 1
    if current_index >= len(SCREENING_QUESTIONS):
        return current_index, data, "Thank you. We have recorded your details. Our team will contact you soon.", True
    _, question = SCREENING_QUESTIONS[current_index]
    return current_index, data, question, False
