# -*- coding: utf-8 -*-
import requests
import textwrap
import csv
from bs4 import BeautifulSoup
import nltk
import urllib2
import logging
from tld import get_tld
from collections import Counter
import string
import re
from collections import OrderedDict


def extract_entities(aboutus7):
    i=0
    for sent in nltk.sent_tokenize(aboutus7):
        #print(sent)
        var1 = nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent)))
        counter=0
        for j in var1:
            #print j
            zz=var1[i]
            i=i+1
            #print zz
            #print type(zz)
            t=0
            chunk=["JJ", "NN", "NNS", "JJR","JJS", "NN", "NNS", "NNP", "NNPS", "PRP","PRP$"]
            for item in zz:
                #print item
                if ("JJ" or "JJR" or "JJS" or "NN" or "NNS" or "NNP" or "NNPS" or "PRP" or "PRP$" in item):
                   #print ("FOUND")
                   counter=counter+1
                #counter=counter+1
        return counter

def compare_entities(c1,c2,c3,a1,a2,a3):
    if(c1>c2 and c1>c3 ):
        #print a1
        final_about=a1
        #print final_about
    else:
        if (c2>c1 and c2>c3):
        #print a2
            final_about=a2
            #print final_about
        else:
            final_about=a3
            #print final_about

    #print final_about
    return final_about

def count_letters(word, valid_letters=string.ascii_letters):
    count = Counter(word)
    return sum(count[letter] for letter in valid_letters)


def decode_compress_data(list):
    about=""
    for link in list:
        try:
            #print "p"
            #print(link.text)
            link = link.text
            #print type(link)
            link = link.encode('ascii','ignore')

            #s1=about
            #about = ''.join(c if c.isalnum() else ' ' for c in s1)
            link=str(link)
            link=link.replace("\n"," . ")
            link=link.replace("\&nbsp"," ")
            #link=link.strip()
            link = link.rstrip().lstrip()
            while "  " in link: # While  there are 2 spaces between words in our string...
                link = link.replace("  ", " ")

            #print "TYPEEEEEEE ",type(link)
            count = len(re.findall(r'\w+', link))
            #count= count_letters(link.text) ##For countinf letters
            #print "COUNT_____",count
            #print "____LINK",link, "\d"
            if count > 11:
                about=about+" || "+link
                #print "_T."
                about=about.encode('ascii','ignore')
            # stop ="JavaScript seems to be disabled in your browser."
            # print stop
            # #about=" ".join(filter(lambda word: word not in stop, about.split()))
            # stop1="You must have enabled utilize the functionality of this website."
            # #about=" ".join(filter(lambda word: word not in stop1, about.split()))
        except Exception, e:
            logging.error("warning Reason :: %s" % e)
            print e, "\d", "\d"
            continue

    #print about
    return about

def check_url(url,url1):
        y="http"
        x="www"
        check1= x in url1
        check2= y in url1

        if(check1== True or check2== True):
            #print "URL FETCHED IS : ",  url1
            ss=[]
        else:
            url1= url+'/'+url1
            #print "URL FETCHED IS (Added url+'/'+url1) : ", url1
        return url1

def about_search(url,links,list):

            list=[]
            aboutus = ["About&nbsp;Us","About","About-us", "Portfolio","About-US", "About the site","About Company","About Us","Who We Are","About the Company","Our Vision", "Our Mission", "Profile", "Company","What We Do","Brand","The Company" "The Brand", "THE BRAND", "Our History","about","about", "Corporate Overview","Who We Are", "About The Company","Brand","Our History","Corporate Information", "Corporate Structure","Introduction to the Company","Introduction to Company", "Business","Our Business","Company Profile", "About The Company", "About Company","Company", "Company Profile","Corporate Profile","Why us",'Who We Are ?','Who We Are?','About Us!','What We Do?','What We Do ?','Who We Are?', 'About Me']
            lo = [element.lower() for element in aboutus]
            up=[element.upper() for element in aboutus]
            title=[element.title() for element in aboutus]
            about7=aboutus+lo+up+title
            i=len(about7)
            for kin in links:
                #print "************Welcome to for Loop*************"
                #print kin.text
                #print kin
                #print "Step1"
                kin1=kin.text.encode('ascii','ignore')

                if (kin1=="About us" or kin1=="About"or kin1=="About Us"or kin1=="ABOUT US" or kin1=="AboutUs"or kin1=="Aboutus"):

                    list=kin
                    #print "Break- Exact About String Match"
                    break
                else:
                    td=get_tld(url)
                    td=str(td)
                    td=td.replace("."," ")
                    token=nltk.word_tokenize(td)
                    domain=token[0]
                    #print domain
                    #print kin
                    if ("About"+domain in kin1.strip() or "About"+domain.upper() in kin1.strip()or "ABOUT"+domain.upper() in kin1.strip()):
                        #print "Break- About URL Name Search"
                        #print kin
                        list=kin
                        break
                    else:
                        is_break = False
                        for a in about7:
                            #print "Search in list"

                            match= kin1==a
                            if(match==True):
                                list=kin
                                #print "Break- Matched in Exact List Search "
                                #print kin.text
                                is_break = True
                                break

                            else:
                                if (a in str(kin)):

                                    list=kin
                                    #print "Break- Match in Content Search"
                                    break
                                else:
                                     continue
                        if is_break: break
            return list

#ABOUT US FIRST FUNCTION TO CALL:
def aboutus(page,links,url,counter):

            format = '%(name)s : %(filename)s : %(asctime)s : %(lineno)s : %(levelname)s : %(message)s'
            logging.basicConfig(format=format,filename="Lido.log", level=logging.ERROR)
            try:
                list_about=about_search(url,links,list)
                #print "_1_"
                url1= list_about.get("href")
                #print "_2_ ", url1
                url_about=check_url(url,url1)
                #print "_3_"
                r = requests.get(url_about)
                #print "_4_"
                soup1 = BeautifulSoup(r.content,'html5lib')
                #print "_5_ \n"
                #print soup1.prettify()
                list1= soup1.find_all("p")
                list2=soup1.find_all("span")
                list3=soup1.find_all("div")
                #print "--Soup parsing for AboutUs DONE--\n"

                #print "Extracting About Us Text and Data_Cleaning"
                #print " For P_about:"
                p_about=decode_compress_data(list1)
                #print "\n For S_about:"
                s_about=decode_compress_data(list2)
                #print "\n For Div_about:"
                div_about=decode_compress_data(list3)
                #print "--About Us Text and Data_Cleaning DONE -- \n"

                #print "Finding Which tag to use: "
                counter1=extract_entities(p_about)
                counter3=extract_entities(s_about)
                counter2=extract_entities(div_about)

                #Entity Function Call
                final_about=compare_entities(counter1,counter2,counter3,p_about,div_about,s_about)
                #print "--extract_entities and Comparison DONE--\n"

                #print "____FINAL ABOUT US::____ ", type(final_about), final_about
                final_about = "\n".join(list(OrderedDict.fromkeys(final_about.split(" || "))))
                final_about = ".".join(list(OrderedDict.fromkeys(final_about.split("."))))
                #now stop words.. javascript, about us

            except Exception, e:
                #print e
                final_about=" Not Found"
                url1="Not Found"
                logging.error("warning Reason :: %s" % e)
                pass

            if final_about == '' :
                final_about = "Not Found"
            return final_about, url1