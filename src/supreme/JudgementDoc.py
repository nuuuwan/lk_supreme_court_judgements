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
    def get_doc_class_label(cls) -> str:
        return "lk_supreme_court_judgements"

    @classmethod
    def get_doc_class_description(cls) -> str:
        return (
            f"Judgements of the [Supreme Court of Sri Lanka]({cls.BASE_URL})."
        )

    @classmethod
    def get_remote_data_url_base(cls) -> str:
        return "/".join(
            [
                "https://github.com",
                "nuuuwan",
                "lk_supreme_court_judgements",
                "tree",
                "data",  # branch-name
            ]
        )

    @cached_property
    def remote_data_url(self) -> str:
        return "/".join(
            [
                self.get_remote_data_url_base(),
                self.__class__.get_dir_docs_for_cls_relative(),
                self.dir_doc_relative_to_class,
            ]
        )
