from dataclasses import dataclass
from functools import cached_property

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
    def get_doc_class_description(cls) -> str:
        return (
            f"Judgements of the [Supreme Court of Sri Lanka]({cls.BASE_URL})."
        )

    @cached_property
    def parties_short(self) -> str:
        if len(self.parties) > 32:
            return self.parties[:29] + "..."
        return self.parties

    # HACK!
    @classmethod
    def get_lines_for_latest_docs(cls):
        lines = [f"## {cls.N_LATEST} Latest documents", ""]
        for doc in cls.list_all()[: cls.N_LATEST]:
            line = "- " + " | ".join(
                [
                    doc.date_str,
                    f"`{doc.num}`",
                    doc.parties_short,
                    doc.judgement_by,
                    f"[data]({doc.remote_data_url})",
                ]
            )
            lines.append(line)
        lines.append("")
        return lines
