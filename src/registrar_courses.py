from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

from selenium import webdriver
from cli import progress_bar, print_colorful_text, AnsiEscapeCodes


class WebDriver:
    def __init__(self, driver_path, username, passcode, term) -> None:
        self.driver_path = driver_path
        self.username = username
        self.passcode = passcode
        self.term = term

    def setup_browser(self) -> None:
        try:
            self.driver = webdriver.Chrome()
        except WebDriverException:
            try:
                self.driver = webdriver.Chrome(executable_path=self.driver_path)
            except WebDriverException as error_message:
                if "executable needs to be in PATH" in error_message.msg:
                    print("You don't have chromedriver in the directory!")
                elif (
                    "This version of ChromeDriver only supports Chrome version"
                    in error_message.msg
                ):
                    print(
                        "You have installed an older version of chrome! update your chrome driver"
                    )
                exit()
        finally:
            self.driver.maximize_window()

    def open_banner9(self):
        driver = self.driver
        finished = False
        while not finished:
            try:
                driver.get(
                    url="https://banner9-registration.kfupm.edu.sa/StudentRegistrationSsb/ssb/registration/registerPostSignIn?mode=preReg"
                )
                WebDriver.wait_request_to_finish(self=self)
                finished = True
            except WebDriverException as error_message:
                if "net::ERR_INTERNET_DISCONNECTED" in error_message.msg:
                    print_colorful_text(
                        text_string="! Sorry, you currently don't have internet connection! the script will recheck in 10 seconds.",
                        text_color=AnsiEscapeCodes.RED,
                    )
                progress_bar(10)

    def login(self):
        driver = self.driver
        finished = False
        while not finished:
            if "Sign in to your account" in driver.page_source:
                driver.find_element(by=By.ID, value="usernameUserInput").send_keys(
                    self.username
                )
                driver.find_element(by=By.ID, value="password").send_keys(self.passcode)
                driver.find_element(
                    by=By.CLASS_NAME, value="eds-button--primary"
                ).click()

                WebDriver.wait_request_to_finish(self)
            elif "https://login.kfupm.edu.sa/" in driver.current_url:
                html_source = driver.page_source
                if (
                    "Login failed! Please recheck the username and password and try again."
                    in html_source
                ):
                    print(
                        "your passcode is wrong please rewrtite your passcode by your self and change the passcode in .config.json file"
                    )
                    WebDriver.wait_request_to_happen(self)
                    WebDriver.login(self)
                elif "Authentication Error!" in html_source:
                    WebDriver.open_banner9(self)
                    WebDriver.login(self)
            else:
                finished = True

    def wait_request_to_finish(self):
        jquery_state = False
        while not jquery_state:
            jquery_state = self.driver.execute_script("return jQuery.active == 0")

    def wait_request_to_happen(self):
        jquery_state = False
        while not jquery_state:
            jquery_state = self.driver.execute_script("return jQuery.active == 1")

    def quit_webdriver(self):
        self.driver.quit()


driver = WebDriver(
    driver_path="/home/potato/work/programming/auto-registrar/auto-registrar/drivers/chromedriver",
    username="s202163910",
    passcode="KF#1RaYs#1PM",
    term="202210",
)
driver.setup_browser()
driver.open_banner9()
driver.login()
driver.quit_webdriver()
print


# TIMEOUT = 10


# def try_finding(element_id):
#     try:
#         WebDriverWait(driver=driver, timeout=TIMEOUT).until(method=EC.presence_of_element_located(locator=(By.ID, element_id)))
#         return True
#     except TimeoutException:
#         print("Timed out waiting for page to load")
#         return False

# def submit_term():
#     result = try_finding("s2id_txt_term")
#     if (result == False):
#         print("time error")
#     select_box = driver.find_element(by=By.ID, value="s2id_txt_term")
#     select_box.click()
#     wait_request_to_finish()

#     result = try_finding("s2id_autogen1_search")
#     if (result == False):
#         print("time error")
#     text_box = driver.find_element(by=By.ID, value="s2id_autogen1_search")
#     text_box.send_keys(TERM)
#     wait_request_to_finish()

#     result = try_finding(TERM)
#     if (result == False):
#         print("time error no such element")
#     term = driver.find_element(by=By.ID, value=TERM)
#     term.click()
#     wait_request_to_finish()

#     submit_button = driver.find_element(by=By.ID, value="term-go")
#     submit_button.click()
#     wait_request_to_finish()

# def check_error():
#     soup = BeautifulSoup(driver.page_source, "html.parser")
#     errors = soup.find_all("li", class_="notification-item notification-center-message-with-prompts notification-center-message-error")

#     if (not bool(len(errors))):
#         return

#     for i in errors:
#         text_error = soup.find("a", class_="notification-flyout-item notification-message").text
#         if ("Time tickets prevent registration" in errors):
#             pass
#         elif ("Must select a term" in errors):
#             pass
#         elif ("Another sign-on is reviewing your registration records at this time. Please try again later." in errors):
#             pass

# "https://banner9-registration.kfupm.edu.sa/StudentRegistrationSsb/ssb/classRegistration/classRegistration"
# "https://banner9-registration.kfupm.edu.sa/StudentRegistrationSsb/ssb/term/termSelection?mode=registration"


# def main():
#     submit_term()
#     check_error()
#     while True: sleep(1)
# # main()


# from time import sleep
# from bs4 import BeautifulSoup
# from cli import print_colorful_text, AnsiEscapeCodes, progress_bar

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException, WebDriverException


# CHECK_STATUS_URL = "https://banner9-registration.kfupm.edu.sa/StudentRegistrationSsb/ssb/term/termSelection?mode=preReg"
# ADD_AND_DROP_URL = "https://banner9-registration.kfupm.edu.sa/StudentRegistrationSsb/ssb/term/termSelection?mode=registration"

# def start_browser(browser, driver_path, username, passcode, term):
#     if (browser == "chrome"):
#         try:
#             driver = webdriver.Chrome(executable_path=driver_path)
#         except WebDriverException as error_message:
#             if ("executable needs to be in PATH" in error_message.msg):
#                 print_colorful_text(text_string="! Sorry, you dont have chromedriver in the directory", color=AnsiEscapeCodes.RED)
#             elif ("This version of ChromeDriver only supports Chrome version" in error_message.msg):
#                 print_colorful_text(text_string="! Sorry, you have installed wrong chromedriver version! please install another one", color=AnsiEscapeCodes.RED)
#             exit()
#     elif (browser == "firefox"):
#         try:
#             driver = webdriver.Firefox(executable_path=driver_path)
#         except WebDriverException as error_message:
#             if ("executable needs to be in PATH" in error_message.msg):
#                 print_colorful_text(text_string="! Sorry, you dont have geckodriver in the directory", color=AnsiEscapeCodes.RED)
#             elif ("This version of FirefoxDriver only supports Firefox version" in error_message.msg):
#                 print_colorful_text(text_string="! Sorry, you have installed wrong geckodriver version! please install another one", color=AnsiEscapeCodes.RED)
#             exit()
#     driver.maximize_window()

#     open_banner(driver, username, passcode, term)
