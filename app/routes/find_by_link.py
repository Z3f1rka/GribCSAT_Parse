from fastapi import APIRouter

from app.driver.driver_session import get_driver
from app.services import ServiceDriver

router = APIRouter()


@router.get("/find_by_link/")
def find_info(address: str, count: int = 0) -> dict:
    driver = get_driver()
    product = ServiceDriver.find_by_link(driver, address, count)
    return {"product": product}


if __name__ == "__main__":
    pass
