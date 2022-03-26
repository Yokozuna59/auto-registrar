import requests
import time
import json

dpart = ["AE", "AE", "ARE" , "ARC" , "MBA" , "CHE" , "CHEM" , "CRP" , "CE" , "COE" , "CEM" , "CIE" , "EE" , "ELD" , "ELI" , "ERTH" , "GS" , "SE" , "ICS" , "ISOM" , "IAS" , "LS" , "MGT" , "MSE" , "MATH" , "ME" , "CPG" , "PETE" , "PE" , "PHYS" , "PSE"]

courses = {}
for i in dpart:
    page = requests.get(f"https://registrar.kfupm.edu.sa/api/course-offering?term_code=202130&department_code={i}")
    data = json.loads(page.text)
    datas = data["data"]
    for course in datas:
        courses[course["crn"]] = i
print(courses)

def registrar_requests(crn):
    # Requesting the API
    request = requests.get(f"https://registrar.kfupm.edu.sa/api/course-offering?term_code=202130&department_code={courses[crn]}")

    # Checking if the API is working
    if request.status_code != 200:
        not200()
    elif request.status_code == 200:
        check_for_change(crn, request)
    else:
        down()


def not200():
    print("The API isn't working for the time being, the script will check every 60s.")
    time.sleep(40)
    registrar_requests()
    pass


def down():
    print("The site is down for maintenance for the time being, the code will check every 60s.")
    time.sleep(40)
    registrar_requests()
    pass


def check_for_change(crn, request):
    check_ = json.loads(request.text)
    checks = check_["data"]
    for x in checks:
        if x["crn"] == crn:
            if x['available_seats'] > 0:
                print("\n\n\n\n\n available \n\n\n\n\n")
            else:
                time.sleep(5)
                registrar_requests(crn)


registrar_requests("30494")
