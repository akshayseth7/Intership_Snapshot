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
import requests
from lxml import etree
from StringIO import StringIO
from collections import Counter
import string
import textwrap
from nltk.corpus import stopwords



########################################################################################################################
#MAIN CONTACT FUNCTION:
#Fun1-to process and extract contact us
def contactus(all_links, url_cont, flag):
            format = '%(name)s : %(filename)s : %(asctime)s : %(lineno)s : %(levelname)s : %(message)s'
            logging.basicConfig(format=format,filename="Lido.log", level=logging.ERROR)

            ##Fun1.1_Contact_Us_Variations_##
            #print "Fun1.1 Begins : To fetch Contactus Link"
            main_url=url_cont
            list_cont=contact_search(url_cont,all_links)
            url1= list_cont.get("href")
            ##Fun1.1b_URL_Check_##
            if flag == 0:
                url_cont=check_url(url_cont,url1)
            #print "URL FETCHED:", url_cont, "\n"

            ##Extract_tags
            r = requests.get(url_cont)
            soup1 = BeautifulSoup(r.content,'lxml')
            #Use_p_and_span_tag

            all_div_tags=soup1.find_all("div")
            all_p_tags= soup1.find_all("p")
            all_s_tags=soup1.find_all("span")
            all_tr_tags=soup1.find_all("tr")


            #print "Fun1.2 Begins - EXTRACT CONTACT DETAILS LIKE PHONE EMAIL &_Data_Cleaning_"
            try:

                ##Fun1.2_Extract_Contact_Text_&_Data_Cleaning_##
                try:
                    #print "For div_contact_txt::::: "
                    div_contact_txt = decode_compress_data(all_div_tags)
                    # print "----------------TEXT ...div: After Decode_compress ----------------"
                    # print div_contact_txt
                    #print "------------------------------------------"
                    #print "Type of : div_contact_txt : ", type(div_contact_txt), "\n"
                except Exception, e:
                    pass

                try:
                    #print "For p_contact_txt:::::"
                    p_contact_txt = decode_compress_data(all_p_tags)
                    # print "----------------TEXT ..p: After Decode_compress ----------------"
                    # print p_contact_txt
                    #print "------------------------------------------"
                    #print "Type of : p_contact_txt : ", type(p_contact_txt), "\n"
                except Exception, e:
                    pass

                try:
                    #print "For s_contact_txt:::::"
                    s_contact_txt = decode_compress_data(all_s_tags)
                    # print "----------------TEXT ...s: After Decode_compress ----------------: "
                    # print s_contact_txt
                    #print "----------------------------------------------"
                    #print "Type of : s_contact_txt : ", type(s_contact_txt), "\n"
                except Exception, e:
                    pass

                try:
                    #print "For tr_contact_txt::::: "
                    tr_contact_txt = decode_compress_data(all_tr_tags)
                    # print "----------------TEXT ...tr: After Decode_compress ----------------"
                    # print div_contact_txt
                    #print "--------------------------------------------"
                    #print "Type of : div_contact_txt : ", type(tr_contact_txt), "\n"
                except Exception, e:
                    pass

                #print "--Done Contact Text Extraction--", "\n"

                ## EMAIL and PHONE FETCHING:
                #print "Fun1.2a Begins - FUNCTION FOR PHONE EMAIL: "
                email, phone = email_phn(div_contact_txt,p_contact_txt,s_contact_txt, tr_contact_txt)
                #print email, phone

                ## Fax:
                fax = fax_number(div_contact_txt,p_contact_txt,s_contact_txt, tr_contact_txt)
                #print "EMAILLLLLLLLL PHONEEEEEEE", email, phone
                for i in phone:
                    fax_cln = int(filter(str.isdigit, fax))
                    i_cln=int(filter(str.isdigit, i))
                    if i_cln == fax_cln:
                        phone.remove(i)
                        #print "CLEARED MATCHED FAX IN PHONE"

            except Exception,e:
                #print "EXCEPTION IN CONTACT DETAILS : : ", e
                email="Not Found"
                phone="Not Found"
                pass

            ## Address MAIN FUNCTION:
            #print "\n =================FETCHING ADSRESS:================= "
            try:
                company_address = address_company(main_url, div_contact_txt,p_contact_txt,s_contact_txt, tr_contact_txt)

                #Again Cleaning of address:
                link=str(company_address)
                link=link.replace("\n"," . ")
                link=link.replace("\&nbsp"," . ")
                #link=link.strip()
                link = link.rstrip().lstrip()
                while "  " in link: # While  there are 2 spaces between words in our string...
                    link = link.replace("  ", " ")
                while "  ." in link: # While  there are 2 spaces between words in our string...
                    link = link.replace("  ", ". ")
                company=link

            except Exception,e:
                #print "EXCEPTION IN ADDRESS: : ", e
                company="Not Found"
                pass
            #print "FINALLY THE RETURNED ADDRESS IS: ", company

            #For Making all empty entities "Not Found" :
            if  phone == '':
                #print "phone is empty = '' "
                phone = "Not Found"
            if  phone == []:
                #print "phone is []"
                phone = "Not Found"
            if email == '':
                #print "email is empty = '' "
                email = "Not Found"
            if email == []:
                #print "email is []"
                email = "Not Found"

            return phone,email,company, fax


