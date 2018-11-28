import time
import requests
from pyquery import PyQuery as pq
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}

def restaurant(url):
    # 获取网页静态源代码
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
    except Exception:
        return None

name=[]
url = [] 
star = []
comment = []
avg_price = []
taste = []
environment = []
services = []
recommend = []

num = {'hs-OEEp': 0, 'hs-4Enz': 2, 'hs-GOYR': 3, 'hs-61V1': 4, 'hs-SzzZ': 5, 'hs-VYVW': 6, 'hs-tQlR': 7, 'hs-LNui': 8, 'hs-42CK': 9}
def detail_number(htm):
    try:
        a = str(htm)
        a = a.replace('1<', '<span class="1"/><')
        a = a.replace('.', '<span class="."/>')
        b = pq(a)
        cn = b('span').items()
        number = ''
        for i in cn:
            attr = i.attr('class')
            if attr in num:
                attr = num[attr]
            number = number + str(attr)
        number = number.replace('None', '')
    except:
        number = ''
    return number

def info_restaurant(html):
    # 获取饭店的名称和链接
    doc = pq(html)
    for i in range(1,16):
        #获取饭店名称
        shop_name = doc('#shop-all-list > ul > li:nth-child('+str(i)+') > div.txt > div.tit > a:nth-child(1) > h4').text()
        if shop_name == '':
            break
        name.append(shop_name)
        #获取饭店链接
        url.append(doc('#shop-all-list > ul > li:nth-child('+str(i)+') > div.pic > a').attr('href'))
        try:
            star.append(doc('#shop-all-list > ul > li:nth-child('+str(i)+') > div.txt > div.comment > span').attr('title'))
        except:
            star.append("")
        #获取评论数量
        comment_html = doc('#shop-all-list > ul > li:nth-child('+str(i)+') > div.txt > div.comment > a.review-num > b')
        comment.append(detail_number(comment_html))
        #获取人均消费
        avg_price_html = doc('#shop-all-list > ul > li:nth-child('+str(i)+') > div.txt > div.comment > a.mean-price > b')
        avg_price.append(detail_number(avg_price_html))
        #获取口味评分
        taste_html = doc('#shop-all-list > ul > li:nth-child('+str(i)+') > div.txt > span > span:nth-child(1) > b')
        taste.append(detail_number(taste_html))
        #获取环境评分
        environment_html = doc('#shop-all-list > ul > li:nth-child('+str(i)+') > div.txt > span > span:nth-child(2) > b')
        environment.append(detail_number(environment_html))
        #获取服务评分
        services_html = doc('#shop-all-list > ul > li:nth-child('+str(i)+') > div.txt > span > span:nth-child(3) > b')
        services.append(detail_number(services_html))
        #推荐菜,都是显示三道菜
        try:
            recommend.append(doc('#shop-all-list > ul > li:nth-child('+str(i)+') > div.txt > div.recommend > a:nth-child(2)').text()+str(',')+\
                            doc('#shop-all-list > ul > li:nth-child('+str(i)+') > div.txt > div.recommend > a:nth-child(3)').text()+str(',')+\
                            doc('#shop-all-list > ul > li:nth-child('+str(i)+') > div.txt > div.recommend > a:nth-child(4)').text())
        except:
            recommend.append("")
for i in range(1,51):
    print('正在获取第{}页饭店信息'.format(i))
    hotpot_url = 'http://www.dianping.com/chengdu/ch10/g110p'+str(i)+'?aid=93195650%2C68215270%2C22353218%2C98432390%2C107724883&cpt=93195650%2C68215270%2C22353218%2C98432390%2C107724883&tc=3'
    html = restaurant(hotpot_url)
    info_restaurant(html)
    print ('第{}页获取成功'.format(i))
    time.sleep(12)

shop = {'name': name, 'url': url, 'star': star, 'comment': comment, 'avg_price': avg_price, 'taste': taste, 'environment': environment, 'services': services, 'recommend': recommend}
shop = pd.DataFrame(shop, columns=['name', 'url', 'star', 'comment', 'avg_price','taste', 'environment', 'services', 'recommend'])
shop.to_csv("shop.csv",encoding="utf_8_sig",index = False)
