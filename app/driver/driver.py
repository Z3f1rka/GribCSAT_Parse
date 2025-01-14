import json
import time

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium_stealth import stealth
import undetected_chromedriver as uc


class Driver:
    def __init__(self) -> None:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.card = {"file": []}
        self.driver = uc.Chrome(options=options)
        self.__ua = UserAgent(browsers="Chrome", os="Windows", platforms="desktop")
        stealth(
            self.driver,
            user_agent=self.__ua.chrome,
            languages=["ru-RU", "ru"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )

    def __click_feedbacks(self, read_completely: str) -> None:
        clickable_elements = [i for i in self.driver.find_elements(By.CLASS_NAME, read_completely)]
        for element in clickable_elements:
            self.driver.execute_script(
                'arguments[0].scrollIntoView({block: "center", inline: "center"});',
                element,
            )
            element.click()

    def __scrolling(self, read: bool, count: int, feedback: str) -> None:
        last_height = self.driver.execute_script("return document.body.scrollHeight")  # Размер страницы
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            if read:  # Преодалевание footer у ozon
                self.driver.execute_script("window.scrollBy(0, -4000);")
            time.sleep(0.5)

            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

            # для установки кол-ва комментариев
            if count:
                count_scroll_elements = [i for i in self.driver.find_elements(By.CLASS_NAME, feedback)]
                if len(count_scroll_elements) >= count:
                    break

    def __find_rating(self, n: bool, scroll_elements: list, element: int, rating: str) -> int:
        if n:
            return len(
                [
                    i
                    for i in scroll_elements[element]
                    .find_element(By.CLASS_NAME, rating)
                    .find_elements(By.TAG_NAME, "svg")
                    if i.get_attribute("style")[10] == "("
                ],
            )
        return int(scroll_elements[element].find_element(By.CLASS_NAME, rating).get_attribute("class")[-1])

    def __card_info(self, n: bool) -> None:
        if n:
            self.card["title"] = self.driver.find_elements(By.CLASS_NAME, "l4u_27")[-1].text
            self.card["type"] = self.driver.find_elements(By.CLASS_NAME, "sd1_10")[-2].text
            self.card["article"] = self.driver.find_elements(By.CLASS_NAME, "ga121-a2")[3].text[9:]
            WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.TAG_NAME, "video-player")))
            self.card["file"] = self.card["file"] + [
                self.driver.find_elements(By.TAG_NAME, "video-player")[0].get_attribute("src"),
            ]
            self.card["file"] = self.card["file"] + [
                i.find_element(By.TAG_NAME, "img").get_attribute("src")
                for i in self.driver.find_elements(By.CLASS_NAME, "jy0_27")[2:]
            ]
            WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.CLASS_NAME, "yj3_27")))
            shop = self.driver.find_elements(By.CLASS_NAME, "yj3_27")[1]
            self.card["shop"] = [
                shop.get_attribute("href"),
                shop.get_attribute("title"),
            ]
        else:
            self.card["title"] = self.driver.find_element(By.CLASS_NAME, "product-page__title").text
            try:
                self.card["type"] = self.driver.find_elements(By.CLASS_NAME, "breadcrumbs__link")[-2].text
            except Exception:
                self.card["type"] = ""
            self.card["article"] = self.driver.find_element(By.CLASS_NAME, "product-params__copy").text
            for i in self.driver.find_elements(By.CLASS_NAME, "slide__content"):
                try:
                    self.card["file"] = self.card["file"] + [i.find_element(By.TAG_NAME, "video").get_attribute("src")]
                except Exception:
                    self.card["file"] = self.card["file"] + [i.find_element(By.TAG_NAME, "img").get_attribute("src")]
            WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.CLASS_NAME, "seller-info__name")))
            shop = self.driver.find_elements(By.CLASS_NAME, "seller-info__name")[0]
            text = str(shop.get_attribute("innerHTML")).strip()
            self.card["shop"] = [
                "https://www.wildberries.ru" + shop.get_attribute("href"),
                text,
            ]

    def __check_link(self, address: str):
        if address.split("/")[2] == "www.ozon.ru":  # Подготовка для товара на ozon
            feedback = "wp4_30"
            read_completely = "pw_30"
            comment = "w6p_30"
            name = "pt_30"
            read = True
            date = "v7p_30"
            rating = "p8v_30"
            # TODO: звездочки class='a5d24-a a5d24-a0'
            self.driver.get(address)
            # antibot
            c = 0
            try:
                while WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.CLASS_NAME, "rb"))):
                    c += 1
                    element = self.driver.find_element(By.CLASS_NAME, "rb")
                    element.click()
                    if c > 10:
                        break
            except Exception:
                pass
            self.__card_info(read)

        elif address.split("/")[2] == "www.wildberries.ru":  # Подготовка для товара на wb
            date = "feedback__date"
            feedback = "comments__item"
            read = False
            name = "feedback__header"
            comment = "feedback__content"
            read_completely = ""
            rating = "feedback__rating"

            self.driver.get(address)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "canvas")))
            self.__card_info(read)
            self.driver.execute_script("window.scrollBy(0, 1000);")
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "comments__btn-all")))
            self.driver.find_element(By.CLASS_NAME, "comments__btn-all").click()
            self.driver.set_window_size(930, 1080)
            time.sleep(0.02)
        return feedback, read, name, comment, read_completely, date, rating

    def find_feedbacks(self, address: str, count: int = 0) -> dict:
        self.card["link"] = address
        feedback, read, name, comment, read_completely, date, rating = self.__check_link(address)
        # Ожидание прогрузки начала страницы
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "img")))

        # Ожидание прогрузки конца страницы
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "footer")))

        # Scroll
        self.__scrolling(read, count, feedback)

        try:
            if read:  # Кликаем по Читать полностью (есть только у ozon)
                self.__click_feedbacks(read_completely)

            scroll_elements = [i for i in self.driver.find_elements(By.CLASS_NAME, feedback)]
            if count:
                scroll_elements = scroll_elements[:count]
            box = {}
            for element in range(len(scroll_elements)):
                self.driver.execute_script(
                    'arguments[0].scrollIntoView({block: "center", inline: "center"});',
                    scroll_elements[element],
                )
                rats = self.__find_rating(read, scroll_elements, element, rating)
                box[element] = (
                    scroll_elements[element].find_element(By.CLASS_NAME, name).text,
                    scroll_elements[element].find_element(By.CLASS_NAME, comment).text,
                    [i for i in scroll_elements[element].find_elements(By.CLASS_NAME, date)][-1].text,
                    rats,
                )
                # i : (name, feedback)

        except Exception:
            pass

        self.card["feedbacks"] = box
        data = json.dumps(self.card)
        data = json.loads(data)
        return data


if __name__ == "__main__":
    exemplar = Driver()
    link = "https://www.wildberries.ru/catalog/170345712/detail.aspx"
    # print(exemplar.find_feedbacks(link))
