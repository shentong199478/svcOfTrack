import numpy as np
import re
import time
import math
from excel_use import *
import pandas as pd
import sys
import os
last_path = os.path.dirname(os.getcwd())
sys.path.append(os.path.join(last_path,'data'))


class EmailData2(object):
    def __init__(self,data,del_one):
        self.data = data
        self.del_one = del_one


    def get_data(self):
        pattern = re.compile(r'(mmsi:.*?status:\d)')
        index1 = re.findall(pattern, self.data)
        timelist1 = list()
        sourcelist = list()
        lonlist = list()
        latlist = list()
        theadlist = list()
        soglist = list()
        coglist = list()

        timepattern = re.compile(r'time:(.*?),source')
        sourcepattern = re.compile(r'source:(.*?),lon')
        lonpattern = re.compile(r'lon:(.*?),lat')
        latpattern = re.compile(r'lat:(.*?),thead')
        theadpattern = re.compile(r'thead:(.*?),sog')
        sogpattern = re.compile(r'sog:(.*?),cog')
        cogpattern = re.compile(r'cog:(.*?),status')
        for i in index1:
            timelist1.append(re.findall(timepattern, i)[0])
            sourcelist.append(int(re.findall(sourcepattern,i)[0]))
            lonlist.append(float(re.findall(lonpattern, i)[0]))
            latlist.append(float(re.findall(latpattern, i)[0]))
            theadlist.append(float(re.findall(theadpattern, i)[0]))
            soglist.append(float(re.findall(sogpattern, i)[0]))
            coglist.append(float(re.findall(cogpattern, i)[0]))
        timelist = list()
        for i in timelist1:
            timelist.append(self.get_second(i))
        return index1,timelist,sourcelist,lonlist,latlist,theadlist,soglist,coglist



    def get_second(self,string):
        timeArray = time.strptime(string, "%Y-%m-%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))
        return timeStamp





    def angles(self,llon, llat, rlon, rlat):
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

    def get_angle(self,a1, a2):
        return min(abs(a1 - a2), 360 - abs(a1 - a2))

    def get_feature(self,point_list,index,timelist,sourcelist,lonlist,latlist,theadlist,soglist,coglist,del_one):
        last_true_index1 = 0
        last_true_index2 = 1
        for i in range(len(timelist)-2):

            time1 = timelist[last_true_index2] - timelist[last_true_index1] #标记点和前一个点的时间差
            time2 = timelist[i+2] - timelist[last_true_index2] #标记点后一个点和标记点的时间差
            source1 = 1 if str(sourcelist[last_true_index2]) != '300' else -1
            source2 = 1 if str(sourcelist[i+2]) != '300' else -1

            lon1 = (lonlist[last_true_index2] - lonlist[last_true_index1])*100000/time1   #标记点和前一个点的经度差
            lat1 = (latlist[last_true_index2] - latlist[last_true_index1])*100000/time1   #标记点和前一个点的纬度差
            lon2 = (lonlist[i+2] - lonlist[last_true_index2])*100000/time2   #标记点和后一个点的经度差
            lat2 = (latlist[i+2] - latlist[last_true_index2])*100000/time2   #标记点和后一个点的纬度差
            fea1 = source1
            fea2 = source2
            fea3 = abs(lon1 - lon2)
            fea4 = abs(lat1 - lat2)
            ang1 = self.angles(lonlist[last_true_index1], latlist[last_true_index1], lonlist[last_true_index2], latlist[last_true_index2])  # 目标点和前一个点的坐标角度
            ang2 = self.angles(lonlist[last_true_index2], latlist[last_true_index2], lonlist[i+2], latlist[i+2])  # 目标点后一个点和目标点的坐标角度
            fea5 = abs(self.get_angle(ang1, ang2))
            if time2 > 7200:
                fea6 = 0
            else:
                fea6 = 1
            if soglist[i+2] <= 4 or soglist[last_true_index2] <= 4:
                fea8 = 0
            elif soglist[i+2] < 6:
                fea8 = 1
            elif soglist[i+2] < 9:
                fea8 = 2
            else:
                fea8 = 3
            # fea6 = abs(self.get_angle(theadlist[last_true_index1],ang2))*2**soglist[last_true_index2]/(1000*time1) #目标点前一个点航首向和角度差
            fea7 = abs(self.get_angle(theadlist[i+2],ang2)) if math.ceil(theadlist[i+2]) not in [0,511] else 0#目标点航首向和角度差
            # sog1 = soglist[i+1] - soglist[i]
            # sog2 = soglist[i+2] - soglist[i+1]
            # cog1 = coglist[i]      #目标点前一个点的航迹向
            # cog2 = coglist[i+1]    #目标点的航迹向
            # cog3 = coglist[i+2]    #目标点后一个点的航迹向
            if str(i+2) in self.del_one:
                l = 1
            else:
                l = -1
                last_true_index1 = last_true_index2
                last_true_index2 = i+2
            point_list.append([fea1,fea2,fea3,fea4,fea5,fea6,fea7,fea8,l,index[i+2]])
        return point_list

    def get_point(self):
        index,timelist, sourcelist,lonlist, latlist, theadlist, soglist, coglist = self.get_data()
        point_list = list()
        res = self.get_feature(point_list,index,timelist,sourcelist,lonlist,latlist,theadlist,soglist,coglist,del_one)
        return res



def read_excel():
    df = pd.read_excel(os.path.join(last_path,r'data\标记数据源1111.xls'))
    return df['data'],df['del']
if __name__ == '__main__':
    res1,res2 = read_excel()
    a = ExcelTools()
    book_name_xls = os.path.join(last_path,r'data\邮箱标签数据12-23.xls')
    sheet_name_xls = '数据'
    value_title = [[ "fea1","fea2","fea3","fea4","fea5","fea6","fea7","fea8", "predict","index"], ]
    a.write_excel_xls(book_name_xls, sheet_name_xls, value_title)

    for i in range(len(res1)):
        data = res1[i]
        del_one = str(res2[i]).split()

#     labeldata = '''mmsi: 477548400,time:2019-10-07 21:38:00,source: 9046,lon: 121.189384,lat: 39.795235,thead: 37,sog: 12.9,cog:38.2,status:0
# mmsi: 477548400,time:2019-10-07 21:50:00,source: 300,lon: 121.23019,lat: 39.83526,thead: 38,sog: 12.3,cog:39.600002,status:0
# mmsi: 477548400,time:2019-10-07 22:14:00,source: 9046,lon: 121.28492,lat: 39.887085,thead: 37,sog: 10.1,cog:38.2,status:0
# mmsi: 477548400,time:2019-10-07 22:38:00,source: 300,lon: 121.12112,lat: 39.729233,thead: 38,sog:12.900001,cog:39.3,status:0
# mmsi: 477548400,time:2019-10-08 01:50:00,source: 300,lon: 121.5032,lat: 40.17391,thead: 8,sog: 0.3,cog:93.8,status:1
# mmsi: 477548400,time:2019-10-08 02:56:00,source: 300,lon: 121.50308,lat: 40.173965,thead: 11,sog: 0.2,cog:114.9,status:1'''
#     del_one = [3,]
        del_str = ''
        for i in del_one:
            del_str += str(i)
            del_str += ' '
        datafrom = [[data,del_str],]
        if '0' not in del_one and '1' not in del_one:
            emaildata = EmailData2(data,del_one)
            res = emaildata.get_point()



        # data_name_xls = "标记数据源1111.xls"
            sheet_xls = '1'
            value_title1 = [["labeldata","del"],]
            # a.write_excel_xls(data_name_xls, sheet_xls, value_title1)
            if res:
                a.write_excel_xls_append(book_name_xls, res)
        # a.write_excel_xls_append(data_name_xls, datafrom)







