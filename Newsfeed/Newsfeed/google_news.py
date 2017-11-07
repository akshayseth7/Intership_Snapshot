# -*- coding: utf-8 -*-i
from selenium import webdriver
import csv
import time
import sys

def news(inputFile,outputFile):


    counter1=0
    inFile = inputFile
    outFile = outputFile
    pages= input("How many pages you need to extract from Googles:")
    print('Thanks for selecting', pages,"pages")
    #web_pages=pages
    print "Pages"
    #print web_pages
    driver = webdriver.Firefox()
    filehandler = open(outFile, 'w')
    filewriter = csv.writer(filehandler )
    data1=[["Company Name","Page Number","Title","Source","Date","Website","Desc"]]
    filewriter.writerows(data1)
    file = open(inFile, 'r')

    for line in file:
        counter1 = counter1+1
        if(counter1%100==0):
            time.sleep(300)

        print ("******************************************************************")
        print "URL Number: ", counter1
        print "Actual URL: ", line

        (line).strip()
        Company_name=line
        Company_name=Company_name.strip()
        #print "Akshay"
        driver.get("https://www.google.com")
        time.sleep(10)

        company=[]
        title=[]
        website=[]
        source=[]
        date=[]
        comp=[]
        desc=[]

        element1 = driver.find_element_by_xpath('//*[@id="lst-ib"]')
        #data1=[[Company_name]]
        #filewriter.writerows(data1)
        element1.send_keys(Company_name)
        #element1.send_keys('Crayon Data')

        #To Click Search Button
        element2 = driver.find_element_by_xpath('//*[@id="sblsbb"]/button')
        element2.click()
        counter=1
        time.sleep(10)
        #To Search News Entity
        try:
            tag1=driver.find_element_by_xpath('//*[@id="hdtb-msb"]/div[2]/a')
            print tag1.text
            if(tag1.text == "News"):
                tag1.click()
                time.sleep(5)
        except Exception,e:
                    print "News"
                    continue
        try:
            tag2=driver.find_element_by_xpath('//*[@id="hdtb-msb"]/div[3]/a')
            print tag2.text
            if(tag2.text == "News"):
                tag2.click()
                time.sleep(5)
        except Exception,e:
                    print "News"
                    continue
        try:
            tag3=driver.find_element_by_xpath('//*[@id="hdtb-msb"]/div[4]/a')
            print tag3.text
            if(tag3.text == "News"):
                tag3.click()
                time.sleep(5)
        except Exception,e:
                    print "News"
                    continue
        try:
            tag4=driver.find_element_by_xpath('//*[@id="hdtb-msb"]/div[5]/a')
            print tag4.text
            if(tag4.text == "News"):
                tag4.click()
                time.sleep(5)
        except Exception,e:
                    print "News"
                    continue


        #To Fetch Google Pages
        try:
            while(counter < pages+1):
                    print "Pages"
                    print counter
                    #To Fetch Title
                    element3=driver.find_elements_by_xpath('//*[@class="r _U6c"]/a')
                    try:
                        for element in element3:
                                com1=element.text
                                website.append(element.get_attribute('href'))
                                title.append(com1)
                                comp.append(counter)
                    except Exception,e:
                        print "E1"
                        continue

                    #To Fetch Source
                    element4=driver.find_elements_by_xpath('//*[@class="slp"]/span[1]')
                    try:
                        for element in element4:

                                com1=element.text
                                source.append(com1)
                    except Exception,e:
                        print "E2"
                        continue

                    #To Fetch Date
                    element5=driver.find_elements_by_xpath('//*[@class="slp"]/span[3]')
                    try:
                        for element in element5:

                                com1=element.text
                                date.append(com1)
                                company.append(Company_name)
                    except Exception,e:
                        print "E3"
                        continue

                    #To Fetch Meta Data
                    element9=driver.find_elements_by_xpath('//*[@class="st"]')
                    try:
                        for element in element9:
                                com1=element.text
                                desc.append(com1)

                    except Exception,e:
                        print "E8"
                        continue


                    # To Fetch Title
                    element6=driver.find_elements_by_xpath('//*[@class="_hnc card-section"]/a')
                    try:
                        for element in element6:
                                com2=element.get_attribute('href')
                                #print com2
                                website.append(com2)
                                com1=element.text
                                #print com1
                                title.append(com1)
                                comp.append(counter)
                    except Exception,e:
                        print "E4"
                        continue

                    # To Fetch Source
                    element7=driver.find_elements_by_xpath('//*[@class="nsa _tQb f _IId"]')
                    try:
                        for element in element7:
                                com1=element.text
                                #print com1
                                source.append(com1)
                                desc.append("not found")
                    except Exception,e:
                        print "E5"
                        continue

                    # To Fetch Date
                    element8=driver.find_elements_by_xpath('//*[@class="nsa _uQb f"]')
                    try:
                        for element in element8:
                                com1=element.text
                                #print com1
                                date.append(com1)
                                company.append(Company_name)
                    except Exception,e:
                        print "E6"
                        continue

                    counter=counter+1
                    print len(source),len(website),len(date),len(title),len(comp),len(desc)

                #To Search Next Button

                    try:
                        e1=driver.find_element_by_xpath('//*[@id="pnnext"]')
                        e1.click()
                    except Exception,e:
                        e1=driver.find_element_by_xpath('//*[@id="nav"]/tbody/tr/td[12]')
                        e1.click()
                    time.sleep(30)
        except Exception,e:
            continue

        finally:
            leng=len(title)
            print leng
            i=0

            while(i < leng):

                #data=[[company[i].encode('ascii','ignore'),comp[i],title[i].encode('ascii','ignore'),source[i].encode('ascii','ignore'),date[i].encode('ascii','ignore'),website[i].encode('ascii','ignore'),desc[i].encode('ascii','ignore')]]
                if (Company_name.lower()in desc[i].lower()):
                    print "Yes"
                    #print desc[i]
                    data=[[company[i].encode('ascii','ignore'),comp[i],title[i].encode('ascii','ignore'),source[i].encode('ascii','ignore'),date[i].encode('ascii','ignore'),website[i].encode('ascii','ignore'),desc[i].encode('ascii','ignore')]]

                    filewriter .writerows(data)
                i=i+1
                    #print i


            print "DONE"



if __name__ == '__main__':
	news(sys.argv[1],sys.argv[2])