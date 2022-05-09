# import get_cpu_info to get cpu name
from cpuinfo import get_cpu_info

# import system to get the system name
from platform import system

# import maxsize to get the number of bits in cpu
from sys import maxsize


def check_platform(browser:str) -> str:
    """
    This function gets the system and the driver's path.\n
    return path as `str` type.
    """

    get_system = system()
    driver_ = "chromedriver" if browser == "chrome" else "geckodriver"

    if (get_system == "Linux"):
        driver_path = f"drivers/{browser}/linux/{driver_}"
    elif (get_system == "Darwin"):
        cpu = get_cpu_info()["brand_raw"]
        if ("Intel" in cpu):
            driver_path = f"drivers/{browser}/macOS/intel/{driver_}"
        else:
            driver_path = f"drivers/{browser}/macOS/m1/{driver_}"
    elif (get_system == "Windows"):
        if (maxsize > 2**32):
            driver_path = f"drivers/{browser}/windows/win32/{driver_}.exe"
        else:
            driver_path = f"drivers/{browser}/windows/win64/{driver_}.exe"

    return driver_path