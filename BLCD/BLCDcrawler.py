from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import datetime
import json
import re
import linecache

options = webdriver.ChromeOptions()
options.add_argument('user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"')
driver = webdriver.Chrome(chrome_options=options)

#ACCOUNT SETTING
def login():
    url = "https://www.chil-chil.net/login/"
    driver.get(url)
    driver.implicitly_wait(2)

    with open("accountset.json","r",encoding="utf-8") as jfile:
        jdata = json.load(jfile)

        email = driver.find_element_by_css_selector("#exampleInputEmail1")
        email.send_keys(jdata["email"])
        time.sleep(0.5)

        passward = driver.find_element_by_css_selector("#exampleInputPassword1")
        passward.send_keys(jdata["password"])
        time.sleep(0.5)

        login_botton = driver.find_element_by_css_selector("#form1 > div:nth-child(3) > button")
        login_botton.click()
        time.sleep(5)

#GET LINKS
def BLCDtitlelinksget():
    url = "https://www.chil-chil.net/goodsList/category_id[]/10/type/9/"
    driver.get(url)
    driver.implicitly_wait(2)

    with open("url_list.txt","a",encoding="utf-8") as url_file:
        for i in range (200):
            title_urls = driver.find_elements_by_css_selector("div:nth-child(n) > div.col-xs-9.c-list_box > h2 > a:nth-child(1)")
            for title_url in title_urls:
                title_url = title_url.get_attribute("href")
                url_file.write(title_url+"\n")
            try:
                next_page = driver.find_element_by_css_selector("div.row.c-block.c-list_block.cleafix > div.col-md-8 > div.c-tab_wrap > div > nav:nth-child(1) > ul > li.single > a[aria-label=Next]")
                next_page.click()
                time.sleep(0.5)
                driver.implicitly_wait(2)
            except:
                break



#GET DETAIL
def datamerge(datafilename):
    with open("url_list.txt","r",encoding="utf-8") as url_file:
        title_url = url_file.readline().rstrip()
        with open(datafilename,"a",encoding="utf-8") as detail_file:
            while title_url:
                driver.get(title_url)
                driver.implicitly_wait(2)
                time.sleep(0.5)

                try:
                    botton = driver.find_element_by_css_selector("#bt_yes")
                    botton.click()
                except:
                    pass

                play_count = 0
                setting_count = 0
                other_count = 0
                play = ""
                setting = ""
                semeXuke = ""
                other = ""

                title = driver.find_element_by_css_selector("div.clearfix > div.c-detail_title > h1").text

                try:
                    jpg_url = driver.find_element_by_css_selector("div:nth-child(4) > div.col-sm-4 > div > div > img").get_attribute("src")
                except:
                    jpg_url = "無"

                try:
                    date_text = driver.find_element_by_css_selector("dd > time").text
                except:
                    date_text = "無"

                try:
                    date = driver.find_element_by_css_selector("dd > time").get_attribute("datetime")
                except:
                    date = "無"

                try:
                    description = driver.find_element_by_css_selector("div > blockquarto").text
                except:
                    description = "無"

                try:
                    seme_list = driver.find_elements_by_css_selector("div.c-story_seme > p > span.chara")
                    uke_list = driver.find_elements_by_css_selector("div.c-story_uke > p > span.chara")
                    for i in range (len(seme_list)):
                        if i+1 == len(seme_list):
                            semeXuke = semeXuke + seme_list[i].text + " X " + uke_list[i].text
                        else:
                            semeXuke = semeXuke + seme_list[i].text + " X " + uke_list[i].text + " / "
                except:
                    semeXuke = "無"

                try:
                    other_list = driver.find_elements_by_css_selector("dl.c-story_other > dd")
                    for others in other_list:
                        other_count = other_count + 1
                        if other_count == len(other_list):
                            other = other + others.text
                        else:
                            other = other + others.text + "／ "
                except:
                    other = "無"

                try:
                    ero = driver.find_element_by_css_selector("div.c-story_tag > dl:nth-child(1) > dd").text.replace('\n', '').replace('\r', '').replace('\t', '')
                except:
                    ero = "無"


                play_list = driver.find_elements_by_css_selector("#anchor_story > div.c-story_tag > dl:nth-child(2) > dd > a:nth-child(n)")
                for plays in play_list:
                    play_count = play_count + 1
                    if play_count == len(play_list):
                        play = play + plays.text
                    else:
                        play = play + plays.text + " / "

                setting_list = driver.find_elements_by_css_selector("#anchor_story > div.c-story_tag > dl:nth-child(3) > dd > a:nth-child(n)")
                for settings in setting_list:
                    setting_count = setting_count + 1
                    if setting_count == len(setting_list):
                        setting = setting + settings.text
                    else:
                            setting = setting + settings.text + " / "  

                detail = {
                    "title" : title,
                    "title_url" : title_url,
                    "jpg_url" : jpg_url,
                    "date_text" : date_text,
                    "date" : date,
                    "description" : description,
                    "seme X uke" : semeXuke,
                    "other" : other,
                    "ero" : ero,
                    "plays" : play,
                    "settings" : setting
                }
                
                detail_file.write(str(detail)+"\n")
                    
                time.sleep(2)
                title_url = url_file.readline().rstrip()

