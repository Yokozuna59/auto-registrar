import requests
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

_exhausted = object()


def registrar_requests(crn, username, password, term, department):
    # Requesting the API
    request = requests.get(f"https://registrar.kfupm.edu.sa/api/course-offering?term_code={term}&department_code={department}")
    # Checking if the API is working
    if request.status_code != 200:
        repeat = not200()
    elif request.status_code == 200:
        repeat = check_for_change(crn, request, username, password)
    else:
        repeat = down()
    return repeat


def not200():
    print("The API isn't working for the time being, the script will check every 60s.")
    time.sleep(40)
    return True


def down():
    print("The site is down for maintenance for the time being, the code will check every 60s.")
    time.sleep(40)
    return True


def check_for_change(crn, request, username, password):
    check_ = json.loads(request.content)
    checks = check_["data"]
    z = filter(lambda j: j["crn"] in crn, checks)
    for x in z:
        if x['available_seats'] and x['waiting_list_count']:
            register(crn, username, password)
            return False
    return True


def register(crn, username, password):
    driver = webdriver.Chrome(PATH)
    driver.get("https://banner9-registration.kfupm.edu.sa/StudentRegistrationSsb/ssb/term/termSelection?mode=registration")
    try:
        term = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "register-desc"))
        )
        term.click()
        try:
            user = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            user.send_keys(username)

            password_input = driver.find_element(By.ID, "password")
            password_input.send_keys(password)
            password_input.send_keys(Keys.RETURN)
            try:
                term = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "select2-chosen-1")))
                term.click()

                term_select = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.ID, terms[crn])))
                term_select.click()
                time.sleep(1)
                term_go = driver.find_element(By.ID, "term-go")
                term_go.click()
            finally:
                time.sleep(1)

            try:
                enterCRNs_tab = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "enterCRNs-tab")))

                enterCRNs_tab.click()

            finally:
                time.sleep(1)
                enterCRN = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "txt_crn1")))
                enterCRN.send_keys(crn)
                addCRNbutton = driver.find_element(By.ID, "addCRNbutton")
                addCRNbutton.click()
                saveButton = driver.find_element(By.ID, "saveButton")
                saveButton.click()
        finally:
            time.sleep(1)
    except:
        driver.quit()
        register(crn, username, password)


repeat = True

while repeat:
    repeat = registrar_requests(crn="", username="", password="", term="", department="")
