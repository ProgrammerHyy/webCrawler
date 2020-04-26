from queue import Queue
import threading
import time
from Crawler import Crawler
from DataOperator import DataOperator

# 定义全局变量
lock = threading.Lock()
gameNo = 0

dataQueue = Queue(maxsize=5000)


# 爬取网页线程代理函数
def crawlerFunc():
    print('Crawl thread start!')
    foreurl = 'http://www.taptap.com/app/'
    crawler = Crawler(foreurl)
    while True:
        global gameNo
        with lock:
            num = gameNo
            gameNo += 1
        if num > 120000:
            global crawlFinish
            crawlFinish += 1
            break
        print('set url')
        crawler.seturl(url=foreurl + str(num))
        bf = crawler.crawler()
        if bf is None:
            time.sleep(2)
            continue
        print('pack data')
        data = [bf, num]
        print('put it to queue')
        while dataQueue.full() is True:
            time.sleep(0.1)
        dataQueue.put(data)
        print('crawl game %d done' % num)
        time.sleep(3)


# 处理数据并写入数据库线程代理函数
def writeFunc():
    print('Write thread start!')
    db = DataOperator('localhost', 'hyy', '360121', 'mobileGameData')
    f = db.connect()
    if f:
        print('database connected!')
    else:
        return -1
    # url前缀
    foreurl = 'http://www.taptap.com/app/'
    crawler = Crawler(foreurl)
    flag = True     # 用于控制写线程何时结束
    print('ready to write')
    while flag:
        if dataQueue.empty():       # 若队列为空则让线程休息
            while dataQueue.empty() is True:
                # 若爬线程完成数量与爬线程数量相同，则退出
                if crawlFinish == crawlCount:
                    flag = False
                    db.closeConnection()
                    break
                else:
                    print('write thread sleep!!!! ')
                    time.sleep(5)
        if flag is False:
            break
        # 获取队列中的数据
        print('write thread try to get lock')
        lock.acquire()
        bf = dataQueue.get()
        lock.release()
        # 将数据写入数据库
        info = crawler.getData(bf[0])
        if info is None:
            time.sleep(4)
            continue
        info['Gno'] = bf[1]
        gflag = db.insertIntoDatabase(**info)
        if gflag:
            print('write game %d done!' % bf[1])
        else:
            print('Unable to write game %d!' % bf[1])


# 编写主函数(爬虫的主函数)
if __name__ == '__main__':
    crawlCount = 8  # 爬虫线程数量
    writeCount = 4  # 写线程数量
    crawlFinish = 0     # 完成爬数据任务的爬虫数量
    threadList = []
    print('Create crawl thread!')
    # 创建爬虫线程
    for x in range(crawlCount):
        print('Creating thread %d' % x)
        t = threading.Thread(target=crawlerFunc)
        threadList.append(t)
    # 创建写线程
    print('Create write thread!')
    for x in range(writeCount):
        print('Creating thread %d' % x)
        t = threading.Thread(target=writeFunc)
        threadList.append(t)
    # 启动线程
    print('Run thread!')
    cnt = -1
    for t in threadList:
        cnt += 1
        if cnt >= crawlCount:
            time.sleep(0.5)
        t.start()
    # 线程加入主线程，即让主线程作为守护线程
    print('thread join')
    for t in threadList:
        t.join()
    print('Writing successful!')
