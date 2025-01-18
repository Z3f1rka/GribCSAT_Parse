from app.driver import driver_init
from app.driver import DriverInitError
from app.driver import get_driver


class TestDriver:
    def test_not_inited(self):
        try:
            get_driver()
        except DriverInitError:
            assert True

    def test_inited(self):
        driver_init()
        get_driver()
        assert True