########################################################################################################################
##Fun1.1a_Contact_Us_&_Variations_########

def contact_search(url,links):

            list=[]

            contactus = ["contact", "contactus", "contact us", "Meet us","We Are Here", "Meet-us","Contact", "CONTACT", "CONTACT US", "Contact Us", "contact-us", "contact_us", "contactus", "meet_us", "meetus", "Locations", "Our Locations", "Contact Me", "Join Us", "Get In Touch", "Our presence", "Our Office", "find us", "engage us", "where we are?","here we are", "Contact Info","Office Information", "Contact Information" , "Office Locations", "Locations"]

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
            #print url1
            dwfwd=[]
        else:
            url1= url+'/'+url1
            #print url1
        return url1

########################################################################################################################

##Fun1.2_Extract_Contact_Text_&_Data_Cleaning_##
def decode_compress_data(list):

    #print "1.2-A"
    #print type(list)
    #print list
    #contact_text1 = ""
    contact_text = " "
    #print type(contact_text)
    #contact_text=list.text
    i=0
    for link in list:
        # print "FOR ITERATION: ", i
        # contact_text1=link.text
        contact_text1=link.text.encode('ascii','ignore')

        #print "11111111111111", contact_text1


        # print link.text
        #print type(contact_text1),contact_text1
        contact_text = contact_text+" || "+contact_text1
        #print contact_text
        # i =i +1
    contact_text=" ".join(contact_text.split())
    #print "TEXT WRAP", contact_text
    # print type(contact_text),contact_text
    contact_text=str(contact_text)
    #print "1.2-B- JAI HO"
    #print contact_text
    contact_text=contact_text.replace("\n"," ")
    #print "1.2-c"
    contact_text=contact_text.replace("\&nbsp"," ")
    #print "1.2-d"
    contact_text=contact_text.strip()
    #print "B. ", contact_text
    #print "CONTACT US FROM decode_compress_data() FUNCTION::  ", contact_text
    return contact_text

########################################################################################################################


