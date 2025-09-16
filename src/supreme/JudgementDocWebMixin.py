import time
from typing import Generator

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from utils import Log

from pdf_scraper import AbstractDoc

log = Log("JudgementDocWebMixin")


class JudgementDocWebMixin:
    T_SLEEP = 3

    @classmethod
    def __parse_tr__(cls, tr):
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
    def __parse_pager__(cls, driver) -> Generator[AbstractDoc, None, None]:
        table = driver.find_elements(By.XPATH, "//table")[1]
        trs = table.find_elements(By.TAG_NAME, "tr")
        assert len(trs) >= 1
        for tr in trs:
            doc = cls.__parse_tr__(tr)
            if doc:
                yield doc

    @classmethod
    def sleep(cls):
        log.debug(f"😴 {cls.T_SLEEP}s...")
        time.sleep(cls.T_SLEEP)

    @classmethod
    def get_driver(cls):
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
                a_next.click()
                cls.sleep()

            except Exception as e:
                log.error(f"Error occurred while clicking 'Next': {e}")
                break
        driver.quit()
