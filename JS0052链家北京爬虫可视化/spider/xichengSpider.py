import  requests
from lxml import etree
from spider.dbUtils import Db
import random
import time
def spider():
    # 数据库名称，url链接拼接
    spider_area="xicheng"
    # 连接数据库
    db = Db(spider_area)
    # 页数
    page=1
    while True:
        time.sleep(random.randint(1,3))


        # 请求某一页得数据
        res=requests.get("https://bj.lianjia.com/ershoufang/{}/pg{}/".format(spider_area,page))
        page+=1
        # 转换html数据方便xpath解析
        tree = etree.HTML(res.text)
        # 解析出来列表为li
        hotellist=tree.xpath('//ul[@class="sellListContent"]/li/div[@class="info clear"]')
        # 如果没有解析道，说明没有数据了，则跳出循环
        if len(hotellist)<=0:
            break
        data=[]
        # 循环获取到的li标签
        for i in hotellist:
            info=[]
            # 根据相关页面结构解析相关信息
            title=i.xpath('./div[@class="title"]/a/text()')[0]
            info.append(title)
            floodList=i.xpath('./div[@class="flood"]/div/a/text()')
            address=i.xpath('./div[@class="address"]/div/text()')[0]
            # info.append(address)
            flood=""
            # 位置有俩标签所决定，解析出来时一个数组，拼接一下
            for x in floodList:
                flood=flood+x
                flood=flood+'-'
            flood=flood[:-1]
            info.append(flood)
            # 其他一些信息时同一个标签下，用|分割，解析后，分割一下数据，然后进行下方得操作
            address=address.split("|")
            #为了防止数据不完整性导致取值出错导致程序异常结束，所以抛出一下异常
            try:
                info.append(address[4])

                info.append(address[5])
                info.append(address[1][:-3])
                info.append(address[2])
                info.append(address[0])
                # 解析总价和单价
                total_price=i.xpath('./div[@class="priceInfo"]/div[@class="totalPrice"]/span/text()')[0]
                unit_price=i.xpath('./div[@class="priceInfo"]/div[@class="unitPrice"]/@data-price')[0]
                info.append(total_price)
                info.append(unit_price)
                data.append(info)
            except:
                continue
        # 插入数据库
        db.insert(data)
    #关闭数据库
    db.close()

# sellListContent