def email_phn(div_contact_txt,p_contact_txt,s_contact_txt, tr_contact_txt):

        #print "TYPE OF DIV AND P TEXT::::::::  ", type(div_contact_txt), type(p_contact_txt), type(s_contact_txt), type(tr_contact_txt)
        #print "Div, p, span and tr text:", div_contact_txt, "\n", p_contact_txt,"\n",s_contact_txt,"\n",tr_contact_txt
        #print len(div_contact_txt), len(p_contact_txt), len(s_contact_txt), len(tr_contact_txt)

        try:
            phone_p=[]
            email_p=[]

            phone_s=[]
            email_s=[]

            phone_div=[]
            email_div=[]

            email=[]
            phone=[]

            #Div_Tag:
            email_div = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", div_contact_txt)
            phone_div = re.findall(r"\+?[ ]?\(?\+?[1-9]{1,4}\)?-?[ ]?\-?\(?[0-9]{1,10}\)?\-?[ ]?[0-9]{3,3}-?\d{0,10}-?[ ]?\d{0,10}", div_contact_txt)

            #P_TAG:
            email_p = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", p_contact_txt)
            phone_p = re.findall(r"\+?[ ]?\(?\+?[1-9]{1,4}\)?-?[ ]?\-?\(?[0-9]{1,10}\)?\-?[ ]?[0-9]{3,3}-?\d{0,10}-?[ ]?\d{0,10}", p_contact_txt)
            
            #SPAN_TAG:
            email_s = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", s_contact_txt)
            phone_s = re.findall(r"\+?[ ]?\(?\+?[1-9]{1,4}\)?-?[ ]?\-?\(?[0-9]{1,10}\)?\-?[ ]?[0-9]{3,3}-?\d{0,10}-?[ ]?\d{0,10}", s_contact_txt)

            #Tr_TAG
            email_tr = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", tr_contact_txt)
            phone_tr = re.findall(r"\+?[ ]?\(?\+?[1-9]{1,4}\)?-?[ ]?\-?\(?[0-9]{1,10}\)?\-?[ ]?[0-9]{3,3}-?\d{0,10}-?[ ]?\d{0,10}", tr_contact_txt)
            
            #Adding all:
            email1 = email_div + email_p + email_s + email_tr
            phone1 = phone_div + phone_p + phone_s + phone_tr

            # print "FINAL EMAIL AND PHONE TO RETURN: \n", "EMAIL : ", email1, "\n", " PHONE: ", phone1

            #to remove duplicates:
            [phone.append(i) for i in phone1 if not i in phone]
            [email.append(i) for i in email1 if not i in email]

            phone1 = phone[:]
            index = 1
            #print "LEN OF PHONE LIST:  ", len(phone), "\n"
            for all in phone1:
                # print "COUNT OF LOOP:", index, " ,RUNNING FOR : ", all
                # print "ITS LENGTH: ", len(str(all)), type(all), all
                # print "ACTUAL LIST : ", type(phone1), phone1
                allz = all.replace(" ", "")
                numb = (filter(str.isalnum, (all)))
                # print "AFTER CLEANING: ", numb, type(numb)
                # print "LEN of this: ", len(numb)
                if (len(numb) < 8) or (len(numb) > 14):
                    # print ("REMOVED")
                    phone.remove(all)
                    #print "THEREFORE: ", phone, "\n"
                # print "THEREFORE: ", phone, "\n"
                index = index+1
                #print "-------------------------"
            # print "BEFORE range: ", phone1
            #print "FINAL AFTER PHONE RANGE 7-14: ", phone

            #print "ACTUAL: ", phone1
            #print email

            return  email,phone
        except Exception, e:
            #print e
            phone="Not Found"
            email="Not Found"

            pass


########################################################################################################################


