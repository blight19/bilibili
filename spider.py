#! /usr/bin/env python
#coding=utf-8
import requests
import json
from SV_Mongo import sv_mongo
import chip.relogin
from multiprocessing import Process,cpu_count
'''
获取B站游戏分类所有视频评论并保存至Mongodb中
'''
sv = sv_mongo('bilibili','replies')

def request(url):
    headers = {
        'Referer':'https://www.bilibili.com',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'    
        }    
    res = requests.get(url,headers=headers)
    if res.status_code==200:
        return res
    else:
        print('更换ip中...')
        chip.relogin.main()
        return request(url)
def get_replies(av):
    #有的禁止评论会出错，如av:22078206,所以先获取评论数
    url = 'https://api.bilibili.com/x/v2/reply?pn=1&type=1&oid='+av
    res = request(url)
    try:
        page_num = json.loads(res.text)['data']['page']['count']
    except KeyError:
        page_num=0
        print('获取评论数失败'+url)
        return None
    for page in range(1,int(int(page_num)/20)+2):
        url = 'https://api.bilibili.com/x/v2/reply?pn='+str(page)+'&type=1&oid='+av
        print(url)
        res = requests.get(url)        
        a=json.loads(res.text)
        try:
            for i in range(0,20):
                try:
                    yield  a['data']['replies'][i]['content']['message']
                except UnicodeEncodeError as e:
                    pass
        except IndexError:
            pass
#get_replies('21149278')

#request('https://api.bilibili.com/x/v2/reply?pn=1&type=1&oid=21149278')    
def get_list(pn):   
    url = 'https://api.bilibili.com/x/web-interface/newlist?callback=jqueryCallback_bili_10&rid=17&type=0&pn='+str(pn)+'&ps=20&_=1523540531903'
    res = request(url)
    data = json.loads(res.text)['data']
    for i in range(0,20):
        title = data['archives'][i]['title']
        aid = data['archives'][i]['aid']
        yield {'title':title,'aid':aid}
def main():
    
    for pn in range(1,20):
        datas = get_list(pn)
        for data in datas:
        
            replies = get_replies(str(data['aid']))
            for replie in replies:
                
                sv.push_content(data['aid'],data['title'],replie)
            

if __name__ == '__main__':
    main()
