# -*- coding: utf-8 -*-i
from selenium import webdriver
import csv
import time
import sys

def start(website):
    f = [website]
    counter1=0
    driver = webdriver.Firefox()

    for line in f:
        try:
            counter1 = counter1+1
            company=[]
            title=[]
            keyword=[]
            desc=[]

            print ("******************************************************************")
            print "URL Number: ", counter1
            print "Actual URL: ", line
            (line).strip()
            Company_name=line
            Company_name=Company_name.strip()
            company.append(Company_name)
            # To check if http in present company url, if yes then to remove it
            if ('http'in Company_name):
                #print "AKSHAY@#"
                Company_name=str(Company_name)
                Company_name=Company_name.replace('https://','')
                Company_name=Company_name.replace('http://','')
            print Company_name
            #print "Akshay"
            # To open metatags site
            driver.get("http://analyzer.metatags.org/")
            time.sleep(3)
            element1 = driver.find_element_by_xpath('//*[@id="url"]')
            element1.send_keys(Company_name)
            #element1.send_keys('adbidx.com')
            element2 = driver.find_element_by_xpath('//*[@id="target"]/table/tbody/tr[4]/td[2]/input')
            element2.click()
            time.sleep(15)

            #To Fetch Title
            element3=driver.find_elements_by_xpath('//*[@id="show_result"]/table[2]/tbody/tr/td/table/tbody/tr[3]/td[3]')
            try:
                for element in element3:
                        com1=element.text
                        com1=str(com1)
                        print com1
                        if (com1==" " or com1==""):
                            com1="not found"
                        title.append(com1)
            except Exception,e:
                print "E1"
                title.append("not found")
                continue

            # To Fetch Description
            element4=driver.find_elements_by_xpath('//*[@id="show_result"]/table[2]/tbody/tr/td/table/tbody/tr[4]/td[3]')
            #print element4
            try:
                for element in element4:
                        com2=element.text
                        com2=str(com2)
                        print com2
                        if (com2==" " or com2==""):
                            com2="not found"
                        desc.append(com2)
            except Exception,e:
                print "E2"
                desc.append("not found")
                continue
            #To Fetch Keywords
            element5=driver.find_element_by_xpath('//*[@id="show_result"]/table[2]/tbody/tr/td/table/tbody/tr[5]/td[3]')
            try:
                print element5.text
                com2=str(element5.text)
                keyword.append(com2)
                '''for a in element5:
                        com2=element5.text
                        print com2
                        if (com2==" " or com2==""):
                            com2="not found"
                        keyword.append(com2)'''
            except Exception,e:
                print "E3"
                keyword.append("not found")
                continue
        except Exception,e:
            continue

        finally:

            leng=len(company)
            print leng
            i=0



            tuple = list(zip(company,title,desc,keyword))

            print "ZIP TYPE: ", type(tuple), "LEN: ", len(tuple)
            print tuple
            return tuple
            i=i+1
            print data
            print i
            print "DONE"

