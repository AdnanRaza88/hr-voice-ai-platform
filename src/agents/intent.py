from typing import Literal

IntentType = Literal["screening_answer", "policy_question", "meeting", "end", "other", "unknown"]

POLICY_KEYWORDS = {
    "policy", "policies", "hours", "timing", "leave", "remote", "work from home",
    "salary structure", "benefits", "holiday", "working days", "office",
}

END_KEYWORDS = {"bye", "goodbye", "end call", "stop", "thank you bye", "that's all"}


def classify_intent(text: str, in_screening: bool = True) -> IntentType:
    lowered = text.lower().strip()
    if not lowered:
        return "unknown"
    if any(k in lowered for k in END_KEYWORDS):
        return "end"
    if any(k in lowered for k in POLICY_KEYWORDS):
        return "policy_question"
    if in_screening:
        return "screening_answer"
    return "other"
