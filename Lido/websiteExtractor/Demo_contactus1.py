# -*- coding: utf-8 -*-

import requests
import textwrap
import csv
from bs4 import BeautifulSoup
import nltk
import urllib2
import logging
from tld import get_tld
#import socialmedia as sm

import re
from collections import Counter
import string

########################################################################################################################
#Fun1-to process and extract contact us
def contactus(all_links, Company_url):

            ##Fun1.1_Contact_Us_Variations_##
            print "Fun1.1 Begins : To fetch Contactus Link"
            list_cont=contact_search(Company_url,all_links)
            url1= list_cont.get("href")
            ##Fun1.1b_URL_Check_##
            url_cont=check_url(Company_url,url1)
            print "URL FETCHED:", url_cont, "\n"

            ##Extract_tags
            r = requests.get(url_cont)
            soup1 = BeautifulSoup(r.content,'lxml')
            #Use_p_and_span_tag

            all_div_tags=soup1.find_all("div")
            all_p_tags= soup1.find_all("p")
            all_s_tags=soup1.find_all("span")


            print "Fun1.2 Begins - Extract_Contact_Text_&_Data_Cleaning_"
            try:

                ##Fun1.2_Extract_Contact_Text_&_Data_Cleaning_##
                try:
                    print "For div_contact_txt::::: "
                    div_contact_txt = decode_compress_data(all_div_tags)
                    print "...div: ",div_contact_txt
                    print "Type of : div_contact_txt : ", type(div_contact_txt), "\n"
                except Exception, e:
                    pass

                try:
                    print "For p_contact_txt:::::"
                    p_contact_txt = decode_compress_data(all_p_tags)
                    print "..p: ", p_contact_txt
                    print "Type of : p_contact_txt : ", type(p_contact_txt), "\n"
                except Exception, e:
                    pass

                try:
                    print "For s_contact_txt:::::"
                    s_contact_txt = decode_compress_data(all_s_tags)
                    print "...s: ",s_contact_txt
                    print "Type of : s_contact_txt : ", type(s_contact_txt), "\n"
                except Exception, e:
                    pass

                print "--Done Text Extraction--", "\n"


                ##Fun1.3__Which_Tag_To_Use_##
                div_selected_tag_txt=[]
                #div_tag
                try:
                    print "--Now checking which tag to use and extract text from--"
                    div_selected_tag_txt = extract_entities(div_contact_txt)
                except Exception, e:
                    pass
                print "div_selected_tag_txt: ", div_selected_tag_txt, "\n"

                #p_tag
                try:
                    p_selected_tag_txt = extract_entities(p_contact_txt)
                    print  "p_selected_tag_txt: ", p_selected_tag_txt, "\n"
                except Exception, e:
                     pass


                #s_tag
                try:
                     s_selected_tag_txt=extract_entities(s_contact_txt)
                     print  "s_selected_tag_txt: ", s_selected_tag_txt, "\n"
                except Exception, e:
                     pass
                final_contactus = p_selected_tag_txt
                #final_contactus = div_selected_tag_txt
                if final_contactus == [] :
                    final_contactus = p_selected_tag_txt
                    final_contactus = div_selected_tag_txt
                if final_contactus == [] :
                    final_contactus = s_selected_tag_txt


                print "Final Contactus text::"
                print final_contactus

                print url1, "\n"
            except Exception,e:
                print "ERROR", e
                pass
            email, phone=email_phn(div_contact_txt,p_contact_txt,s_contact_txt)
            print email, phone
            return final_contactus , url1,phone,email