def address_company(main_url, div_contact_txt1, p_contact_txt1, s_contact_txt1, tr_contact_txt1):

        div_contact_txt = div_contact_txt1.lower()
        p_contact_txt = p_contact_txt1.lower()
        s_contact_txt = s_contact_txt1.lower()
        tr_contact_txt = tr_contact_txt1.lower()
        #print "TYPE OF DIV AND P TEXT::::::::  ", type(div_contact_txt), type(p_contact_txt), type(s_contact_txt), type(tr_contact_txt)
        #print "Div text:", div_contact_txt, "\n", "p_contact txt: ",p_contact_txt," \ns_div text: ",s_contact_txt,"\ntr_div_text: ",tr_contact_txt
        #print "Length of div, p, span, tr: ",len(div_contact_txt), len(p_contact_txt), len(s_contact_txt), len(tr_contact_txt)

        try:

            try:
                #to fetch Comapny Name (Title) :
                parser = etree.HTMLParser()
                r = requests.get(main_url)
                html = r.text
                tree  = etree.parse(StringIO(html), parser)
                titled = tree.xpath('//title/text()')
                #print main_url, titled
                # fst_title=titled[0]
                title = str(titled)
                title=title.lower()
                title1word = title.split()
                #print title1word[0], type(title1word[0])
                try:
                    title = title1word[0] + " " + title1word[1]
                    title = title.replace("['","")
                    #print "Title is :::::::::::::::: ", title
                except Exception, e:
                    #print e
                    title = title1word[0][0].encode("ascii", "ignore")
            except Exception, e:
                logging.error("warning Reason :: %s" % e)
                #print e
                title = "contact"

            title = title.replace("[u'","").replace("[","").replace("]","").replace("'","")
            #print "FINAL TITLE OF THE COMPANY:", title, "\n"

            ## Rules::::

            #print "\n Rule 1: address till phone"
            start = "address"
            tag = div_contact_txt
            check1a, add_rule1a = add_reg_phone(start, tag,title)
            tag = s_contact_txt
            check1b, add_rule1b = add_reg_phone(start, tag,title)
            tag = p_contact_txt
            check1c, add_rule1c = add_reg_phone(start, tag,title)
            tag = tr_contact_txt
            check1d, add_rule1d = add_reg_phone(start, tag,title)
            ## now add checking function here for all these tags:
            address = handling_all_add(check1a, add_rule1a, check1b, add_rule1b, check1c, add_rule1c, check1d, add_rule1d)
            #print "----Rule 9 Finished----\n"

            if address == "\n Not Found" or address == "[] ++ [] ++ [] ++ []" or address == "Not Found ++ Not Found ++ Not Found ++ Not Found" or address == "[]" or address == []or address == "'[]'":
                #print "Rule 2: address till pin"
                start = "address"
                tag = div_contact_txt
                check2a, add_rule2a = add_reg_pin(start, tag,title)
                tag = s_contact_txt
                check2b, add_rule2b = add_reg_pin(start, tag,title)
                tag = p_contact_txt
                check2c, add_rule2c = add_reg_pin(start, tag,title)
                tag = tr_contact_txt
                check2d, add_rule2d = add_reg_pin(start, tag,title)
                ## now add checking function here for all these tags:
                address = handling_all_add(check2a, add_rule2a, check2b, add_rule2b, check2c, add_rule2c, check2d, add_rule2d)
                #print "RULE 2 FINISHED \n"
                #print "----Rule 2 Finished----\n"

                if address == "\n Not Found" or address == "[] ++ [] ++ [] ++ []" or address == "Not Found ++ Not Found ++ Not Found ++ Not Found" or address == "[]" or address == []or address == "'[]'":
                    #print "Rule 3: contact till phone"
                    start = "contact"
                    tag = div_contact_txt
                    check3a, add_rule3a = add_reg_phone(start, tag,title)
                    tag = s_contact_txt
                    check3b, add_rule3b = add_reg_phone(start, tag,title)
                    tag = p_contact_txt
                    check3c, add_rule3c = add_reg_phone(start, tag,title)
                    tag = tr_contact_txt
                    check3d, add_rule3d = add_reg_phone(start, tag,title)
                    ## now add checking function here for all these tags:
                    address = handling_all_add(check3a, add_rule3a, check3b, add_rule3b, check3c, add_rule3c, check3d, add_rule3d)
                    #print "----Rule 3 Finished----\n"

                    if address == "\n Not Found" or address == "[] ++ [] ++ [] ++ []" or address == "Not Found ++ Not Found ++ Not Found ++ Not Found" or address == "[]" or address == []or address == "'[]'":
                        #print "Rule 4: contact till pin"
                        start = "contact"
                        tag = div_contact_txt
                        check4a, add_rule4a = add_reg_pin(start, tag,title)
                        tag = s_contact_txt
                        check4b, add_rule4b = add_reg_pin(start, tag,title)
                        tag = p_contact_txt
                        check4c, add_rule4c = add_reg_pin(start, tag,title)
                        tag = tr_contact_txt
                        check4d, add_rule4d = add_reg_pin(start, tag,title)
                        ## now add checking function here for all these tags:
                        address = handling_all_add(check4a, add_rule4a, check4b, add_rule4b, check4c, add_rule4c, check4d, add_rule4d)
                        #print "----Rule 4 Finished----\n"

                        if address == "\n Not Found" or address == "[] ++ [] ++ [] ++ []" or address == "Not Found ++ Not Found ++ Not Found ++ Not Found" or address == "[]" or address == []or address == "'[]'":
                            #print "Rule 5: location till phone"
                            start = "location"
                            tag = div_contact_txt
                            check5a, add_rule5a = add_reg_phone(start, tag,title)
                            tag = s_contact_txt
                            check5b, add_rule5b = add_reg_phone(start, tag,title)
                            tag = p_contact_txt
                            check5c, add_rule5c = add_reg_phone(start, tag,title)
                            tag = tr_contact_txt
                            check5d, add_rule5d = add_reg_phone(start, tag,title)
                            ## now add checking function here for all these tags:
                            address = handling_all_add(check5a, add_rule5a, check5b, add_rule5b, check5c, add_rule5c, check5d, add_rule5d)
                            #print "----Rule 5 Finished----\n"

                            if address == "Not Found" or address == "[] ++ [] ++ [] ++ []" or address == "Not Found ++ Not Found ++ Not Found ++ Not Found" or address == "[]" or address == []or address == "'[]'":
                                #print "\n Rule 6: location till pin"
                                start = "location"
                                tag = div_contact_txt
                                check6a, add_rule6a = add_reg_pin(start, tag,title)
                                tag = s_contact_txt
                                check6b, add_rule6b = add_reg_pin(start, tag,title)
                                tag = p_contact_txt
                                check6c, add_rule6c = add_reg_pin(start, tag,title)
                                tag = tr_contact_txt
                                check6d, add_rule6d = add_reg_pin(start, tag,title)
                                ## now add checking function here for all these tags:
                                address = handling_all_add(check6a, add_rule6a, check6b, add_rule6b, check6c, add_rule6c, check6d, add_rule6d)
                                #print "----Rule 6 Finished----\n"

                                if address == "Not Found" or address == "[] ++ [] ++ [] ++ []" or address == "Not Found ++ Not Found ++ Not Found ++ Not Found" or address == "[]" or address == []or address == "'[]'":
                                    #print "\n Rule 7: title till phone"
                                    start = title
                                    tag = div_contact_txt
                                    check7a, add_rule7a = add_reg_phone(start, tag,title)
                                    tag = s_contact_txt
                                    check7b, add_rule7b = add_reg_phone(start, tag,title)
                                    tag = p_contact_txt
                                    check7c, add_rule7c = add_reg_phone(start, tag,title)
                                    tag = tr_contact_txt
                                    check7d, add_rule7d = add_reg_phone(start, tag,title)
                                    ## now add checking function here for all these tags:
                                    address = handling_all_add(check7a, add_rule7a, check7b, add_rule7b, check7c, add_rule7c, check7d, add_rule7d)
                                    #print "----Rule 7 Finished----\n"

                                    if address == "Not Found" or address == "[] ++ [] ++ [] ++ []" or address == "Not Found ++ Not Found ++ Not Found ++ Not Found" or address == "[]" or address == []or address == "'[]'":
                                        #print "\n Rule 8: title till pin"
                                        start = title
                                        tag = div_contact_txt
                                        check8a, add_rule8a = add_reg_phone(start, tag,title)
                                        tag = s_contact_txt
                                        check8b, add_rule8b = add_reg_phone(start, tag,title)
                                        tag = p_contact_txt
                                        check8c, add_rule8c = add_reg_phone(start, tag,title)
                                        tag = tr_contact_txt
                                        check8d, add_rule8d = add_reg_phone(start, tag,title)
                                        ## now add checking function here for all these tags:
                                        address = handling_all_add(check8a, add_rule8a, check8b, add_rule8b, check8c, add_rule8c, check8d, add_rule8d)
                                        #print "----Rule 8 Finished----\n"

                                        if address == "Not Found" or address == "[] ++ [] ++ [] ++ []" or address == "Not Found ++ Not Found ++ Not Found ++ Not Found" or address == '[]' or address == []or address == "'[]'":
                                            #print "\n Rule 9: Checking only the Phone here: "
                                            start = " "
                                            tag = div_contact_txt
                                            check9a, add_rule9a = add_reg_phone(start, tag,title)
                                            tag = s_contact_txt
                                            check9b, add_rule9b = add_reg_phone(start, tag,title)
                                            tag = p_contact_txt
                                            check9c, add_rule9c = add_reg_phone(start, tag,title)
                                            tag = tr_contact_txt
                                            check9d, add_rule9d = add_reg_phone(start, tag,title)
                                            ## now add checking function here for all these tags:
                                            address = handling_all_add(check9a, add_rule9a, check9b, add_rule9b, check9c, add_rule9c, check9d, add_rule9d)
                                            #print "----Rule 9 Finished----\n"

                                            if address == "[] ++ [] ++ [] ++ []":
                                                #print "\n Rule 10: For Not Found"
                                                #print "Address is Not Found as it is IN COMPLETE ELSE PART \n "
                                                address = "Not Found"
                                                #print "----Rule 10 Else Part Finished----\n"
                                                #address == div_contact_txt1
                                            else:
                                                #print "Address is Not Found as it is IN COMPLETE ELSE PART \n"
                                                address = "Not Found"

            if "++" in address:
                        #print "ADD BEFORE SPLIT: ", address
                        add = address.split("++")
                        #print "ADDRESS SPLITED BY ++: ", add
                        p =[]
                        for e in add:
                            e=e.strip()
                            #print e

                            if e in p:
                                dfsad=""
                            #print "Repeated Address"

                            else:
                                p.append(e)
                        #print p
                        address=p

            #Final Address Cleaning:
            #print "CLEANING STARTS HERE : "
            address = clean_add(address)
            #print "Final Address To Return::::::::: ", address

        except Exception, e:
            address = "Not Found"
            #print "EXCEPTION IN ADDRESS MAIN FUNCTION: ",e
            logging.error("warning Reason :: %s" % e)
            pass


        return address



