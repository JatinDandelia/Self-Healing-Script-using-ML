from selenium import webdriver
import time  
from selenium.webdriver.common.keys import Keys
from self_healing import invoke_self_healing
from selenium.webdriver.common.by import By

def enter_email():
  try:
    email_id = driver.find_element(By.ID, "ctl00_CPHContainer_txtUserLogin")
  except Exception as e:
    print(e)
    time.sleep(5)
    print('I was in email loop')
    if ('no such element' or 'Unable to locate element') in str(e):
      email_id = invoke_self_healing(e, driver)
  email_id.send_keys('jatin.d@timepass.com')
  time.sleep(5)

def enter_password():
  try:
    password = driver.find_element(By.ID, "ctl00_CPHContainer_txtPassword")
  except Exception as e:
    print(e)
    print('I was in password loop')
    time.sleep(5)
    if ('no such element' or 'Unable to locate element') in str(e):
      password = invoke_self_healing(e, driver)
  password.send_keys('jatin11')
  time.sleep(5)

print("sample test case started")

def press_login():
  print('I was in if login loop')
  try:
    login_button = driver.find_element(By.ID, "ctl00_CPHContainer_btnLoginn")
  except Exception as e:
    print(e)
    if ('no such element' or 'Unable to locate element') in str(e):
      login_button = invoke_self_healing(e, driver)
  login_button.click()

driver = webdriver.Chrome(executable_path='/Users/jatin/Downloads/chromedriver')  
#driver=webdriver.Firefox()  

driver.maximize_window()  
url="https://www.testyou.in/Login.aspx"
driver.get(url) 
enter_email()
enter_password()
press_login()
driver.close()  
print("sample test case successfully completed")  