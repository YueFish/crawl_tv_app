#coding=utf-8
import requests
import json
import os
from bs4 import BeautifulSoup

def get_app_list_data():
    f = open("./data/app_list_save.csv",'r')
    fw = open("./data/app_info.csv",'w')
    item_json = {}
    num = 0
    for line in f.readlines():
        item_json = json.loads(line)
        href = item_json['href']
        name = item_json['name']
        category = item_json['category']
        data_json = parse_page(href)
        data_json.update(item_json)
        # print(json.dumps(data_json))
        fw.write(json.dumps(data_json) + "\n")
        fw.flush()
    f.close()
    fw.close()

def parse_page(url):
    res_json = {}
    response = requests.get(url)
    
    soup = BeautifulSoup(response.text, 'lxml')

    #获取tags
    tags = soup.select("body > div.container > div:nth-child(3) > div > section > div.view-header-middle > div.view-header-tags > ul > li")
    tags_clean = []
    for tag in tags:
        tags_clean.append(tag.span.string)
    res_json["tags"] = tags_clean

    
    #ratingoptions
    ratings = soup.select("body > div.container > div:nth-child(3) > div > section > div.view-header-middle > div.view-header-rating > span:nth-child(1) >span")
    score = 0
    for rating in ratings:
        tag_class = rating.attrs
        if tag_class:
            if 'hit' in tag_class['class']:
                score += 1
    res_json["rating"] = score 

    #options
    options = soup.select("body > div.container > div:nth-child(3) > div > section > div.view-header-middle > div.view-header-rating > span:nth-child(3)")
    option = ''
    for option_span in options:
        option+=option_span.string.strip()
    res_json["option"] = option

    #download 
    download_times = soup.select("body > div.container > div:nth-child(4) > div > section > ul > li:nth-child(3) > span")
    times = ''
    for time_span in download_times:
        if  time_span.string:
            times = time_span.string.strip()
    res_json["download_times"] = times

    #language
    languages = soup.select("body > div.container > div:nth-child(4) > div > section > ul > li:nth-child(4) > span")
    language = ''
    for language_span in languages:
        if language_span.string:
            language = language_span.string.strip()
    res_json["language"] = language
    # print(language)

    #brief
    briefs =soup.select("body > div.container > div:nth-child(6) > div > section > p")
    brief=''
    for brief_p in briefs[:-1]:
        brief_p = brief_p.string.strip()
        brief += brief_p 
    res_json["brief"] = brief


    return res_json

if __name__ == '__main__':
    get_app_list_data()
    # parse_page("http://app.shafa.com/apk/yunshitinghudianjing.html")
    # parse_page("http://app.shafa.com/apk/sanlingzhinengkongdiaoTVban.html")