def email_phn(div_contact_txt,p_contact_txt,s_contact_txt):

        print "TYPE OF DIV AND P TEXT::::::::  ",type(div_contact_txt), type(p_contact_txt)
        print "Div and p text:", div_contact_txt, "\n", p_contact_txt
        print len(div_contact_txt), len(p_contact_txt)
        try:
            phone_p=[]
            email_p=[]
            phone_s=[]
            email_s=[]
            phone_div=[]
            email_div=[]
            email=[]
            phone=[]
            #Div_Tag
            regex = re.compile('[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
            email_matched = regex.search(div_contact_txt)
            if email_matched:
                email_div=email_matched.group()
                print "email_div-----", email_div

            regex_ph = re.compile('\+?[ ]?\(?\+?[1-9]{2,6}\)?[ ]?\-??[0-9]{2,14}[ ]?\-?[0-9]{3,14}-?\d{0,10}-?\d{0,10}')
            phone_matched = regex_ph.search(div_contact_txt)
            if phone_matched:
                phone_div = phone_matched.group()
                print "phone_div----",  phone_div

            #P_TAG:
            regex = re.compile('[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
            email_matched = regex.search(p_contact_txt)
            if email_matched:
                email_p=email_matched.group()
                print "email_p-----",email_p

            regex_ph = re.compile('\+?[ ]?\(?\+?[1-9]{2,6}\)?[ ]?\-??[0-9]{2,14}[ ]?\-?[0-9]{3,14}-?\d{0,10}-?\d{0,10}')
            phone_matched = regex_ph.search(p_contact_txt)
            if phone_matched:
                phone_p = phone_matched.group()
                print "phone_p-----", phone_p

            #SPAN_TAG:
            regex = re.compile('[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
            email_matched = regex.search(s_contact_txt)
            if email_matched:
                email_p=email_matched.group()
                print "email_p-----",email_s

            regex_ph = re.compile('\+?[ ]?\(?\+?[1-9]{2,6}\)?[ ]?\-??[0-9]{2,14}[ ]?\-?[0-9]{3,14}-?\d{0,10}-?\d{0,10}')
            phone_matched = regex_ph.search(s_contact_txt)
            if phone_matched:
                phone_p = phone_matched.group()
                print "phone_p-----", phone_s

            print "1.YES============================"
            print email_div, "\n",phone_div,"\n", phone_p,"\n", email_p
            print "2.YES============================"
        except Exception ,e:
            print "ttttttt.EXCEPTIPN REGEX============================"
            print e, "\n"
        pass
        print email_p
        print email_div
        print phone_p
        print phone_div
        try:
            if email_div==email_p and  email_p==email_s:
                email=email_p
            else:
                if email_div==[] and email ==[] and email_s==[]:
                    email=email_p
                if email_p==[] and email ==[]and email_s==[]:
                    email=email_div
                if email_p==[] and email ==[]and email_div==[]:
                    email=email_s
                if email_div==[] and email_p==[] and email_s==[] and email ==[]:
                    email="no email found"

            if email==[] and email_p!=[] and email_div !=[] and email_s==[]:
                email=email_div+", "+email_p
                print email
            if email==[] and email_p!=[] and email_s !=[] and email_div==[] :
                email=email_div+", "+email_s
                print email
            if email==[] and email_s!=[] and email_div !=[] and email_p==[]:
                email=email_div+", "+email_s
                print email
            if email==[] and email_p!=[] and email_div !=[]and email_s!=[]:
                email=email_div+", "+email_p+", "+email_s
                print email

            print "Final Email",email


            if phone_div==phone_p and  phone_p==phone_s:
                phone=phone_p
            else:
                if phone_div==[] and phone ==[] and phone_s==[]:
                    phone=phone_p
                if phone_p==[] and phone ==[]and phone_s==[]:
                    phone=phone_div
                if phone_p==[] and phone ==[]and phone_div==[]:
                    phone=phone_s
                if phone_div==[] and phone_p==[] and phone_s==[] and phone ==[]:
                    phone="no phone found"

            if phone==[] and phone_p!=[] and phone_div !=[] and phone_s==[]:
                phone=phone_div+", "+phone_p
                print phone
            if phone==[] and phone_p!=[] and phone_s !=[] and phone_div==[] :
                phone=phone_div+", "+phone_s
                print phone
            if phone==[] and phone_s!=[] and phone_div !=[] and phone_p==[]:
                phone=phone_div+", "+phone_s
                print phone
            if phone==[] and phone_p!=[] and phone_div !=[]and phone_s!=[]:
                phone=phone_div+", "+phone_p+", "+phone_s
                print phone


            print "DONE ", phone

        except Exception ,e:
            print "EXCEPTION CONTACT US"
            print e, "\n"

        print "THIS IS EMAIL : ", email, "   ::  ", "THIS IS PHONE : ", "phone ", phone

        return email, phone
########################################################################################################################
##Fun1.1a_Contact_Us_&_Variations_########

def contact_search(url,links):

            list=[]

            contactus = ["contact", "contactus", "contact us", "Meet us", "Meet-us","Contact", "CONTACT", "CONTACT US", "Contact Us", "contact-us", "contact_us", "contactus", "meet_us", "meetus"]

            lo = [element.lower() for element in contactus]
            up=[element.upper() for element in contactus]
            contactus7=contactus+lo+up

            i=len(contactus7)
            for kin in links:
                #print "************Welcome to for Loop*************"
                #print kin.text
                #print kin
                #print "Step1"
                kin1=kin.text.encode('ascii','ignore')

                if (kin1 in contactus7):

                    list=kin
                    #print "Break- Exact Contact String Match"
                    break
                else:

                    #To check "Contact IBM"
                    td=get_tld(url)
                    td=str(td)
                    td=td.replace("."," ")
                    token=nltk.word_tokenize(td)
                    domain=token[0]
                    #print domain
                    #print kin
                    if ("Contact "+domain in kin1.strip() or "Contact "+domain.upper() in kin1.strip() or "CONTACT "+domain.upper() in kin1.strip() or "Contact-"+domain.upper() in kin1.strip() or "CONTACT-"+domain.upper() in kin1.strip() or "Meet "+domain.upper() in kin1.strip() ):
                        #print "Break- Contact URL Name Search"
                        #print kin
                        list=kin
                        break
                    else:
                        is_break = False
                        for a in contactus7:
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


####Fun1.1b_URL_Check_####
def check_url(url,url1):
        y="http"
        x="www"
        check1= x in url1
        check2= y in url1

        if(check1== True or check2== True):
            print url1
        else:
            url1= url+'/'+url1
            print url1
        return url1

########################################################################################################################

##Fun1.2_Extract_Contact_Text_&_Data_Cleaning_##
def decode_compress_data(list):

    print "1.2-A"
    print type(list)
    #print list
    contact_text1 = ""
    contact_text = ""
    print type(contact_text)
    #contact_text=list.text
    for link in list:
            contact_text1=link.text.encode('ascii','ignore')
            #print link.text
            #print "RAM"
            #print type(contact_text1)
            contact_text=contact_text+contact_text1

    #contact_text=str(contact_text)
    print "1.2-B"
    #print contact_text
    contact_text=contact_text.replace("\n"," ")
    print "1.2-c"
    contact_text=contact_text.replace("\&nbsp"," ")
    print "1.2-d"
    contact_text=contact_text.strip()
    #print "B. ", contact_text

    return contact_text


########################################################################################################################
def extract_entities(contact):

    try:
        regex = re.compile('[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
        email_matched = regex.search(contact)
        email=email_matched.group()
        print email_matched.group()
    except Exception, e:
        pass

    digit = False
    print digit
    org = False
    location = False
    '''for sent in nltk.sent_tokenize(contact):
        print "SENTENCE"
        print sent'''
    var1 = nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(contact)))
    #print "TTTTTT", var1
    for i in var1:
            #print "I"
            if isinstance(i,nltk.tree.Tree):
                if i.node == 'GPE':
                    location = True
                if i.node == "ORGANIZATION":
                    org = True
            for j in i:
                #print j
                if digit == False :
                    #print "RAM"
                    digit= (('CD') in i)
                    #print "DIGIT"
                    #print digit
    print digit, location, org
    #print "ZERO"
    if ((digit and location and org == True ) and email_matched ):
        print "FOUND"
        #print contact
        contact = contact
    else:
        contact="NOT MATCHED"
        print "NOT MATCHED"
        contact=[]
    return contact



########################################################################################################################
########################################################################################################################