########################################################################################################################

def fax_number(div_contact_txt,p_contact_txt,s_contact_txt, tr_contact_txt):
    fax_num = "Not Found"
    div_contact_txt = div_contact_txt.lower()
    #print div_contact_txt
    if "fax" in div_contact_txt:
        #print "yes.....in tr div"
        #print fxx.split("div_contact_txt")
        #print fx
        regexp = re.compile("fax(.*)")
        fn= regexp.search(div_contact_txt).group(1)
        fax_num = re.findall(r"\+?[ ]?\(?\+?[1-9]{1,4}\)?-?[ ]?\-?\(?[0-9]{1,10}\)?\-?[ ]?[0-9]{3,3}-?\d{0,10}-?[ ]?\d{0,10}", fn)
        fax_num=fax_num[0]
        #print "FAX NUMBER___+_+_+_+_+_+_++_+_+_+_+_+_+_+_+_+__+_+_+_+_+_+_+_+_", fax_num

    p_contact_txt = p_contact_txt.lower()
    #print p_contact_txt
    if "fax" in p_contact_txt:
        #print "yes.....in p tag"
        #print fxx.split("p_contact_txt")
        #print fx
        regexp = re.compile("fax(.*)")
        fn= regexp.search(p_contact_txt).group(1)
        fax_num = re.findall(r"\+?[ ]?\(?\+?[1-9]{1,4}\)?-?[ ]?\-?\(?[0-9]{1,10}\)?\-?[ ]?[0-9]{3,3}-?\d{0,10}-?[ ]?\d{0,10}", fn)
        fax_num=fax_num[0]
        #print "FAX NUMBER___+_+_+_+_+_+_++_+_+_+_+_+_+_+_+_+__+_+_+_+_+_+_+_+_", fax_num

    tr_contact_txt = tr_contact_txt.lower()
    #print tr_contact_txt
    if "fax" in tr_contact_txt:
        #print "yes.....in tr tag"
        #print fxx.split("tr_contact_txt")
        #print fx
        regexp = re.compile("fax(.*)")
        fn= regexp.search(tr_contact_txt).group(1)
        fax_num = re.findall(r"\+?[ ]?\(?\+?[1-9]{1,4}\)?-?[ ]?\-?\(?[0-9]{1,10}\)?\-?[ ]?[0-9]{3,3}-?\d{0,10}-?[ ]?\d{0,10}", fn)
        fax_num=fax_num[0]
        #print "FAX NUMBER___+_+_+_+_+_+_++_+_+_+_+_+_+_+_+_+__+_+_+_+_+_+_+_+_", fax_num
    #print "FINAL FAX NUMBER: ", fax_num
    return fax_num
