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
                "A Supreme Court judgment is a binding legal decision that interprets the Constitution and laws, shaping justice, governance, and citizens’ rights.",  # noqa: E501
            ]
        )

    @classmethod
    def get_doc_class_emoji(cls) -> str:
        return "⚖️"
