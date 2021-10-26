
import pymysql
class Db():
    def __init__(self,table_name):
        # spider@121.199.29.111
        self.conn = pymysql.connect(host="121.199.29.111", user ="root", password ="201212", database ="spider", charset ="utf8")

        self.cursor = self.conn.cursor()
        self.table_name=table_name
        self.clear(table_name)


    def clear(self,table_name):
        sql="delete from {}".format(table_name)
        self.cursor.execute(sql)
        self.conn.commit()

    def insert(self,info):
        # 得到一个可以执行SQL语句的光标对象
        # 定义要执行的SQL语句
        sql = """
        insert into {}(`title`,`address`,`floor`,`year`,`area`,`direation`,`type`,`total_price`,`single_price`) 
        values (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """.format(self.table_name)
        # 执行SQL语句
        self.cursor.executemany(sql,info)
        self.conn.commit()
    def close(self):
        # 关闭光标对象
        self.cursor.close()
        # 关闭数据库连接
        self.conn.close()