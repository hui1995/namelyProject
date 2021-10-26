import  requests
from lxml import etree
from spider.dbUtils import Db
import random
import time
def spider():
    db = Db("dongcheng")
    page=1
    while True:
        time.sleep(random.randint(1,3))

        res=requests.get("https://bj.lianjia.com/ershoufang/dongcheng/pg{}/".format(page))
        page+=1
        tree = etree.HTML(res.text)
        hotellist=tree.xpath('//ul[@class="sellListContent"]/li/div[@class="info clear"]')
        if len(hotellist)<=0:
            break
        data=[]


        for i in hotellist:
            info=[]
            title=i.xpath('./div[@class="title"]/a/text()')[0]
            info.append(title)
            floodList=i.xpath('./div[@class="flood"]/div/a/text()')
            address=i.xpath('./div[@class="address"]/div/text()')[0]
            # info.append(address)
            flood=""
            for x in floodList:
                flood=flood+x
                flood=flood+'-'
            flood=flood[:-1]
            info.append(flood)
            address=address.split("|")
            try:
                info.append(address[4])

                info.append(address[5])
                info.append(address[1][:-3])
                info.append(address[2])
                info.append(address[0])
                total_price=i.xpath('./div[@class="priceInfo"]/div[@class="totalPrice"]/span/text()')[0]
                unit_price=i.xpath('./div[@class="priceInfo"]/div[@class="unitPrice"]/@data-price')[0]
                info.append(total_price)
                info.append(unit_price)
                data.append(info)
            except:
                continue
        db.insert(data)
    db.close()

# sellListContent