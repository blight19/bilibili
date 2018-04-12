#! /usr/bin/env python
#coding=utf-8
import requests
import json
def get_replies(av):
    url = 'https://api.bilibili.com/x/v2/reply?pn=1&type=1&oid='+av
    res = requests.get(url)
    page_num = json.loads(res.text)['data']['page']['count']
    for page in range(1,int(int(page_num)/20)+2):
        url = 'https://api.bilibili.com/x/v2/reply?pn='+str(page)+'&type=1&oid='+av
        print(url)
        res = requests.get(url)        
        a=json.loads(res.text)
        try:
            for i in range(19):
                try:
                    print( a['data']['replies'][i]['content']['message'])
                except UnicodeEncodeError as e:
                    pass
        except IndexError:
            pass
#get_replies('21149278')
def get_list():   
    url = 'https://api.bilibili.com/x/web-interface/newlist?callback=jqueryCallback_bili_10&rid=17&type=0&pn=1&ps=20&_=1523540531903'
    headers = {
        'Referer':'https://www.bilibili.com',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'    
        }
    res = requests.get(url,headers=headers)
    data = json.loads(res.text)['data']
    print(data['archives'][0]['title'],end='----av:')
    print(data['archives'][0]['aid'])
#get_list()
