import json
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium_stealth import stealth
import undetected_chromedriver as uc


class Driver:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.driver = uc.Chrome(options=options)
        stealth(
            self.driver,
            languages=["ru-RU", "ru"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )
        self.driver.maximize_window()

    def click_feedbacks(self, read_completely):
        clickable_elements = [i for i in self.driver.find_elements(By.CLASS_NAME, read_completely)]
        for element in clickable_elements:
            self.driver.execute_script(
                'arguments[0].scrollIntoView({block: "center", inline: "center"});',
                element,
            )
            element.click()

    def scrolling(self, read, count, feedback):
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

    def check_link(self, address):
        if address.split("/")[2] == "www.ozon.ru":  # Подготовка для товара на ozon
            feedback = "wp4_30"
            read_completely = "pw_30"
            comment = "w6p_30"
            name = "pt_30"
            read = True
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

        elif address.split("/")[2] == "www.wildberries.ru":  # Подготовка для товара на wb
            feedback = "comments__item"
            read = False
            name = "feedback__header"
            comment = "feedback__content"
            read_completely = ""

            self.driver.get(address)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "canvas")))
            self.driver.execute_script("window.scrollBy(0, 1000);")
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "comments__btn-all")))
            self.driver.find_element(By.CLASS_NAME, "comments__btn-all").click()
        return feedback, read, name, comment, read_completely

    def find_feedbacks(self, address: str, count: int = 0):
        feedback, read, name, comment, read_completely = self.check_link(address)
        # Ожидание прогрузки начала страницы
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "img")))

        # Ожидание прогрузки конца страницы
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "footer")))

        # Scroll
        self.scrolling(read, count, feedback)

        try:
            if read:  # Кликаем по Читать полностью (есть только у ozon)
                self.click_feedbacks(read_completely)

            scroll_elements = [i for i in self.driver.find_elements(By.CLASS_NAME, feedback)]
            if count:
                scroll_elements = scroll_elements[:count]
            box = {}
            for element in range(len(scroll_elements)):
                self.driver.execute_script(
                    'arguments[0].scrollIntoView({block: "center", inline: "center"});',
                    scroll_elements[element],
                )
                box[element] = (
                    scroll_elements[element].find_element(By.CLASS_NAME, name).text,
                    scroll_elements[element].find_element(By.CLASS_NAME, comment).text,
                )
                # i : (name, feedback)

        except Exception:
            pass

        data = json.dumps(box)
        data = json.loads(data)
        return data
