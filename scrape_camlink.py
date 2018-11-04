from selenium import webdriver
from selenium.webdriver.support.ui import Select
import getpass
from bs4 import BeautifulSoup
import pandas
import os
import re


user = input("Enter your camlink username: ")
pswd = getpass.getpass("Enter your camlink password: ")

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

timetableButton = wd.find_element_by_link_text("Step 3. Build My Timetable")
timetableButton.click()

term = Select(wd.find_element_by_id("VAR1"))
term.select_by_value("2019W")

subject = Select(wd.find_element_by_id("LIST_VAR1_1"))
subject.select_by_value("ICS")

courseLevel = Select(wd.find_element_by_id("LIST_VAR2_1"))
courseLevel.select_by_value("200")

continueButton = wd.find_element_by_name("SUBMIT2")
continueButton.click()

soup = BeautifulSoup(wd.page_source,"html.parser")

for tag in soup.find_all("a", string=re.compile("^ICS")):
  print(tag)






