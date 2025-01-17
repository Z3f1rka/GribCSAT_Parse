from urllib import parse

from app.driver.driver import Driver


class ServiceDriver:
    def find_by_link(driver: Driver, address: str, amount_feedbacks: int = 0) -> dict:
        return driver.find_feedbacks(parse.unquote_plus(address), amount_feedbacks)


if __name__ == "__main__":
    driver = Driver()
    service = ServiceDriver
    ozon_link = ("https://www.ozon.ru/product/pro-series-nabor-dlya-zhenshchin"
                 "-shampun-balzam-dlya-volos-intensivnoe-vosstanovlenie-728885875/")
    wb_link = "https://www.wildberries.ru/catalog/188449648/detail.aspx"
    # print(service.find_by_link(driver, ozon_link))
    # print(service.find_by_link(driver, wb_link))
