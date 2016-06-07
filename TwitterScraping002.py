from selenium import webdriver
from bs4 import BeautifulSoup
import time
import urllib
import calendar
import argparse
import datetime

def dformat(date):
    return str(date.year) + "-" + str(date.month) + "-" + str(date.day)

def sformat(date):
    return str(date.day) + " " + calendar.month_abbr[date.month] + " " + str(date.year)

def TWscraping(word, date, interval):
    date = datetime.datetime.strptime(date,"%Y-%m-%d")
    url = urllib.quote(str(word) + " since:" + dformat(date - datetime.timedelta(days=1)) + " until:" + dformat(date + datetime.timedelta(days=2)))
    browser = webdriver.Firefox()
    browser.get("https://twitter.com/search?q=" + url)
    
    count = 0;
    counttemp = 1;
    
    while(count < counttemp):
        count = counttemp
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(interval)
        html = browser.page_source.encode('utf-8')
        soup = BeautifulSoup(html, "lxml")
        result = soup.find_all("p", class_="TweetTextSize js-tweet-text tweet-text")
        result1 = soup.find_all("a",class_="tweet-timestamp js-permalink js-nav js-tooltip")
        counttemp = len(result)
    
    f = open("output_"+ str(datetime.datetime.today()) +".txt","w")
    for (e1, e2) in zip(result, result1):
        if sformat(date) == e2.text:
            f.write(e1.text.replace("\n"," ").encode('utf-8'))
            f.write("\n")
    
    f.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search and Scraping Twitter Data!")
    parser.add_argument("word", help=u"Search key word")
    parser.add_argument("date",help="example: 2015-8-12")
    parser.add_argument("-i", dest="interval", default=2, help=u"Update interval: Short if it fails do not cry.")
    args = parser.parse_args()
    
    TWscraping(args.word, args.date, args.interval)

