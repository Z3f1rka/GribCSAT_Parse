from app.driver.driver import Driver

__driver = None


class DriverInitError(Exception):
    pass


def driver_init() -> None:
    global __driver
    __driver = Driver()


def get_driver() -> Driver:
    if __driver:
        return __driver
    else:
        # print("Init driver first")
        raise DriverInitError


if __name__ == "__main__":
    pass
