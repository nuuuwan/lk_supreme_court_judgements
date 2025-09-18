import time
from typing import Generator

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from utils import Log

from scraper import AbstractDoc

log = Log("JudgementDocWebMixin")


class JudgementDocWebMixin:
    T_SLEEP = 3

    @classmethod
    def __parse_tr__(cls, tr):
        tds = tr.find_elements(By.TAG_NAME, "td")
        if len(tds) == 0:
            return None
        td_text_list = [td.text for td in tds]
        assert len(td_text_list) == 7, td_text_list

        # num
        num = td_text_list[1]
        assert num.startswith("SC") or num.startswith("CS"), num

        # date_str
        date_str = td_text_list[0]
        assert len(date_str) == 10, date_str

        # url_pdf
        td_final = tds[-1]
        url_pdf = td_final.find_element(By.TAG_NAME, "a").get_attribute("href")
        assert url_pdf.endswith(".pdf"), url_pdf

        # judgement_by, parties, description
        judgement_by = td_text_list[3]
        parties = td_text_list[2]
        max_parties_len = 32
        parties_short = parties
        if len(parties) > max_parties_len:
            parties_short = parties[: max_parties_len - 3] + "..."
        description = f"{judgement_by} - {parties_short}"

        return cls(
            num=num,
            date_str=date_str,
            description=description,
            url_metadata=cls.BASE_URL,
            lang="en",
            url_pdf=url_pdf,
            parties=parties,
            judgement_by=judgement_by,
        )

    @classmethod
    def __parse_pager__(cls, driver) -> Generator[AbstractDoc, None, None]:
        table = driver.find_elements(By.XPATH, "//table")[1]
        trs = table.find_elements(By.TAG_NAME, "tr")
        assert len(trs) >= 1
        for tr in trs:
            try:
                doc = cls.__parse_tr__(tr)
                if doc:
                    yield doc
            except Exception as e:
                log.error(f"Error occurred while parsing tr: {e}")

    @classmethod
    def sleep(cls):
        log.debug(f"😴 {cls.T_SLEEP}s...")
        time.sleep(cls.T_SLEEP)

    @classmethod
    def get_driver(cls) -> webdriver.Chrome:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1280,12800")
        return webdriver.Chrome(options=options)

    @classmethod
    def gen_docs(cls) -> Generator[AbstractDoc, None, None]:
        driver = cls.get_driver()

        log.debug(f"🌐 Openning {cls.BASE_URL}...")
        driver.get(cls.BASE_URL)
        i_page = 0
        while True:
            i_page += 1
            log.debug(f"{i_page=}")
            for doc in cls.__parse_pager__(driver):
                yield doc

            try:
                a_next = driver.find_element(By.LINK_TEXT, "Next")
                if not a_next:
                    break
                if "disabled" in a_next.get_attribute("class"):
                    break
                a_next.click()
                cls.sleep()

            except Exception as e:
                log.error(f"Error occurred while clicking 'Next': {e}")
                break
        driver.quit()
