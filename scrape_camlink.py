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

myScheduleButton = wd.find_element_by_link_text("My class schedule")
myScheduleButton.click()

term = Select(wd.find_element_by_id("VAR4"))
term.select_by_value("2018F")

submitButton2 = wd.find_element_by_class_name("shortButton")
submitButton2.click()

soup = BeautifulSoup(wd.page_source,"html.parser")

# with open("classes.html", "w") as f:
#   f.write(soup)

classes = soup.find_all("a", id=re.compile("LIST_VAR6_"))
for myClass in classes:
  print("class: " + myClass.text)
  info = myClass.parent.parent.next_sibling.next_sibling.contents[1]
  print(info.contents[1].text + "\n")






