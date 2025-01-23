from urllib.parse import unquote_plus

from app.driver.driver import Driver
from app.validation_models import FBLOUTPUT


class ServiceDriver:
    def find_by_link(driver: Driver, address: str, amount_feedbacks: int = 0) -> FBLOUTPUT:
        __return = driver.find_feedbacks(unquote_plus(address), amount_feedbacks)

        return FBLOUTPUT(file=__return["file"],
                         link=__return["link"],
                         title=__return["title"],
                         type=__return["type"],
                         article=__return["article"],
                         shop=__return["shop"],
                         feedbacks=__return["feedbacks"])


if __name__ == "__main__":
    driver = Driver()
    service = ServiceDriver
    ozon_link = ""
    wb_link = ''
    # print(service.find_by_link(driver, ozon_link))
    # print(service.find_by_link(driver, wb_link))
