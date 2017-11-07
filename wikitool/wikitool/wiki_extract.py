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
        counter1 = counter1+1

        print ("******************************************************************")
        print "URL Number: ", counter1
        print "Actual URL: ", line

        (line).strip()
        Company_name=line
        Company_name=Company_name.strip()
        #print "Akshay"
        driver.get("https://www.google.com")
        time.sleep(3)
        element1 = driver.find_element_by_xpath('//*[@id="lst-ib"]')
        #data1=[[Company_name]]
        #Filewriter.writerows(data1)
        element1.send_keys(Company_name+' Wiki')
        #element1.send_keys('115 Solutions P/L')

        element2 = driver.find_element_by_xpath('//*[@id="sblsbb"]/button')
        element2.click()
        counter=0
        time.sleep(10)
        c=[]
        company=""
        wikilinks=""
        wiki_links=""
        content=[]
        list_Company_name=[]
        list_wiki=[]
        list_company_content=[]
        a=1
        try:

                # To Fetch all Weblinks
                element4=driver.find_elements_by_xpath('//*[@class="r"]/a')
                try:
                    for element in element4:
                            com2=element.get_attribute('href')
                            print com2
                            if("wikipedia.org" in com2):
                                if (counter==0):
                                    print "WIKI"
                                    wikilinks=com2
                                    counter=counter+1
                except Exception,e:
                    print "E2"
                    continue
                time.sleep(30)
        except Exception,e:
            print "Pages Exception"

        print "page"
        print wikilinks
        driver.get(wikilinks)
        wiki_links=wikilinks
        print "T"
        cont=""
        try:
            element9=driver.find_element_by_xpath('//*[@id="mw-content-text"]/p[1]')
            print element9.text
            print "HH"

            cont=element9.text
        except Exception,e:
            print "Exception 1"
            pass
        try:
            element10=driver.find_element_by_xpath('//*[@id="mw-content-text"]/p[2]')
            print element10.text
            cont=cont+" " +element10.text
        except Exception,e:
            print "Exception 2"
            content.append(cont)
            pass
        try:
            element11=driver.find_element_by_xpath('//*[@id="mw-content-text"]/p[3]')
            print element11.text
            cont=cont+" " +element10.text
        except Exception,e:
            print "Exception 3"
            content.append(cont)
            pass

        content.append(cont)
        if (cont==""):
            content.append("not found")


        print "DONE"

        data=[[Company_name,wiki_links,content[0].encode('ascii','ignore')]]
        print data
        print "YO"

        list_Company_name.append(Company_name)
        list_wiki.append(wiki_links)
        list_company_content.append(content[0].encode('ascii','ignore'))
        tuple = list(zip(list_Company_name,list_wiki,list_company_content))

        print "ZIP TYPE: ", type(tuple), "LEN: ", len(tuple)
        print tuple
        return tuple



