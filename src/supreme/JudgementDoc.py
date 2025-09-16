from dataclasses import dataclass

from utils import Log

from pdf_scraper import AbstractDoc
from supreme.JudgementDocWebMixin import JudgementDocWebMixin

log = Log("JudgementDoc")


@dataclass
class JudgementDoc(JudgementDocWebMixin, AbstractDoc):
    parties: str
    judgement_by: str

    BASE_URL = "https://supremecourt.lk/judgements/"

    @classmethod
    def get_doc_class_label(cls) -> str:
        return "lk_supreme_court_judgements"

    @classmethod
    def get_doc_class_description(cls) -> str:
        return (
            f"Judgements of the [Supreme Court of Sri Lanka]({cls.BASE_URL})."
        )
