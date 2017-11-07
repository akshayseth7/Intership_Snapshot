# -*- coding: utf-8 -*-
import re
import nltk
from bs4 import BeautifulSoup

facebook_link=re.compile('https?\:\/\/+[w\.]*facebook.com/[a-zA-Z0-9/]*')
youtube_link=re.compile('https?\:\/\/+[w\.]*youtube.com/[a-zA-Z0-9/]*')
linkedin_link=re.compile('https?\:\/\/+[a-z\.]*linkedin.com/[a-zA-Z0-9/]*')
twitter_link=re.compile('https?\:\/\/+[w\.]*twitter.com/[a-zA-Z0-9/]*')
pinterest_link=re.compile('https?\:\/\/+[w\.]*pinterest.com/[a-zA-Z0-9/]*')
gplus_link=re.compile('https?\:\/\/+[w\.]*plus.google.com/[a-zA-Z0-9/]*')

def socialmedia(page,links):
            company_fb="no link found"
            company_yt="no link found"
            company_lin="no link found"
            company_pi="no link found"
            company_tw="no link found"
            company_gp="no link found"
            soup = BeautifulSoup(page,'lxml')

            soup1=str(soup)
            ##print soup1
            #print type(soup1)

            links= soup.find_all("a")
            for a in links:
                try:
                    ##print "ALL"
                    ##print a
                    links_href=a['href']
                    ##print links_href
                    matched1 = facebook_link.search(links_href)
                    matched2 = youtube_link.search(links_href)
                    matched3 = linkedin_link.search(links_href)
                    matched4 = twitter_link.search(links_href)
                    matched5 = pinterest_link.search(links_href)
                    matched6 = gplus_link.search(links_href)
                    if matched1:
                        #print "Found the URL:",matched1,a['href']
                        company_fb=links_href
                    if matched2:
                        #print "Found the URL:",matched2,a['href']
                        company_yt=links_href
                    if matched3:
                        #print "Found the URL:",matched3,a['href']
                        company_lin=links_href
                    if matched4:
                        #print "Found the URL:",matched4,a['href']
                        company_tw=links_href
                        #print type(company_tw)
                    if matched5:
                        #print "Found the URL:",matched5,a['href']
                        company_pi=links_href
                    if matched6:
                        #print "Found the URL:",matched5,a['href']
                        company_gp=links_href
                except Exception:
                    continue

            if company_fb=="no link found":
                try:
                    company_fb=re.search("(?P<url>https?\:\/\/+[w\.]*facebook.com/[a-zA-Z0-9/]*)", soup1).group("url")
                    #print company_fb
                except Exception:
                    #print "Welcome Exception Facebook"
                    pass
            if company_yt=="no link found":
                try:
                    company_yt=re.search("(?P<url>https?\:\/\/+[w\.]*youtube.com/[a-zA-Z0-9/]*)", soup1).group("url")
                    #print company_yt
                except Exception:
                    #print "Welcome Exception Youtube"
                    pass
            if company_lin=="no link found":
                try:
                    company_lin=re.search("(?P<url>https?\:\/\/+[a-z\.]*linkedin.com/[a-zA-Z0-9/]*)", soup1).group("url")
                    #print company_lin
                except Exception:
                    #print "Welcome Exception Linkedin"
                    pass
            if company_tw=="no link found":
                try:
                    company_tw=re.search("(?P<url>https?\:\/\/+[w\.]*twitter.com/[a-zA-Z0-9/]*)", soup1).group("url")
                    #print company_tw
                except Exception:
                    #print "Welcome Exception Twitter"
                    pass
            if company_pi=="no link found":
                try:
                    company_pi=re.search("(?P<url>https?\:\/\/+[w\.]*pinterest.com/[a-zA-Z0-9/]*)", soup1).group("url")
                    #print company_pi
                except Exception:
                    #print "Welcome Exception Pinterest"
                    pass
            if company_gp=="no link found":
                try:
                    #print "hello1"
                    company_gp=re.search("(?P<url>https?\:\/\/+[w\.]*plus.google.com/[a-zA-Z0-9/+]*)", soup1).group("url")
                    #print company_gp
                except Exception:
                    #print "Welcome Exception GooglePlus"
                    pass

            #print "DONE"
            return company_fb,company_yt,company_lin,company_tw,company_pi,company_gp