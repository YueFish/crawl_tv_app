#coding=utf-8
import requests
import json
import os
from bs4 import BeautifulSoup

SOURCE_HTML = "http://app.shafa.com/archives/{}.html"
SAVE_File = "./data/app_list_save.csv"
PAGE_NUM = 24

def get_app_list():
    # if not os.path.exists(SAVE_File):
    #     os.mkdir("./data")
    with open(SAVE_File,'w',encoding='utf-8') as f:
        for page_id in range(1,PAGE_NUM+1):
            whole_url = SOURCE_HTML.format(page_id)
            response = requests.get(whole_url)
            soup = BeautifulSoup(response.text, 'lxml')
            tag_list = soup.select('div.col-sm-6')
            item_json ={}
            for item in tag_list:
                href = item.a['href'].strip().split("=")[0]
                name_category = item.a.string.strip().split(" ")
                category = name_category[0][1:-1]
                name = name_category[1]
                item_json['href'] = href
                item_json['name'] = name
                item_json['category'] = category
                f.write(json.dumps(item_json)+"\n")
                # print(name+"---"+href+"---"+category)
            f.flush()
    


if __name__ == '__main__':
    get_app_list()
    