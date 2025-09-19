from dataclasses import dataclass

from utils import Log

from scraper import AbstractPDFDoc
from supreme.JudgementDocWebMixin import JudgementDocWebMixin

log = Log("JudgementDoc")


@dataclass
class JudgementDoc(JudgementDocWebMixin, AbstractPDFDoc):
    parties: str
    judgement_by: str

    BASE_URL = "https://supremecourt.lk/judgements/"

    @classmethod
    def get_doc_class_description(cls) -> str:
        return "\n\n".join(
            [
                "A Supreme Court judgement is the final and binding decision delivered by the highest court in a country.",  # noqa: E501
                "In Sri Lanka, the Supreme Court plays a vital role in interpreting the Constitution, safeguarding fundamental rights, and resolving disputes of national importance. Its judgements set legal precedents that influence how laws are applied and upheld across the nation, shaping both governance and society.",  # noqa: E501
            ]
        )

    @classmethod
    def get_doc_class_emoji(cls) -> str:
        return "⚖️"