########################################################################################################################

def ct_homepg(phone,email,phone1,email1):
    if phone == "Not Found" and phone1 != "Not Found":
        phone2 = phone1[:]
        #print "If 1 of phone"

    if phone != "Not Found" and phone1 == "Not Found":
        phone2 = phone[:]
        #print "If 2 of phone"
    if phone == "Not Found" and phone1 == "Not Found":
        phone2 == "Not Found"
        #print "If 3 of phone"
    if phone != "Not Found" and phone1 != "Not Found":
        phone2 = phone+phone1
        #print "If 4 of phone"


    if email == "Not Found" and email1 != "Not Found":
        email2 = email1[:]
        #print "If 1 of email"
    if email != "Not Found" and email1 == "Not Found":
        email2 = email[:]
        #print "If 2 of email"
    if email == "Not Found" and email1 == "Not Found":
        email2 == "Not Found"
        #print "If 3 of email"
    if email != "Not Found" and email1 != "Not Found":
        email2 = email+email1
        #print "If 4 of email"

    #print "Contact at CONTACT US: PHONE ", phone, " EMAIL: ", email
    #print "Contact at HOMEPAGE: PHONE ", phone1, " EMAIL: ", email1
    #print "Final Contact before deduplication: PHONE ", phone2, " EMAIL: ", email2
    #print "TYPE OF PHONE IS AFTER Not Found PROCESSING::", type(phone)
    # phone =  phone + phone1
    # email = email + email1

    #to remove duplicates:
    # phone=[]
    # for i in phone2:
    #     if i not in phone:
    #         phone.append(i)
    if phone2 != "Not Found":
        [phone.append(i) for i in phone2 if not i in phone]
    if email2 != "Not Found":
        [email.append(i) for i in email2 if not i in email]

