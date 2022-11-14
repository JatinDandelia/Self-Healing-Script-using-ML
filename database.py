# importing the libraries
from bs4 import BeautifulSoup
import requests
import sqlite3
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time

url="https://www.testyou.in/Login.aspx"
#url = "https://www.testyou.in/SignUp.aspx"

# start web browser
options = Options()
  
# this parameter tells Chrome that
# it should be run without UI (Headless)
options.headless = True
driver=webdriver.Firefox(options=options)
driver.get(url)

all_ids = driver.find_elements('xpath','//*[@id]')

connection_obj = sqlite3.connect('page.db')
 
# cursor object
cursor_obj = connection_obj.cursor()
 
# Drop the GEEK table if already exists.
cursor_obj.execute("DROP TABLE IF EXISTS PAGE")
 
# Creating table
table = """ CREATE TABLE PAGE (
            tag VARCHAR(255),
            id VARCHAR(255),
            class VARCHAR(255),
            type VARCHAR(255),
            name VARCHAR(255),
            href VARCHAR(255),
            value VARCHAR(255)
        ); """
 
cursor_obj.execute(table)

for ii in all_ids:
     tag = ii.tag_name
     id = ii.get_attribute('id')
     classe = ii.get_attribute('class')  # id name as string
     type = ii.get_attribute('type')
     name = ii.get_attribute('name')
     value = ii.get_attribute('value')
     href = ii.get_attribute('href')
     cursor_obj.execute("insert into PAGE (tag, id, class, type, name, value, href) values (?, ?, ?, ?, ?, ?, ?)",
            (tag, id, classe, type, name, value, href))

print("Table is Ready")

# # Printing the required data
# data=cursor_obj.execute('''SELECT * FROM PAGE''')
# for row in data:
#     print(row)

connection_obj.commit() 
# Close the connection
connection_obj.close()