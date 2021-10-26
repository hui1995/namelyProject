import requests
from lxml import etree
from books.models import Category, Book
from datetime import datetime
import time
import uuid
import requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
}
import jieba.analyse

jieba.analyse.set_stop_words('stop_words')


def start_spider():
    url = "https://book.douban.com/tag/?view=type&icn=index-sorttags-all"

    payload = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    # xpath解析

    # 建立html的树
    tree = etree.HTML(response.text)
    data = tree.xpath('//div[@class="article"]')[0]
    data = data.xpath("./div/div")
    url_head = "https://book.douban.com"
    for i in data:
        urllist = i.xpath("./table/tbody/tr/td/a/@href")
        if len(urllist)>2:
            urllist=urllist[:2]
        category=i.xpath("./a/@name")[0].strip()
        category=Category.objects.filter(name=category).first()
        if category is None:
            continue
        for x in urllist:
            book_list_url = url_head + x
            print(book_list_url)
            content = requests.get(book_list_url, headers=headers)
            book_etree = etree.HTML(content.text)
            # resolve_book_list(book_etree,category)


def resolve_book_list(etreeinfo,category):
    booklist = etreeinfo.xpath('//ul[@class="subject-list"]/li')
    for i in booklist:
        data = {}
        img = i.xpath('./div[@class="pic"]/a/img/@src')[0]
        info = i.xpath('./div[@class="info"]')[0]
        title = info.xpath("./h2/a/@title")[0]
        href = info.xpath("./h2/a/@href")[0]
        book=Book.objects.filter(href=href).first()
        # 基础数据入库使用
        if book is not None:
            continue
        response = requests.get(img)
        name = str(uuid.uuid4()) + ".jpg"
        with open("./static/image/"+name, "wb") as f:
            f.write(response.content)

        detail = info.xpath('./div[@class="pub"]/text()')[0]
        time.sleep(1)
        bookdetail = requests.get(href, headers=headers)
        data["img"] = "static/image/"+name
        data["title"] = title
        data["detail"] = detail
        data["href"] = href
        book_etree = etree.HTML(bookdetail.text)
        try:
            resolve_book_detail(book_etree, href.split("/")[-2], data,category)
        except:
            continue



import json


def resolve_book_detail(etreeinfo, id, data,category):
    star = etreeinfo.xpath('//strong[@class="ll rating_num "]/text()')[0]
    content = etreeinfo.xpath('//div[@class="intro"]/p/text()')
    commentsStr = ""
    data['content'] = json.dumps(content)
    data['star'] = star
    for i in range(10):
        time.sleep(1)
        url = "https://book.douban.com/subject/{}/comments/?start={}&limit=20&status=P&sort=new_score".format(id,
                                                                                                              i * 20)
        comments = requests.get(url, headers=headers)
        comments_etree = etree.HTML(comments.text)
        comments_list = comments_etree.xpath('//span[@class="short"]/text()')
        for x in comments_list:
            commentsStr += x
            commentsStr += ","

    tags = jieba.analyse.extract_tags(commentsStr, topK=10, withWeight=True)
    data["tags"] = json.dumps([ x[0] for x in tags])
    book = Book.objects.filter(href=data["href"]).first()
    if book is not None:
        book.content = data['content']
        book.star = data['star']
        book.title = data['title']
        book.detail = data['detail']
        book.create_time = datetime.now()
        book.tags=data['tags']
        book.save()
    else:
        Book.objects.create(pic=data['img'], content=data['content'], star=data['star'], title=data['title'],
                            detail=data['detail'], create_time=datetime.now(), href=data['href'],category=category,tags=data['tags'])