def clean_add(contact_text1):
        #Data cleaning for less than 3 words:
        #print "HI"
        contact_text1 = str(contact_text1)
        contact_text1=" . \n".join(contact_text1.split(" || "))
        contact_text1=str(contact_text1).replace("[] ++", " ").replace("+", "").replace("[]","").replace("[","").replace("]","").replace("'","").replace("[","").replace(",","").replace("| |","\n").replace("|","")
        #print contact_text
        txt = contact_text1.rstrip().lstrip().lower() # Remove all extra spaces at the start and at the end of the string
        while "  " in txt: # While  there are 2 spaces beetwen words in our string...
            txt = txt.replace("  ", " ") # ... replace them by one space!
        if txt == "":
            wordCount = 0
        else:
            wordCount = 1
            for letter in txt:
                if letter == " ":
                    wordCount += 1
        #print(wordCount)
        if wordCount < 3:
            #print "Just one word in contact text for this tag"
            if ("tel" in txt) or ("fax" in txt) or ("mob" in txt) or ("phone" in txt) or ("ph" in txt) or ("@" in txt) or ("contact" in txt) or ("location" in txt) or ("add" in txt) or ("reach" in txt):
                #print "YES 1"
                wdf=""
            else:
                #print "NO 1"
                #print "Text to delete: ", txt
                txt=""
            #print txt
        # if wordCount > 100:
        #     print "Lenghty text len > 100: And Deleted: ", txt
        #     txt = "%"
        #contact_text1 = txt
        stop = stopwords.words('english')
        additional_stop_list = ["careers","customers","right","quality","admin","can","you","send","ask","details","enquiry","free","toll","helpdesk","less","more","information","more","additional","issue","complain","select","no","yes","customer","cutomers","orders","carts","cart","order","login","account","footer","faq","read","unfollow","unsubscribe","yes", "follow","products","accessories","menu","catalogue","reach","powered","by","managed","hosted","designed","email", "id", "phone", "no.","news", "online","contact", "!", "chat", "events","locations","||",">","%","[","*", "us", "home", "our", "contacts", "form", "name", "subscribe", "forum", "message", "home", "quick", "about", "]", "mision", "vision", "blog", "rss feeds", "copyright", "all" , "rights", "reserved", "sitemap", "site map", "terms and conditions", "terms", "use","privacy", "policy", "map","site","page", "website","terms of use", "print", "your", "messages", "name", "subject", "enquiry", "required", "(required)", "Comments", "submit", "reset", "review"]
        stop.extend(additional_stop_list)
        contact_text1=" ".join(filter(lambda word: word not in stop, contact_text1.split()))
        #print "stop word completed"
        #print type(contact_text1)
        contact_text1 = contact_text1.replace("||", "\n").replace(". .","")

        #print "__________________"

        #print "22222222222222", contact_text1
        return contact_text1

