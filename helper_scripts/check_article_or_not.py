# Functions and variable to check urls whether they represent an article or someother kind of website

# Requrired libraries
import re
from types import resolve_bases
import requests
from bs4 import BeautifulSoup

# Function to check whether given url is for an article
def is_article_url(url):
    respose=requests.get(url)
    soup=BeautifulSoup(respose.text,features="html.parser")
    # Seacrching for meta tag with property content=article 
    # required tag for article url: <meta content="article" property="og:type"/>
    result=soup.find_all("meta",{'content':"article"})
    result.append(soup.find_all())
    return len(result)>0

# Function travers over all links mentioned in tweeet and return article url
def find_article_urls_from_mentioned_urls(mentioned_urls):
    article_urls=[]
    for url in mentioned_urls:
        if is_article_url(url):
            article_urls.append(url)

    return article_urls