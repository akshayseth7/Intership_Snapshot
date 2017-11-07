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


def extract_entities(aboutus7):
    i=0
    for sent in nltk.sent_tokenize(aboutus7):
        ##print(sent)
        var1 = nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent)))
        counter=0
        for j in var1:
            ##print j
            zz=var1[i]
            i=i+1
            ##print zz
            ##print type(zz)
            t=0
            chunk=["JJ", "NN", "NNS", "JJR","JJS", "NN", "NNS", "NNP", "NNPS", "PRP","PRP$"]
            for item in zz:
                ##print item
                if ("JJ" or "JJR" or "JJS" or "NN" or "NNS" or "NNP" or "NNPS" or "PRP" or "PRP$" in item):
                   ##print ("FOUND")
                   counter=counter+1
                #counter=counter+1
        return counter

def compare_entities(c1,c2,a1,a2):
    if(c1>c2):
        ##print a1
        final_about=a1
        #print final_about
    else:
        ##print a2
        final_about=a2
        #print final_about
    ##print final_about
    return final_about

def count_letters(word, valid_letters=string.ascii_letters):
    count = Counter(word)
    return sum(count[letter] for letter in valid_letters)


def decode_compress_data(list):
    about=""
    for link in list:

        ##print "p"
        ##print(link.text)
        ##print type(link.text)
        count= count_letters(link.text)
        ##print link
        if count > 50:
            about=about+link.text
            about=about.encode('ascii','ignore')
        stop ="JavaScript seems to be disabled in your browser."
        ##print stop
        about=" ".join(filter(lambda word: word not in stop, about.split()))
        stop1="You must have enabled utilize the functionality of this website."
        about=" ".join(filter(lambda word: word not in stop1, about.split()))

    s1=about
    #about = ''.join(c if c.isalnum() else ' ' for c in s1)
    about=str(about)
    about=about.replace("\n","")
    about=about.replace("\&nbsp","")
    about=about.strip()
    #print about
    return about

def check_url(url,url1):
        y="http"
        x="www"
        check1= x in url1
        check2= y in url1

        if(check1== True or check2== True):
            ##print url1
            None
        else:
            url1= url+'/'+url1
            #print url1
        return url1

def about_search(url,links,list):

            list=[]
            aboutus = ["About&nbsp;Us","About","About-us", "About-US", "About Us","Who We Are","About the Company","Our Vision", "Our Mission", "Profile", "Company","What We Do","Brand","The Company" "The Brand", "THE BRAND", "Our History", "Our Business", "Business", "Corporate Overview","Who We Are", "About The Company","Brand","Our History", "Our Business", "Business","Corporate Information", "Corporate Structure","Introduction to the Company","Introduction to Company", "Company Profile", "About The Company", "About Company","Company", "Company Profile","Corporate Profile","Why us" ]
            lo = [element.lower() for element in aboutus]
            up=[element.upper() for element in aboutus]
            about7=aboutus+lo+up
            i=len(about7)
            for kin in links:
                #print "************Welcome to for Loop*************"
                ##print kin.text
                ##print kin
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
                    ##print domain
                    ##print kin
                    if ("About"+domain in kin1.strip() or "About"+domain.upper() in kin1.strip()or "ABOUT"+domain.upper() in kin1.strip()):
                        #print "Break- About URL Name Search"
                        ##print kin
                        list=kin
                        break
                    else:
                        is_break = False
                        for a in about7:
                            ##print "Search in list"

                            match= kin1==a
                            if(match==True):
                                list=kin
                                #print "Break- Matched in Exact List Search "
                                ##print kin.text
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

def aboutus(page,links,url,counter):
            list_about=about_search(url,links,list)
            url1= list_about.get("href")
            url_about=check_url(url,url1)
            r = requests.get(url_about)
            soup1 = BeautifulSoup(r.content,'lxml')
            ##print soup1.prettify()

            list1= soup1.find_all("p")
            list2=soup1.find_all("span")
            p_about=decode_compress_data(list1)
            s_about=decode_compress_data(list2)
            counter1=extract_entities(p_about)
            ##print "$$$$$"
            ##print counter1
            ##print counter
            counter3=extract_entities(s_about)
            ##print counter3
            #Entity Function Call
            final_about=compare_entities(counter1,counter3,p_about,s_about)
            return final_about,url1