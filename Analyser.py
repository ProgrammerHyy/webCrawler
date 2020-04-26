from DataOperator import DataOperator
import re


# 获取玩家数最多的5000个游戏的所有tag，以及对应tag的玩家数量
def getTagPlayer(mode, val=None):
    db = DataOperator('localhost', 'hyy', '360121', 'mobileGameData')
    db.connect()
    if mode == 0:
        data = db.selectData()
    elif mode == 1:
        data = db.selectSpData(val)
    else:
        print('无效的mode参数，请重新输入')
        return -1
    db.closeConnection()
    tagCount = {}
    tagT = []
    # 通过迭代器与生成器的方式，获取数据并进行拆分，获取需要的信息
    while True:
        try:
            res = next(data)
            player = res[4]     # 获取玩家数量
            tagList = res[3]    # 获取tag列表
            # 对tag列表进行拆分，获取所有的tag
            tagList = tagList[1:len(tagList)-1]
            tagList = tagList.replace(',', '8')
            tagList = tagList.replace("'", '8')
            tagList = re.split('(?:8+)', tagList)
            # 遍历列表，并计算每个tag的玩家总数
            for tag in tagList:
                if tag == ' ' or tag == '':
                    continue
                if tag in tagCount:
                    tagCount[tag] += player
                else:
                    tagCount[tag] = player
                if tag not in tagT:
                    tagT.append(tag)
        # 当出现异常时，表示已经迭代结束，返回需要的数据
        except StopIteration:
            return tagCount


def draw(mode, val=None):
    allCount = getTagPlayer(mode=mode, val=val)
    allCount = sorted(allCount.items(), key=lambda x: x[1], reverse=True)  # 对allCount按照value排序
    allTag = []  # 存放绘制时用的lable
    explodeList = []  # 用于存放绘制饼状图时的explode值（前四个设置该值）
    count = []  # 存放绘制时用的数字
    cnt = 0
    # 设置要绘制的数据
    for t in allCount:
        cnt += 1
        allTag.append(t[0])
        count.append(t[1])
        if cnt >= 10:
            break
    # 设置explode
    for x in range(10):
        if x < 4:
            explodeList.append(0.1)
        else:
            explodeList.append(0)
    # 将各种数据封装成字典返回
    data = {'explode': explodeList, 'color': ['red', 'yellow', 'green', 'orange', 'pink', 'blue'], 'tag': allTag,
            'count': count}
    return data

