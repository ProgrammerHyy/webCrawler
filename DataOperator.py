# 连接数据库以及数据库的操作
import mysql.connector


class DataOperator:
    __config = {}   # 连接数据库用的参数
    __mydb = None
    __mydb_cursor = None

    def __init__(self, host, username, password, database):
        self.__config['host'] = host
        self.__config['user'] = username
        self.__config['password'] = password
        self.__config['database'] = database
        self.__config['port'] = 3306

    def connect(self):  # 连接数据库，返回成功或失败
        try:
            self.__mydb = mysql.connector.connect(**self.__config)
        except Exception as e:
            e.with_traceback()
            print("Unable to connect to the database!")
            return False
        self.__mydb_cursor = self.__mydb.cursor()
        return True

    def insertIntoDatabase(self, **data):  # 插入数据操作，返回成功或失败
        sql = "insert into game values (%s,%s,%s,%s,%s)"
        val = (int(data['Gno']), str(data['Gname']), float(data['score']), str(data['tag']), int(data['playercount']))
        try:
            self.__mydb_cursor.execute(sql, val)
            self.__mydb.commit()
        except Exception as e:
            e.with_traceback()
            print(val)
            print("Unable to insert data!")
            return False
        return True

    def selectData(self):   # 获取数据的生成器，按照玩家数量，从大到小排序，选取前5000条数据
        sql = "select * from game order by playerCount DESC limit 5000"
        self.__mydb_cursor.execute(sql)
        res = self.__mydb_cursor.fetchall()
        for elem in res:
            yield elem  # 作为生成器返回数据

    def selectSpData(self, tag):     # 按照tag获取数据的生成器，按照玩家数量从大到小排序，选取前1000条数据
        sql = "select * from game where locate(%s,tag)>1 order by playerCount Desc limit 1000"
        val = (str(tag),)
        try:
            self.__mydb_cursor.execute(sql,val)
            res = self.__mydb_cursor.fetchall()
        except Exception as e:
            print('Unable to get data')
        for elem in res:
            yield elem

    # 关闭连接
    def closeConnection(self):
        try:
            self.__mydb.close
        except Exception as e:
            print("Unable to close connection!")
            return False
        return True

