import csv
import sqlite3
import MLmodel
from selenium.webdriver.common.by import By

def invoke_self_healing(e, driver):
  locator, locator_element = parse_error(e)
  make_trainer_file(driver)
  make_test_file(locator, locator_element)
  print ('* * * Triggering ML Model * * *')
  locator_element = MLmodel.call_ML_model()
  locator_element_attributes = get_new_locator(locator_element)
  new_locator_is = continue_selenium_script(driver, locator_element_attributes)
  return new_locator_is

def parse_error(e):
  e = str(e)
  if 'xpath' in (e):
    words = e.split('}')[0]
    words = words.split('@')
    locator = words[-1].split('=')[0]
    locator_element = words[-1].split('=')[1]
    locator_element = locator_element.split(']')[0]
    locator_element = locator_element[1:-1]
  elif ('id' or 'class' or 'name') in (e):
    #print('I was in id')
    words = e.split('}')[0]
    words  = e.split('=')
    #print(words, len(words))
    locator = words[0].split('[')
    locator = locator[-1]
    #print(locator[-1])
    locator_element = words[1].split(']')
    locator_element = str(locator_element[0])
    #print(str(locator_element[0]))
  else:
    words = e.split(',')
    locator = words[0].split(':')[-1]
    #print(locator)
    locator_element = words[1].split(':'[0])[-1].split('}')[0]
    #print(locator_element)
  return locator, locator_element

def make_trainer_file(driver):
  all_ids = driver.find_elements('xpath','//*[@id]')
  fields = ['tag', 'id', 'class', 'type', 'name', 'value', 'href']
  with open('self-healing script/train.csv', 'w+') as csvfile:
    csvwriter = csv.writer(csvfile)    
    # writing the fields 
    csvwriter.writerow(fields) 

    for ii in all_ids:
      tag = ii.tag_name
      id = ii.get_attribute('id')
      classe = ii.get_attribute('class')  # id name as string
      type = ii.get_attribute('type')
      name = ii.get_attribute('name')
      value = ii.get_attribute('value')
      href = ii.get_attribute('href')
      csvwriter.writerow([tag,id,classe,type,name,value,href])

def make_test_file(locator, locator_element):
  connection = sqlite3.connect('page.db')
  cursor = connection.cursor()
  if 'link text' in locator:
    locator = 'href'
  elif 'tag name' in locator:
    locator = 'tag'
  # WHERE CLAUSE TO RETRIEVE DATA
  #print(locator, locator_element)
  query = "SELECT * FROM PAGE WHERE {} = {}".format(locator, locator_element)
  #print(query)
  cursor.execute(query)
  data = cursor.fetchall()
  #print(data, 'data')
  connection.commit()
  connection.close()
  fields = ['tag', 'id', 'class', 'type', 'name', 'value', 'href']
  with open('self-healing script/test.csv', 'w+') as csvfile:
    csvwriter = csv.writer(csvfile)    
    # writing the fields 
    csvwriter.writerow(fields)
    for each_data in data:
      each_data = list(each_data)
      #print(each_data)
      csvwriter.writerow(each_data)

def get_new_locator(locator_element):
  locator_element_attributes = None
  with open('self-healing script/train.csv') as file_obj:
    csvr = csv.reader(file_obj)
    csvr = list(csvr)
    #print(csvr)
    #print('Printing csv')
    #print (locator_element)
    for row in csvr:
      if locator_element in row:
        locator_element_attributes = row
        #print(locator_element_attributes)
        break
    return locator_element_attributes

def continue_selenium_script(driver, locator_element_attributes):
  if locator_element_attributes[1] is not (None or ''):
    new_locator_is = driver.find_element(By.ID, str(locator_element_attributes[1]))
  return new_locator_is
