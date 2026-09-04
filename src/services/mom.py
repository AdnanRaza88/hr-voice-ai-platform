from typing import Dict, Optional

from langchain_core.prompts import ChatPromptTemplate

from src.core.config import get_settings
from src.core.llm import build_chat_model, clear_llm_cache


MOM_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You produce clean Minutes of Meeting. "
            "Return structured output with: summary, key_points (bullet list), "
            "action_items (each with owner and task), and decisions. "
            "Be concise and professional. Use plain text sections.",
        ),
        (
            "human",
            "Meeting transcript:\n\n{transcript}\n\nProduce the minutes.",
        ),
    ]
)


class MOMService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self._llm = None

    @property
    def llm(self):
        if self._llm is None:
            self._llm = build_chat_model(temperature=0.1, max_tokens=1024)
        return self._llm

    def reset_llm(self) -> None:
        self._llm = None
        clear_llm_cache()

    def generate(self, transcript: str) -> Dict[str, str]:
        if not transcript.strip():
            return {
                "summary": "",
                "key_points": "",
                "action_items": "",
                "decisions": "",
                "raw": "",
            }
        chain = MOM_PROMPT | self.llm
        response = chain.invoke({"transcript": transcript})
        text = response.content if hasattr(response, "content") else str(response)
        return {
            "summary": text,
            "key_points": "",
            "action_items": "",
            "decisions": "",
            "raw": text,
        }


_mom_service: Optional[MOMService] = None


def get_mom_service() -> MOMService:
    global _mom_service
    if _mom_service is None:
        _mom_service = MOMService()
    return _mom_service
