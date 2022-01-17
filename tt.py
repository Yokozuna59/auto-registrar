import requests
import time
import json


#answer = (input("For how long you want to use your the app? e.g. (1s, 1m, 1h)\n")).split()
#
#current_time = time.strftime("%H:%M:%S",(time.localtime()))
#for i in answer:
#     if (i.find("s")):
#          pass
#     elif (i.find("m")):
#          pass
#     elif (i.find("h")):
#          pass

def hi():
     for i in range(10000):
          req = requests.get("https://registrar.kfupm.edu.sa/api/course-offering?term_code=202120&department_code=ICS")
          status = req.status_code

          if (status != 200):
               not200()
          else:
               text = req.text
               if (text.find("The site is down")):
                    down()
                    return

               data = json.loads(req.text)
               if (data["data"] == None):
                    print("The API isn't working for the time being, the code will check for sections every 60s.")
                    time.sleep(40)
                    hi()
                    return
               itis200(data, i)
          print("\n\n")
          time.sleep(20)



def not200():
     print("The API isn't working for the time being, the code will check for sections every 60s.")
     time.sleep(40)
     hi()
     return


def down():
     print("The site is down for maintenance for the time being, the code will check every 60s.")
     time.sleep(40)
     hi()
     return


def itis200(data, index):
     datas = data["data"]
     print(index + 1)

     for i in range(44):
          course = datas[i]
          course_number = course["course_number"]
          section = course["section_number"]

          if (section.find("F") != -1):
               continue

          class_type = course["class_type"]
          crn = course["crn"]
          available_seats = course["available_seats"]
          waiting_list_count = course["waiting_list_count"]

          if ((available_seats != 0) or (waiting_list_count != 0)):
               print(f"{course_number}-{section} , Type: {class_type} , AS: {available_seats} - WL: {waiting_list_count} , {crn}")
               if ((section == "55") or (section == "56") or (section == "73") or (section == "97")):
                    print(f"\n\n\n\n\n {section} \n\n\n\n\n")

hi()

# def tt():
#      driver = webdriver.Chrome()
#      driver.get("https://registrar.kfupm.edu.sa/api/course-offering?term_code=202120&department_code=ICS")

#      for i in range(10000):
#           source = driver.page_source
#           soup = BeautifulSoup(source, "html.parser").text
#           soup_json = json.loads(soup)
#           for j in (12, 20):
#                course = soup_json["data"][j]
#                crn = course["crn"]
#                available_seats = course["available_seats"]
#                waiting_list_count = course["waiting_list_count"]
#                print("crn: " + str(crn), end=", ")
#                print("AS: " + str(available_seats), end=", ")
#                print("WL: " + str(waiting_list_count), end=f"         {i}")
#                if (available_seats != 0 or waiting_list_count != 0):
#                     print("\n\n\n\n\n")
#                else:
#                     print("")
#           time.sleep(10)
#           driver.refresh()