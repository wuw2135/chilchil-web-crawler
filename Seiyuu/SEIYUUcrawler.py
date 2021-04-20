from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import datetime
import json
import re
import linecache

options = webdriver.ChromeOptions()
options.add_argument('user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"')
driver = webdriver.Chrome(chrome_options=options)


#GET LINKS
def SEIYUUget():
    url = "https://www.chil-chil.net/voiceList/"
    driver.get(url)
    driver.implicitly_wait(2)

    with open("detail_list.txt","w",encoding="utf-8") as file:
        for i in range (200):
            name = driver.find_elements_by_css_selector("#anchor_list > div.c-list_wrap > div > table > tbody > tr:nth-child(n) > th > a")
            title = driver.find_elements_by_css_selector("#anchor_list > div.c-list_wrap > div > table > tbody > tr:nth-child(n) > td:nth-child(2) > a")
            seme = driver.find_elements_by_css_selector("#anchor_list > div.c-list_wrap > div > table > tbody > tr:nth-child(n) > td:nth-child(3) > a")
            uke = driver.find_elements_by_css_selector("#anchor_list > div.c-list_wrap > div > table > tbody > tr:nth-child(n) > td:nth-child(4) > a")
        
            for j in range (len(name)):
                try:
                    HP = driver.find_element_by_css_selector(" tbody > tr:nth-child("+str(int(j+1))+") > td:nth-child(5) > a").get_attribute("href")
                except:
                    HP = "None"
                
                try:
                    Twitter = driver.find_element_by_css_selector(" tbody > tr:nth-child("+str(int(j+1))+") > td:nth-child(6) > a").get_attribute("href")
                except:
                    Twitter = "None"

                detail = {
                    "name" : name[j].text,
                    "name_url" : name[j].get_attribute("href"),
                    "title_count" : title[j].text,
                    "title_url" : title[j].get_attribute("href"),
                    "seme_count" : seme[j].text,
                    "seme_url" : seme[j].get_attribute("href"),
                    "uke_count" : uke[j].text,
                    "uke_url" : uke[j].get_attribute("href"),
                    "HP_link" : HP,
                    "twitter_link" : Twitter,
                }
                
                file.write(str(detail)+"\n")
            try:
                next_page = driver.find_element_by_css_selector("#anchor_list > div.c-list_wrap > nav > ul > li.single > a[aria-label=Next]")
                next_page.click()
                time.sleep(0.5)
                driver.implicitly_wait(2)
            except:
                break


#convertjson
def jsoninput():
    detail_list_list = []
    with open("detail_list.txt","r",encoding="utf-8") as detail_file:
        details = detail_file.readline().rstrip()
        while details:
            detail_list_list.append(eval(details))
            details = detail_file.readline().rstrip()

    with open("SEIYUU_data.json","w",encoding="utf-8") as file:
        file.write(json.dumps(detail_list_list,ensure_ascii=False,indent=1))

def main():
    open("detail_list.txt","a",encoding="utf-8")
    open("SEIYUU_data.json","a",encoding="utf-8")

    SEIYUUget()
    jsoninput()

    driver.close()

if __name__ == "__main__": 
    main()