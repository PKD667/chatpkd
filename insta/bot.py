

import json
import os,sys
from os import kill  
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import threading
from selenium.webdriver.common.keys import Keys
from time import sleep

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import main

# Initiate the browse
groups = [
   "340282366841710300949128508074012347782",
   "340282366841710300949128414022578350903"
   ]


response_dict = {}
Queue = [[],[]]
text_queue = [[],[]]

dir_path = os.path.dirname(os.path.abspath(__file__))
print(dir_path)

conv = main.Conversation()
conv.load(filename="{}/../insta.json".format(dir_path))
os.remove("log.txt")



        

class WebThread(threading.Thread) :
   text_input = None

   def __init__(self,number,browser,user,password) :
      threading.Thread.__init__(self)
      self.browser = browser
      self.user = user
      self.password = password
      self.number = number

      print(f"Getting group {groups[self.number-1]}")
      browser.get(f'https://www.instagram.com/direct/t/{groups[self.number-1]}')
      sleep(2)
      browser.find_element(by=By.CLASS_NAME, value="_a9--").click()
      print("Accepted cookies")
      sleep(1)
      browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(self.user)
      browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(self.password)
      browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button').click()
      print("Logged in")
      sleep(5)
      browser.find_element(by=By.CLASS_NAME, value="_acan").click()
      print("Cred challenge passed")
      sleep(2)
      try :
         browser.find_element(by=By.CLASS_NAME, value="_a9--").click()
      except Exception :
         pass
      sleep(2)
      self.text_input = browser.find_element(by=By.XPATH,value='/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div/section/div/div/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea')

   def send(self,text):
      print("Sending msg in group {} : {}".format(groups[self.number-1],text))
      self.text_input.send_keys(text + Keys.ENTER)

   def ordering(self,order,response_dict) :
      order = order.lower()
      print(order)
      try :
         if order in response_dict : 
            print('correlation found')  
            self.send(response_dict[order])        
      except Exception :
         pass
      if "comrade" in order or "mon reuf" in order or "camarade" in order or "frere" in order :
         conv.append("user", order)
         response = conv.get_response()
         conv.append(response["role"], response["content"])
         self.send(response["content"])
      else : 
         pass

   def run(self):
    sleep(2)
    prev = ""
    prev_text = ""
    while 1:
        global Queue
        global text_queue
        global image_queue
        sleep(1)
        try:
            active_chat_container = self.browser.find_element(by=By.XPATH, value="/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div/section/div/div/div/div/div[2]")
            messages = active_chat_container.find_elements(by=By.CLASS_NAME, value="x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.xyamay9.x1pi30zi.x1l90r2v.x1swvt13.x1n2onr6.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.xl56j7k")
            msg = messages[-1].text
            if msg != prev and msg != prev_text:
                print("Message received : " + msg)
                self.ordering(msg, response_dict)
            prev = msg
        except Exception as e:
            print("Error : " + str(e))




accounts = [["claude.kirsky","ezf449ezfezfzf"],["groupe_bot","Soniak23"],["groupe_bot02","Soniak23"]]
indices = 0

threads = []

for i in range(1, len(groups) + 1) :
   browser = webdriver.Chrome()        
   threads.append(WebThread(i,browser,accounts[indices][0],accounts[indices][1]))
   threads[i-1].name = "Thread {} : {}".format(i,groups[i-1])
   threads[i-1].start()
   print("Thread {} started".format(threads[i-1].name))
