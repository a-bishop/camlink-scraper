from selenium import webdriver
from selenium.webdriver.support.ui import Select
import getpass
import sys
from bs4 import BeautifulSoup
import csv
import json
import re

# type in '-v' on command line for verbose flag
if '-v' in sys.argv:
  verbose = True
else:
  verbose = False

user = input("Enter your camlink username: ").upper()
pswd = getpass.getpass("Enter your camlink password: ")
myTerm = input("Enter the school term (ex. 2019W) ").upper()

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
    titles = ['ID', 'Course', 'StartDate', 'EndDate', 'Type', 'Day', 'StartTime', 'EndTime', 'Room']
    writer.writerow(titles)
    courseId = 1
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
        courseInfo.append(courseId)
        courseInfo.append(courseTitle)
        dateInfoSplit = re.split(r"(?<=\d{4})[ ]", course, 1)
        startDateEndDate = re.split(r"(?<=\d{4})-", dateInfoSplit[0], 1)
        startDate = startDateEndDate[0]
        endDate = startDateEndDate[1]
        if verbose:
          print("Start Date: %s" % startDate)
          print("End Date: %s" % endDate)
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
          classTime = re.sub(' - ', ',', classTime)
          classTimeSplit = re.split(',', classTime)
          startTime = classTimeSplit[0]
          endTime = classTimeSplit[1]
          if verbose:
            print("Class Type: %s" % classType)
            print("Class Day: %s" % classDay)
            print("Start Time: %s" % startTime)
            print("End Time: %s" % endTime)
          courseInfo.append(classType)
          courseInfo.append(classDay)
          courseInfo.append(startTime)
          courseInfo.append(endTime)
          roomNum = classRoomTimesSplit[1]
          if verbose:
            print("Room: %s" % roomNum)
          courseInfo.append(roomNum)
        writer.writerow(courseInfo)
        courseId += 1
        

if "-json" in sys.argv:
  totalrows = sum(1 for line in open('camosunCourses' + myTerm + '.csv', 'r'))
  with open('camosunCourses' + myTerm + '.json', 'w') as jsonfile:
    with open('camosunCourses' + myTerm + '.csv', 'r') as csvfile:
      fieldnames = ('ID', 'Course','StartDate','EndDate','Type','Day','StartTime','EndTime','Room')
      dictReader = csv.DictReader(csvfile, fieldnames)
      for row in dictReader:
        if dictReader.line_num == 1:
          jsonfile.write('{ "Courses": [')
          jsonfile.write("\n")
          continue
        else:
          json.dump(row, jsonfile, indent=4, separators=(',', ': '))
        if dictReader.line_num != totalrows:
          jsonfile.write(",\n")
        else:
          jsonfile.write("\n")
      jsonfile.write("]}")







