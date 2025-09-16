from dataclasses import dataclass
from typing import Generator

from selenium import webdriver
from selenium.webdriver.common.by import By
from utils import Log

from pdf_scraper import AbstractDoc

log = Log("JudgementDoc")


@dataclass
class JudgementDoc(AbstractDoc):
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
    def __parse_tr__(cls, tr) -> "JudgementDoc":
        tds = tr.find_elements(By.TAG_NAME, "td")
        if len(tds) == 0:
            return None
        assert len(tds) == 7
        td_text_list = [td.text for td in tds]

        # num
        num = td_text_list[1]
        assert num.startswith("SC/")

        # date_str
        date_str = td_text_list[0]
        assert len(date_str) == 10

        # url_pdf
        td_final = tds[-1]
        url_pdf = td_final.find_element(By.TAG_NAME, "a").get_attribute("href")
        assert url_pdf.endswith(".pdf")

        return cls(
            num=num,
            date_str=date_str,
            description="",
            url_pdf=url_pdf,
            url_metadata=cls.BASE_URL,
            parties=td_text_list[2],
            judgement_by=td_text_list[3],
        )

    @classmethod
    def gen_docs(cls) -> Generator["JudgementDoc", None, None]:
        driver = webdriver.Firefox()
        log.debug(f"🌐 Openning {cls.BASE_URL}...")
        driver.get(cls.BASE_URL)

        table = driver.find_elements(By.XPATH, "//table")[1]
        trs = table.find_elements(By.TAG_NAME, "tr")
        assert len(trs) >= 1
        for tr in trs:
            doc = cls.__parse_tr__(tr)
            if doc:
                yield doc

        driver.quit()
