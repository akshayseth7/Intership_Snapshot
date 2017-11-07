# -*- coding: utf-8 -*-i
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import csv
import time
import sys


def start(website):
    f = [website]
    print "Search"

    counter=0

    driver = webdriver.Firefox()

    try:
        for line in f:
            ad_company=[]
            ad_category=[]
            ad_phone=[]
            ad_address=[]
            ad_timings=[]
            ad_website=[]
            ad_dir=[]
            search_comp=[]
            search_web=[]
            company=[]

            counter = counter+1
            if(counter%100==0):
                time.sleep(300)
            print ("******************************************************************")
            print "URL Number: ", counter
            print "Actual URL: ", line

            (line).strip()
            Company_name=line
            Company_name=Company_name.strip()

            driver.get("https://www.google.com")
            element1 = driver.find_element_by_xpath('//*[@id="lst-ib"]')

            company.append(Company_name)
            element1.send_keys(Company_name)
            #element1.send_keys('115 Solutions P/L')
            element2 = driver.find_element_by_xpath('//*[@id="sblsbb"]/button')
            element2.click()
            time.sleep(20)

            # To Fetch ADBox Company Name
            element3=driver.find_elements_by_xpath('//*[@class="kno-ecr-pt kno-fb-ctx _hdf"]')
            if element3==[]:
                com1="Not Found"
            else:
                for element in element3:
                    com1=element.text
                    print com1
                    com1=str(com1)
            ad_company.append(com1)

            # To Fetch ADBox Category
            element4=driver.find_elements_by_xpath('//*[@class="_mr _Wfc vk_gy"]/span[1]')
            if element4==[]:
                com1="Not Found"
            else:
                for element in element4:
                    print "ELE"
                    print element.text
                    com1=element.text
                    com1=str(com1)
            ad_category.append(com1)

            # To Fetch ADBox Address
            element5=driver.find_elements_by_xpath('//*[@class="_Xbe"]')
            if element5==[]:
                com1="Not Found"
            else:
                for element in element5:
                    com1=element.text
                    com1=str(com1)
            ad_address.append(com1)

            # To Fetch ADBox Phone
            element6=driver.find_elements_by_xpath('//*[@id="rhs_block"]/div/div[1]/div/div[1]/ol/div[7]/div/div/span')
            if element6==[]:
                com1="Not Found"
            else:
                for element in element6:
                    com1=element.text
                    com1=str(com1)
            ad_phone.append(com1)

            # To Fetch ADBox Timings
            try:
                element7=driver.find_element_by_xpath('//*[@id="rhs_block"]/div/div[1]/div/div[1]/ol/div[8]/div/div/div/div[1]/span/a/span/span[1]')
                element7.click()
                element8=driver.find_elements_by_xpath('//*[@id="rhs_block"]/div/div[1]/div/div[1]/ol/div[8]/div/div/div/div[2]/table/tbody')
                if element8==[]:
                    com1="Not Found"
                else:
                    for element in element8:
                        com1=element.text
                        com1=str(com1)
                ad_timings.append(element.text)
            except Exception,e:
                print "E1"
                ad_timings.append("not found")

            # To Fetch ADBox WEBSITE
            element8=driver.find_elements_by_xpath('//*[@id="rhs_block"]/div/div[1]/div/div[1]/ol/div[2]/div/div[2]/div[1]/a')
            if element8==[]:
                com1="Not Found"
            else:
                for element in element8:
                    com1=element.get_attribute("href")
                    com1=str(com1)
                    com1=str(com1)
            ad_website.append(com1)

            #To Fetch DIRECTION
            element9=driver.find_elements_by_xpath('//*[@id="rhs_block"]/div/div[1]/div/div[1]/ol/div[2]/div/div[2]/div[2]/a')
            if element9==[]:
                com1="Not Found"
            else:
                for element in element9:
                    com1= element.get_attribute("href")
                    com1=str(com1)
                    com1=str(com1)
            ad_dir.append(com1)

            #To First Result from Google
            element10=driver.find_elements_by_xpath('//*[@id="rso"]/div/div[1]/div/h3/a')
            print element10
            if element10==[]:
                com1="Not Found"
                print "HELLO"
                element10=driver.find_elements_by_xpath('//*[@class="r"]/a')
                print element10
            j=1
            for element in element10:
                if(j==1):
                    com1=element.text
                    j=j+1
                    print counter
                    print element.get_attribute("href")
                    print element.text
                    if ("http" in (element.get_attribute("href"))):
                        search_web.append(element.get_attribute("href"))
                    search_comp.append(element.text)
            time.sleep(15)
            print len(ad_company),len(ad_category),len(ad_phone),len(ad_address),len(ad_timings),len(ad_website),len(ad_dir),len(search_comp),len(search_web)
    except Exception,e:
        pass

    finally:

            leng= len(search_comp)

            print "FINAL"
            print search_comp,search_web
            print leng
            i=0

            data=[[company[i].encode('ascii','ignore'),search_comp[i].encode('ascii','ignore'),search_web[i].encode('ascii','ignore'),ad_company[i].encode('ascii','ignore'),ad_category[i].encode('ascii','ignore'),ad_phone[i].encode('ascii','ignore'),ad_address[i].encode('ascii','ignore'),ad_timings[i].encode('ascii','ignore'),ad_website[i].encode('ascii','ignore'),ad_dir[i].encode('ascii','ignore')]]
            #print data
            tuple = list(zip(company,search_comp,search_web,ad_company,ad_category,ad_phone,ad_address,ad_timings,ad_website,ad_dir))
            print tuple
            return tuple
