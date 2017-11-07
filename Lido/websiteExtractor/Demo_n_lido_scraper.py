# -*- coding: utf-8 -*-

import requests
import textwrap
import csv
from bs4 import BeautifulSoup
import nltk
import urllib2
import logging
from tld import get_tld
import Demo_socialmedia as sm
#import Demo_n_aboutus as au
import Demo_aboutus as au
import Demo_contactus as ctus

#def main():
def start(website):
    f = [website]
    logging.basicConfig(level=logging.DEBUG, filename='contact.log')
    list_abt=[]
    list_Company_url=[]
    list_ct_us_text=[]
    list_company_fb=[]
    list_company_yt=[]
    list_company_lin=[]
    list_company_tw=[]
    list_company_pi=[]
    list_google_pl=[]
    list_company_tel=[]
    list_company_email=[]
    list_company_in=[]
    list_company_fax=[]
    list_company_add=[]
    list_company_fl=[]
    counter=0
    for line in f:
            counter = counter+1
            print ("------------------------------------------------------------------------------------------------------------")
            print "URL Number: ", counter
            print "Actual URL: ", line
            try:
                (line).strip()
                Company_url=line
                Company_url=Company_url.strip()

                try:
                    opener = urllib2.build_opener()
                    opener.addheaders = [('User-agent', 'Mozilla/7.0')]
                    #print "sdgsgkjnssf"
                except Exception,e:
                    #print e
                    logging.error("Error in Browser Agent :: %s" % e)


                ## To check for URL error and website status:
                try:
                    urllib2.urlopen(Company_url)
                    #print "YES"
                except urllib2.HTTPError, e:
                    logging.info(" --HTTP_ERROR-- ")
                    logging.error("Error in HTTPError :: %s" % e)

                    #print "HTTP ERROR"
                    error=e.code
                    (error)=str(error)
                    #print error
                    data = [[Company_url,"Not Active: "+error]]
                    #a.writerows(data)
                    continue

                except urllib2.URLError, e:
                    logging.info(" --URL_ERROR-- ")
                    logging.error("Error in URLError :: %s" % e)

                    #print "URL ERROR: "
                    error=e.args
                    (error)=str(error)
                    #print error
                    data = [[Company_url,"Not Active: "+error]]
                    #a.writerows(data)
                    continue

                # Implement Timeout
                response = opener.open(Company_url, timeout=100)
                page = response.read()
                soup = BeautifulSoup(page,'lxml')
                # for script in soup(["javascript"]):
                #     script.extract()    # rip it out
                all_links= soup.find_all("a")
                #print "--Soup Parsing at Lido Level DONE--- \n\n"

                #About_Us:
                #print "---About Us Execution---"
                try:
                    logging.info(" --ABOUT US STARTED-- ")
                    aboutus_text, abtus_url = au.aboutus(page,all_links, Company_url,counter)

                except Exception, e:
                    aboutus_text = abtus_url = "Not Found"
                    #print "LIDO ABOUT's EXCEPTIION: ", e
                    pass
                #print ":::::::::::::::Final ABOUT_US::::::::::::::::: type and text - "
                #print type(aboutus_text)
                #print aboutus_text
                #print "---About Us DONE--- \n\n"


                #Social_Profiles:
                #print "---Social Execution---"
                try:
                    logging.info(" --SOCIAL PROFILE STARTED-- ")

                    company_fb, company_yt, company_lin, company_tw, company_pi, google_pl,company_in,company_fl= sm.socialmedia(page,all_links)
                except Exception, e:
                    #print "LIDO SOCIAL's EXCEPTIION: ", e
                    #company_fb = company_yt = company_lin = company_tw = company_pi = google_pl= company_in= company_fl="Not Found"
                    pass

                #print "---Social DONE--- \n\n"

                #Contact_Us:
                #print "---Contact Us Execution---"
                try:
                    logging.info(" --CONTACT US STARTED-- ")

                    phone=[]
                    email=[]
                    phone1=[]
                    email1=[]
                    phone2=[]
                    email2=[]
                    fax="Not Found"
                    company="Not Found"
                    #print "Processing contacts on contact related page: "
                    phone, email,company, fax= ctus.contactus(all_links, Company_url, flag=0)
                    #print company

                    #print "Processing contacts on home page: "
                    #phone1, email1 = ctus.contactus(all_links, Company_url, flag=1)
                    #phone, email =  ctus.ct_homepg(phone,email,phone1,email1)

                    # to remove numbers ending with "-"
                    k=[]
                    if phone != "Not Found":
                        for j in phone:
                            #print j[-1]
                            if j[-1]=="-":
                                sasd=[]
                                #print "yes"
                                #k.append((j[:-1]))
                            else:
                                #print "no"
                                k.append((j[:]))
                        phone = k[:]
                    phone = str(phone).replace("[","").replace("]","").replace("'","")
                    email = str(email).replace("[","").replace("]","").replace("'","")

                except Exception, e:
                    #print "LIDO CONTACT's EXCEPTIION: ", e
                    #ct_us_text = ctus_url = phone = email = "Not Found"
                    pass
                if  phone == [] or phone=="" or phone==" ":
                    #print "EMPTY phone [] (due to exception)"
                    phone = "Not Found"
                if  email == [] or email == [ ] :
                    #print "EMPTY email [] (due to exception)"
                    email = "Not Found"
                if company== [] or company == [ ] or company == "" or company == " ":
                    company = "Not Found"
                if "javascript" in str(company):
                    #print "--WARNING: JAVASCRIPT IN ADDRESS--"
                    company="Not Found"
                if "jquery" in str(company):
                    #print "--WARNING: JAVASCRIPT IN ADDRESS--"
                    company="Not Found"
                if "{" and "}" and "#" in str(company):
                    if "}" in str(company):
                        if ";" in str(company):
                            #print "--WARNING: XML CODE IN ADDRESS--"
                            company="NOT FOUND"

                #print "THE END RESULTANT ADDRESS:",company

                if phone == "N, O, T,  , F, O, U, N, D":
                    phone="Not Found"
                    #print "YESSSSSSS"

                #print "Final Contact TO SAVE: ", phone, " EMAIL: ", email


                # print ":::::::::::::::Final CONTACT_US::::::::::::::::: type and text - \n"
                # print type(ct_us_text)
                # print ct_us_text
                #print "---Contact Us DONE--- \n\n"

                #To_Save:
                #type(data)
                #print "SAVE"
                data = [[Company_url,"Active",company_fb, company_yt, company_lin, company_tw, company_pi, google_pl,company_in,company_fl, email, phone,fax,company, aboutus_text]]
                #a.writerows(data)
                #print "DATA"
                #print data
                #print "---Saving DONE--- \n\n"
            except Exception,e:
                print "EXCEPTION IN THE END"

            #to_tuple
            list_Company_url.append(Company_url)
            list_abt.append(aboutus_text)
            #list_ct_us_text.append(ct_us_text)
            list_company_tel.append(phone)
            list_company_email.append(email)
            list_company_fb.append(company_fb)
            list_company_yt.append(company_yt)
            list_company_lin.append(company_lin)
            list_company_tw.append(company_tw)
            list_company_pi.append(company_pi)
            list_google_pl.append(google_pl)
            list_company_in.append(company_in)
            list_company_fl.append(company_fl)
            list_company_fax.append(fax)
            list_company_add.append(company)


            tuple = list(zip(list_Company_url, list_company_fb, list_company_yt, list_company_lin, list_company_tw, list_company_pi, list_google_pl,list_company_in,list_company_fl,list_company_email, list_company_tel,list_company_fax,list_company_add, list_abt))


            #tuple = list(zip(list_Company_url, list_abt, list_company_tel,list_company_email, list_company_fb, list_company_yt, list_company_lin, list_company_tw, list_company_pi, list_google_pl))
            print "ZIP TYPE: ", type(tuple), "LEN: ", len(tuple)
            print tuple
            return tuple





#if __name__ == '__main__':main()