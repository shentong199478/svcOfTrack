import pandas as pd
import math
from excel_use import *
import re,time,sys
import random as rd
sys.path.append(r"D:\shentong\svcOfTrack\svcClassification")


def angles(llon, llat, rlon, rlat):
    angle = 0
    dy = rlat - llat
    dx = rlon - llon
    if dx == 0 and dy > 0:
        angle = 0
    if dx == 0 and dy < 0:
        angle = 180
    if dy == 0 and dx > 0:
        angle = 90
    if dy == 0 and dx < 0:
        angle = 270
    if dx > 0 and dy > 0:
        angle = math.atan(dx / dy) * 180 / math.pi
    elif dx < 0 and dy > 0:
        angle = 360 + math.atan(dx / dy) * 180 / math.pi
    elif dx < 0 and dy < 0:
        angle = 180 + math.atan(dx / dy) * 180 / math.pi
    elif dx > 0 and dy < 0:
        angle = 180 + math.atan(dx / dy) * 180 / math.pi
    return angle

def get_second(string):
    timeArray = time.strptime(string, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    return timeStamp

def get_angle(a1, a2):
    return min(abs(a1 - a2), 360 - abs(a1 - a2))

def get_feature(dic1,dic2,dic3):
    try:
        time1 = get_second(dic2['time']) - get_second(dic1['time'])
        time2 = get_second(dic3['time']) - get_second(dic2['time'])
    except:
        time1 = int(dic2['time']) - int(dic1['time'])
        time2 = int(dic3['time']) - int(dic2['time'])
    source1 = 1 if dic2['source'] != '300' else -1
    source2 = 1 if dic3['source'] != '300' else -1
    lon1 = (dic2['lon'] - dic1['lon']) * 100000 / time1
    lat1 = (dic2['lat'] - dic1['lat']) * 100000 / time1
    lon2 = (dic3['lon'] - dic2['lon']) * 100000 / time2
    lat2 = (dic3['lat'] - dic2['lat']) * 100000 / time2
    fea1 = source1
    fea2 = source2
    fea3 = abs(lon1 - lon2)**2
    fea4 = abs(lat1 - lat2)**2
    ang1 = angles(dic1['lon'], dic1['lat'], dic2['lon'], dic2['lat'])
    ang2 = angles(dic2['lon'], dic2['lat'], dic3['lon'], dic3['lat'])
    # fea5 = abs(ang1*2**dic2['sog']/ time1 - ang2*2**dic3['sog']/time2)
    fea5 = abs(get_angle(ang1,ang2))
    if time2 > 7200:
        fea6 = 0
    else:
        fea6 = 1
    if dic3['sog'] < 3 or dic2['sog'] < 3:
        fea8 = 0
    elif dic3['sog'] < 6:
        fea8 = 1
    elif dic3['sog'] < 9:
        fea8 = 2
    else:
        fea8 = 3
    fea7 = abs(get_angle(dic3['thead'], ang2))  # 目标点航首向和角度差
    print(fea5)
    print(fea7)
    return [fea1,fea2,fea3,fea4,fea5,fea6,fea7,fea8]

def get_point():
    index,timelist, sourcelist,lonlist, latlist, theadlist, soglist, coglist = get_data()
    point_list = list()
    res = get_feature(point_list,index,timelist,sourcelist,lonlist,latlist,theadlist,soglist,coglist)
    return res

def get_data(a,b,c):

    dic3 = eval(a)
    dic2 = eval(b)
    dic1 = eval(c)
    try:
        time1 = get_second(dic2['time']) - get_second(dic1['time'])
        time2 = get_second(dic3['time']) - get_second(dic2['time'])
    except:
        time1 = int(dic2['time']) - int(dic1['time'])
        time2 = int(dic3['time']) - int(dic2['time'])
    source1 = 1 if int(dic2['source']) != 300 else -1
    source2 = 1 if int(dic3['source']) != 300 else -1
    lon1 = (dic2['lon'] - dic1['lon']) * 100000 / time1
    lat1 = (dic2['lat'] - dic1['lat']) * 100000 / time1
    lon2 = (dic3['lon'] - dic2['lon']) * 100000 / time2
    lat2 = (dic3['lat'] - dic2['lat']) * 100000 / time2

    # lon1 = (dic2['lon'] - dic1['lon'])*(1+rd.randint(1, 10)/1000) * 100000 / time1
    # lat1 = (dic2['lat'] - dic1['lat'])*(1+rd.randint(1, 10)/1000) * 100000 / time1
    # lon2 = (dic3['lon'] - dic2['lon'])*(1+rd.randint(1, 10)/1000) * 100000 / time2
    # lat2 = (dic3['lat'] - dic2['lat'])*(1+rd.randint(1, 10)/1000) * 100000 / time2
    fea1 = source1
    fea2 = source2
    fea3 = abs(lon1 - lon2)
    fea4 = abs(lat1 - lat2)
    ang1 = angles(dic1['lon'], dic1['lat'], dic2['lon'], dic2['lat'])
    ang2 = angles(dic2['lon'], dic2['lat'], dic3['lon'], dic3['lat'])
    # ang1 = angles(dic1['lon'], dic1['lat'], dic2['lon'], dic2['lat'])*(1+rd.randint(1, 10)/1000)
    # ang2 = angles(dic2['lon'], dic2['lat'], dic3['lon'], dic3['lat'])*(1+rd.randint(1, 10)/1000)
    fea5 = abs(get_angle(ang1,ang2))
    if time2 > 7200:
        fea6 = 0
    else:
        fea6 = 1
    if dic3['sog'] <= 4 or dic2['sog'] <= 4:
        fea8 = 0
    elif dic3['sog'] < 6:
        fea8 = 1
    elif dic3['sog'] < 9:
        fea8 = 2
    else:
        fea8 = 3
    fea7 = abs(get_angle(dic3['thead'], ang2)) if math.ceil(dic3['thead']) not in [0,511] else 0
    # fea7 = abs(get_angle(dic3['thead']*(1+rd.randint(1, 10)/1000), ang2))
    return [fea1,fea2,fea3,fea4,fea5,fea6,fea7,fea8]


def read_excel():
    df = pd.read_excel(r'D:\shentong\svcOfTrack\data\正确点.xlsx')
    return df['data1'],df['data2'],df['data3']

res1,res2,res3 = read_excel()
a = ExcelTools()
book_name_xls = r'D:\shentong\svcOfTrack\data\excelfile.xls'
sheet_name_xls = '1'
value_title = [[ "fea1", "fea2", "fea3", "fea4", "fea5","fea6","fea7","fea8"], ]
a.write_excel_xls(book_name_xls, sheet_name_xls, value_title)
shuchu = list()
for i in range(len(res1)):
# for i in range(100):
    shuchu = get_data(res1[i],res2[i],res3[i])
    a.write_excel_xls_append(book_name_xls, [shuchu])
    