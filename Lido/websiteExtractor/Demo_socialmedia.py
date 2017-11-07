# -*- coding: utf-8 -*-
import re
import nltk
from bs4 import BeautifulSoup
import logging

format = '%(name)s : %(filename)s : %(asctime)s : %(lineno)s : %(levelname)s : %(message)s'
logging.basicConfig(format=format,filename="Lido.log", level=logging.DEBUG)

facebook_link=re.compile('https?\:\/\/+[w\.]*facebook.com/[a-zA-Z0-9/]*')
youtube_link=re.compile('https?\:\/\/+[w\.]*youtube.com/[a-zA-Z0-9/]*')
linkedin_link=re.compile('https?\:\/\/+[a-z\.]*linkedin.com/[a-zA-Z0-9/]*')
twitter_link=re.compile('https?\:\/\/+[w\.]*twitter.com/[a-zA-Z0-9/]*')
pinterest_link=re.compile('https?\:\/\/+[w\.]*pinterest.com/[a-zA-Z0-9/]*')
gplus_link=re.compile('https?\:\/\/+[w\.]*plus.google.com/[a-zA-Z0-9/]*')
intsagram_link=re.compile('https?\:\/\/+[w\.]*intsagram.com/[a-zA-Z0-9/]*')
flickr_link=re.compile('https?\:\/\/+[w\.]*flickr.com/[a-zA-Z0-9/]*')

def socialmedia(page,links):
            company_fb="Not Found"
            company_yt="Not Found"
            company_lin="Not Found"
            company_pi="Not Found"
            company_tw="Not Found"
            company_gp="Not Found"
            company_in="Not Found"
            company_fl="Not Found"
            soup = BeautifulSoup(page,'lxml')

            soup1=str(soup)
            #print soup1
            #print type(soup1)

            links= soup.find_all("a")
            for a in links:
                try:
                    #print "ALL"
                    #print a
                    links_href=a['href']
                    #print links_href
                    matched1 = facebook_link.search(links_href)
                    matched2 = youtube_link.search(links_href)
                    matched3 = linkedin_link.search(links_href)
                    matched4 = twitter_link.search(links_href)
                    matched5 = pinterest_link.search(links_href)
                    matched6 = gplus_link.search(links_href)
                    matched7 = intsagram_link.search(links_href)
                    matched8= flickr_link.search(links_href)

                    try:
                        if matched1:
                            #print "Found the URL:",matched1,a['href']
                            company_fb=links_href
                    except Exception,e:
                        logging.error("Error Reason :: %s" % e)
                        pass
                    try:
                        if matched2:
                            #print "Found the URL:",matched2,a['href']
                            company_yt=links_href
                    except Exception,e:
                        logging.error("Error Reason :: %s" % e)
                        pass
                    try:
                        if matched3:
                            #print "Found the URL:",matched3,a['href']
                            company_lin=links_href
                    except Exception,e:
                        logging.error("Error Reason :: %s" % e)
                        pass
                    try:
                        if matched4:
                            #print "Found the URL:",matched4,a['href']
                            company_tw=links_href
                            #print type(company_tw)
                    except Exception,e:
                        logging.error("Error Reason :: %s" % e)
                        pass
                    try:
                        if matched5:
                           # print "Found the URL:",matched5,a['href']
                            company_pi=links_href
                    except Exception,e:
                        logging.error("Error Reason :: %s" % e)
                        pass
                    try:
                        if matched6:
                            #print "Found the URL:",matched6,a['href']
                            company_gp=links_href
                    except Exception, e:
                        logging.error("Error Reason :: %s" % e)
                        pass
                    try:
                        if matched7:
                            #print "Found the URL:",matched7,a['href']
                            company_in=links_href
                    except Exception,e:
                        logging.error("Error Reason :: %s" % e)
                        pass
                    try:
                        if matched8:
                            #print "Found the URL:",matched8,a['href']
                            company_fl=links_href
                    except Exception, e:
                        logging.error("Error Reason :: %s" % e)
                        pass
                except Exception,e:
                    logging.error("Error Reason :: %s" % e)
                    continue

            if company_fb=="Not Found":
                try:
                    company_fb=re.search("(?P<url>https?\:\/\/+[w\.]*facebook.com/[a-zA-Z0-9/]*)", soup1).group("url")
                    #print company_fb
                except Exception,e:
                    logging.error("Error Reason :: %s" % e)
                    #print "Welcome Exception Facebook"
                    pass
            if company_yt=="Not Found":
                try:
                    company_yt=re.search("(?P<url>https?\:\/\/+[w\.]*youtube.com/[a-zA-Z0-9/]*)", soup1).group("url")
                    #print company_yt
                except Exception, e:
                    logging.error("Error Reason :: %s" % e)
                    #print "Welcome Exception Youtube"
                    pass
            if company_lin=="Not Found":
                try:
                    company_lin=re.search("(?P<url>https?\:\/\/+[a-z\.]*linkedin.com/[a-zA-Z0-9/]*)", soup1).group("url")
                    #print company_lin
                except Exception, e:
                    logging.error("Error Reason :: %s" % e)
                    #print "Welcome Exception Linkedin"
                    pass
            if company_tw=="Not Found":
                try:
                    company_tw=re.search("(?P<url>https?\:\/\/+[w\.]*twitter.com/[a-zA-Z0-9/]*)", soup1).group("url")
                    #print company_tw
                except Exception, e:
                    logging.error("Error Reason :: %s" % e)
                    #print "Welcome Exception Twitter"
                    pass
            if company_pi=="Not Found":
                try:
                    company_pi=re.search("(?P<url>https?\:\/\/+[w\.]*pinterest.com/[a-zA-Z0-9/]*)", soup1).group("url")
                    #print company_pi
                except Exception, e:
                    logging.error("Error Reason :: %s" % e)
                    #print "Welcome Exception Pinterest"
                    pass
            if company_gp=="Not Found":
                try:
                    #print "hello1"
                    company_gp=re.search("(?P<url>https?\:\/\/+[w\.]*plus.google.com/[a-zA-Z0-9/+]*)", soup1).group("url")
                    #print company_gp
                except Exception, e:
                    logging.error("Error Reason :: %s" % e)
                    #print "Welcome Exception GooglePlus"
                    pass
            if company_in=="Not Found":
                try:
                    #print "hello1"
                    company_in=re.search("(?P<url>https?\:\/\/+[w\.]*instagram.com/[a-zA-Z0-9/+]*)", soup1).group("url")
                    #print company_in
                except Exception, e:
                    logging.error("Error Reason :: %s" % e)
                    #print "Welcome Exception intsagram"
                    pass

            if company_fl=="Not Found":
                try:
                    #print "hello1"
                    company_fl=re.search("(?P<url>https?\:\/\/+[w\.]*Flickr.com/[a-zA-Z0-9/+]*)", soup1).group("url")
                    #print company_fl
                except Exception, e:
                    #print "Welcome Exception Flickr"
                    logging.error("Error Reason :: %s" % e)

                    pass
            #print "DONE"
            return company_fb, company_yt, company_lin, company_tw, company_pi, company_gp, company_in, company_fl