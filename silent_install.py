from selenium import webdriver
from pyvirtualdisplay.display import Display
import time
import pyautogui
from selenium.webdriver.common.by import By
#from Common_Methods.GenericMethods import *
import os 
import json
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement




def generate_install_json(url):
        setting_file = open('/usr/lib/firefox/distribution/policies.json','w')
        text = {
                "policies":{
                        "Extensions":{
    	                        "Install":[url]
                        }
                }
        }
        json.dump(text, setting_file, indent=2, sort_keys=True, ensure_ascii=False)
        setting_file.close()
        
def generate_uninstall_json(url):
        setting_file = open('/usr/lib/firefox/distribution/policies.json','w')
        text = {
                "policies":{
                        "Extensions":{
    	                        "Uninstall":[url]
                        }
                }
        }
        json.dump(text, setting_file, indent=2, sort_keys=True, ensure_ascii=False)
        setting_file.close()

if __name__ == '__main__':
        source_path = './URL/other_url.txt'
        dst_path = './FIN/other_url.txt'
        url_to_honeysite = 'file:///home/parallels/Downloads/pythonProject/honey/views/index.html'
        stdout = open(dst_path,'a')
        url_list = open(source_path)

        readlines = url_list.readlines()
        count = 0
        for line in readlines:
                print(line)
                count+=1
                generate_install_json(line)
                display =Display(visible=0, size=(1920, 1080))
                driver = webdriver.Firefox()
                time.sleep(6)
                windowstabs=driver.window_handles
                driver.switch_to.window(windowstabs[0])
                driver.get(url_to_honeysite); 
                time.sleep(10)
                
                try:
                    msg = driver.find_element(By.ID, "msg_signatures").text
                    http = driver.find_element(By.ID, "http_signatures").text
                    tabs_errupt = len(driver.window_handles)-1
                    context = {
                    "index" : count,
                    "name" : line.split("/")[-1].strip(),
                    "fingerprints":{
                        "MSG": msg,
                        "http": http
                    },
                    "tabs" : tabs_errupt
        	    }
        	    
                    stdout.write(json.dumps(context))
                    stdout.write('\n')
                except:
                    continue
                driver.quit()
                generate_uninstall_json(line)
                driver = webdriver.Firefox()
                time.sleep(1)
                driver.quit()
