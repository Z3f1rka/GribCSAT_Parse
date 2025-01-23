from typing import Annotated

from fastapi import APIRouter
from fastapi import Query

from app.driver.driver_session import get_driver
from app.services import ServiceDriver
from app.validation_models import FBLINPUT
from app.validation_models import FBLOUTPUT

router = APIRouter()


@router.get("/find_by_link/")
def find_info(data: Annotated[FBLINPUT, Query()]) -> FBLOUTPUT:
    driver = get_driver()
    product = ServiceDriver.find_by_link(driver, data.link, data.count)
    return product


if __name__ == "__main__":
    pass