#usedurldelete
def usedurldelete():
    url_dict = eval(linecache.getline("detail_list.txt",datacountdetect()))
    url = url_dict["title_url"]

    with open("url_list.txt") as cover_file:
        for i, line in enumerate(cover_file):
            if url in line:
                line_count = i+1
                with open("url_list.txt","r",encoding="utf-8") as file:
                    readlines = file.readlines()
                with open("url_list.txt","w",encoding="utf-8") as file:
                    file.write("".join(readlines[line_count:]))
    


#update
def update():
    url = "https://www.chil-chil.net/goodsList/category_id[]/10/type/9/"
    driver.get(url)
    driver.implicitly_wait(2)

    url_list = []
    with open("url_list.txt","r+",encoding="utf-8") as url_file:
        title_urls = driver.find_elements_by_css_selector("div:nth-child(n) > div.col-xs-9.c-list_box > h2 > a:nth-child(1)")
        for title_url in title_urls:
            title_url = title_url.get_attribute("href")
            url_list.append(title_url)
            url_file.write(title_url+"\n")
    
    datamerge("updatedetail_list.txt")

    with open("BLCD_data.json","r",encoding="utf-8") as f:
        data = json.load(f)

            
    for i in range (len(url_list)):
        for j in range (len(data)):
            if url_list[i] in str(data[j]):
                data.pop(j)
                break
            
    with open("updatedetail_list.txt","r+",encoding="utf-8") as file:
        readline = file.readline().rstrip()
        while readline:
            data.append(eval(readline))
            readline = file.readline().rstrip()
        file.truncate()

    with open("BLCD_data.json","w",encoding="utf-8") as file:
        file.truncate()
        file.write(json.dumps(data,ensure_ascii=False,indent=1))
    
    with open("url_list.txt","w",encoding="utf-8") as file:
        file.truncate()
    

#urlcountdetect
def urlcountdetect():
    return len(open("url_list.txt","r",encoding="utf-8").readlines())

#datacountdetect
def datacountdetect():
    return len(open("detail_list.txt","r",encoding="utf-8").readlines())


#convertjson
def jsoninput():
    detail_list_list = []
    with open("detail_list.txt","r",encoding="utf-8") as detail_file:
        details = detail_file.readline().rstrip()
        while details:
            detail_list_list.append(eval(details))
            details = detail_file.readline().rstrip()

    with open("BLCD_data.json","w",encoding="utf-8") as file:
        file.write(json.dumps(detail_list_list,ensure_ascii=False,indent=1))
    
    with open("url_list.txt","w",encoding="utf-8") as file:
        file.truncate()

def semeukemark():
    with open("BLCD_data.json","r",encoding="utf-8") as file:
        content = json.load(file)

    changed = []
    with open("BLCD_data.json","w",encoding="utf-8") as file:
        for j in range (len(content)):
            string3 = ""
            string1 = content[j]["seme X uke"]
            string2 = re.split(' → | X | / ',string1)
            for i in range(len(string2)):
                if i == 0 or i == 2 or i ==  4 or i ==  6 or i ==  8 or i ==  10 or i ==  12 or i ==  14 or i ==  16 or i ==  18 or i ==  20 or i ==  22 or i ==  24 or i ==  26:
                    string2[i] = string2[i] + " → "
                if i == 1 or i ==  5 or i ==  9 or i ==  13 or i ==  17 or i ==  21 or i ==  25:
                    string2[i] = "*" + string2[i] + " X "
                if i == 3 or i ==  7 or i ==  11 or i ==  15 or i ==  19 or i ==  23 or i ==  27:
                    string2[i] = string2[i] + "*" + " / "
                
                string3 = string3 + string2[i]
            
            content[j]["seme X uke"] = string3.removesuffix(' / ')
            changed.append(content[j])
        file.write(json.dumps(changed,ensure_ascii=False,indent=1))

def main():
    login()
    open("url_list.txt","a",encoding="utf-8")
    open("detail_list.txt","a",encoding="utf-8")
    open("updatedetail_list.txt","a",encoding="utf-8")

    if len(open("BLCD_data.json","r",encoding="utf-8").readlines()) > 0:
        update()
        semeukemark()
    else:    
        if urlcountdetect() == 0 and datacountdetect() == 0:
            BLCDtitlelinksget()
            datamerge("detail_list.txt")
            jsoninput()
            semeukemark()
        else:
            if datacountdetect() == 0:
                datamerge("detail_list.txt")
                jsoninput()
                semeukemark()
            else:
                usedurldelete()
                datamerge("detail_list.txt")
                jsoninput()
                semeukemark()
    

    driver.close()

if __name__ == "__main__": 
    main()