def add_reg_pin(start, tag,title):
    try:
        check="Not Found"
        add_rule = re.findall(start + r".*[0-9]{5,6}[ ]", tag)
        check=re.findall(r"[0-9]{5,6}[ ]",add_rule)
        #print("11111JSJSDFJSDJFSDJFJSDFJSDFJSD")
        #add_rule=add_rule.group()
        #check=check.group()
        #print "CHECK::::::::::::::::::: ", check

    except Exception, e:
        check="Not Found"
        add_rule="Not Found"
        #print "Exception in ADD_REG_PIN Function: ", e
        logging.error("warning Reason :: %s" % e)
        pass
    #print "Check and add_rule: ", " : ", add_rule
    return check, str(add_rule)


def add_reg_phone(start, tag,title):
    try:
        add_rule = re.findall(start + r".*\+?[ ]?\(?\+?[1-9]{1,4}\)?-?[ ]?\-?\(?[0-9]{1,10}\)?\-?[ ]?[0-9]{3,3}-?\d{0,10}-?[ ]?\d{0,10}", tag)
        #print "IN ADD_REG_PHONE FUNCTION: REGX O/P: ", add_rule
        #check=re.search(r"[0-9]{5,6}[ ]",add_rule)
        #add_rule=add_rule.group()
        #check=check.group()
        #print "CHECK::::::::::::::::::: ", check
        check = "Not Found"

        #to find just one address:
        phone_add = re.findall(r"\+?[ ]?\(?\+?[1-9]{1,4}\)?-?[ ]?\-?\(?[0-9]{1,10}\)?\-?[ ]?[0-9]{3,3}-?\d{0,10}-?[ ]?\d{0,10}", str(add_rule))
        #print "PHONE IN ADDRESSSSSSS:::::::::: ", phone_add
        if phone_add !=[]:
            #print "FOUND PHONE IN ADDRESS "

            phone = []
            for e in phone_add:
                t = e
                t = t.strip().rstrip().lstrip().replace("+","").replace("'","").replace("-","").replace(" ","").replace("(","").replace(")","").replace(".","")

                #print t, "LEN: ",len(t)
                if t.isdigit() == 1:
                    if e[-1] != "-":
                        phone.append(e)
            #print phone

            phone_add = phone[0]
            #print "Terminating till Phone number :",phone_add
            try:

                add_rule_pt = str(add_rule).partition(phone_add)
                add_rule = add_rule_pt[0]+" "+add_rule_pt[1]
                #print "-----ADDRESS BEFORE FIRST PHONE:----- ", add_rule
                other_add = add_rule_pt[2]
                #print "-----OTHER ADDRESS TEXT:----- ", other_add ,"\n"

                if title in add_rule:
                    #print "YESSSSSSS TITLE IS PRESENT AND FETCHED IN ADDRESS: "
                    add_rule = str(add_rule).partition(title)
                    add_rule=add_rule[1]+" "+add_rule[2]
                    #print add_rule
            except Exception, e:
                logging.error("warning Reason :: %s" % e)
                #print e
                add_rule=add_rule[:]

    except Exception, e:
        #check="Not Found"
        add_rule="Not Found"
        #print "Exception in ADD_REG_PIN Function: ", e
        logging.error("warning Reason :: %s" % e)
        pass
    #print "Final Address from Check and add_rule,from RULES :\n: ", str(add_rule), "\n: "
    return check, str(add_rule)


## Function for handling address::
def handling_all_add(checka, add_rulea, checkb, add_ruleb, checkc, add_rulec, checkd, add_ruled):
    try:
        address = str(add_rulea) + " ++ " + str(add_ruleb) + " ++ " + str(add_rulec) + " ++ " + str(add_ruled)
    except Exception, e:
        #print "EXCEPTION IN CHECKING FOR SAME ADDRESSES IN ALL TAGS: ", e
        address = "Not Found"

    #print "ADDRESS: ","|"+address+"|"
    if address=="[]":
        address="Not Found"
    return address