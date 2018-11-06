from selenium import webdriver
from selenium.webdriver.support.ui import Select
import getpass
import sys
from bs4 import BeautifulSoup
import csv
import re

# type in '-v' on command line for verbose flag
if '-v' in sys.argv:
  verbose = True
else:
  verbose = False

user = input("Enter your camlink username: ")
pswd = getpass.getpass("Enter your camlink password: ")
myTerm = input("Enter the school term (ex. 2019W) ")

wd = webdriver.Chrome()
url = "https://camlink1.camosun.bc.ca"
wd.get(url)

loginButton = wd.find_element_by_id("acctLogin")
loginButton.click()

username = wd.find_element_by_id("USER_NAME") #username form field
password = wd.find_element_by_id("CURR_PWD") #password form field

username.send_keys(user)
password.send_keys(pswd)

submitButton = wd.find_element_by_class_name("shortButton") 
submitButton.click()

studentButton = wd.find_element_by_class_name("WBST_Bars")
studentButton.click()

myScheduleButton = wd.find_element_by_link_text("My class schedule")
myScheduleButton.click()

term = Select(wd.find_element_by_id("VAR4"))
term.select_by_value(myTerm)

submitButton2 = wd.find_element_by_class_name("shortButton")
submitButton2.click()

soup = BeautifulSoup(wd.page_source,"html.parser")

courses = soup.find_all("a", id=re.compile("LIST_VAR6_"))
info = soup.find_all("p", id=re.compile("LIST_VAR12_"))
courseInfo = dict(zip(courses, info))
with open('camosunCourses' + myTerm + '.csv', 'w') as f:
    writer = csv.writer(f)
    titles = ['Course', 'Start Date', 'End Date', 'Type', 'Day', 'Time', 'Room']
    writer.writerow(titles)
    for course, info in courseInfo.items():
      courseTitle = course.text
      if verbose:
        print("----COURSE----")
        print(courseTitle)
      if verbose:
        print("-----INFO-----")
      info = info.text.replace(',', '').split("\n")
      for course in info:
        courseInfo = []
        courseInfo.append(courseTitle)
        dateInfoSplit = re.split(r"(?<=\d{4})[ ]", course, 1)
        startDateEndDate = re.split(r"(?<=\d{4})-", dateInfoSplit[0], 1)
        startDate = startDateEndDate[0]
        endDate = startDateEndDate[1]
        if verbose:
          print(startDate)
          print(endDate)
        courseInfo.append(startDate)
        courseInfo.append(endDate)
        try:
          classRoomTimes = dateInfoSplit[1]
        except:
          classRoomTimes = ''
        if classRoomTimes != '':
          classRoomTimesSplit = re.split(r"(?<=-[ ]\d\d:\d\d\w\w)[ ]", classRoomTimes, 1)
          classTypeDayTime = re.split(r"[ ]", classRoomTimesSplit[0], 2)
          classType = classTypeDayTime[0]
          classDay = classTypeDayTime[1]
          classTime = classTypeDayTime[2]
          if verbose:
            print(classType)
            print(classDay)
            print(classTime)
          courseInfo.append(classType)
          courseInfo.append(classDay)
          courseInfo.append(classTime)
          RoomNum = classRoomTimesSplit[1]
          if verbose:
            print(RoomNum)
          courseInfo.append(RoomNum)
          writer.writerow(courseInfo)







