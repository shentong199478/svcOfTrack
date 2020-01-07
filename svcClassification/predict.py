import sys
import os
last_path = os.path.dirname(os.getcwd())
sys.path.append(os.path.join(last_path,'svcOfTrack'))
dangqian_path = os.getcwd()
sys.path.append(os.path.join(os.path.join(dangqian_path,'components'),'svcOfTrack'))
sys.path.append(os.path.join(os.path.join(os.path.join(dangqian_path,'components'),'svcOfTrack'),'svcClassification'))
from getData import *
#from drawmap.map import *
import joblib
import  re
import math
import time
import numpy as np


class SvcClassifition:
    #svm模型加载且预处理数据预测
    def __init__(self,model_path):
        self.model_path = model_path
        self.load_model()

    def load_model(self):
        self.clf = joblib.load(self.model_path)

        # 预测
    def predict(self,X_test):
        # X_test = self.ss.transform(X_test)  # 数据标准�?
        Y_predict = self.clf.predict(X_test)  # 预测
        Y_predict_proba = self.clf.predict_proba(X_test)
        return Y_predict,Y_predict_proba

    def predict_proba(self,X_test):
        X_test = self.ss.transform(X_test)  # 数据标准�?
        Y_predict = self.lr.predict_proba(X_test)  # 预测
        return Y_predict

    # def load_model(self):
    #     joblib.load("logistic_ss1.model")  # 加载模型,会保存该model文件
    #     joblib.load("logistic_lr1.model")
    #     self.clf = joblib.load(self.model_path)

    def get_sign(self,content):
        timepattern = re.compile(r'time:(.*?),source')
        sourcepattern = re.compile(r'source:(.*?),lon')
        lonpattern = re.compile(r'lon:(.*?),lat')
        latpattern = re.compile(r'lat:(.*?),thead')
        theadpattern = re.compile(r'thead:(.*?),sog')
        sogpattern = re.compile(r'sog:(.*?),cog')
        cogpattern = re.compile(r'cog:(.*?),status')
        time_date = re.findall(timepattern, content)[0]
        source = int(re.findall(sourcepattern, content)[0])
        lon = float(re.findall(lonpattern, content)[0])
        lat = float(re.findall(latpattern, content)[0])
        thead = float(re.findall(theadpattern, content)[0])
        sog = float(re.findall(sogpattern, content)[0])
        cog = float(re.findall(cogpattern, content)[0])
        return {'time':time_date,'source':source,'lon':lon,'lat':lat,'thead':thead,'sog':sog,'cog':cog}


    @staticmethod
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

    @staticmethod
    def get_angle(a1, a2):
        return min(abs(a1 - a2), 360 - abs(a1 - a2))



    def get_feature(self,dic1,dic2,dic3):
        try:
            time1 = self.get_second(dic2['time']) - self.get_second(dic1['time'])
            time2 = self.get_second(dic3['time']) - self.get_second(dic2['time'])
        except:
            time1 = int(dic2['time']) - int(dic1['time'])
            time2 = int(dic3['time']) - int(dic2['time'])
        source1 = 1 if int(dic2['source']) != 300 else -1
        source2 = 1 if int(dic3['source']) != 300 else -1
        lon1 = (dic2['lon'] - dic1['lon']) * 100000 / time1
        lat1 = (dic2['lat'] - dic1['lat']) * 100000 / time1
        lon2 = (dic3['lon'] - dic2['lon']) * 100000 / time2
        lat2 = (dic3['lat'] - dic2['lat']) * 100000 / time2
        fea1 = source1
        fea2 = source2
        fea3 = abs(lon1 - lon2)
        fea4 = abs(lat1 - lat2)
        ang1 = self.angles(dic1['lon'], dic1['lat'], dic2['lon'], dic2['lat'])
        ang2 = self.angles(dic2['lon'], dic2['lat'], dic3['lon'], dic3['lat'])
        # fea5 = abs(ang1*2**dic2['sog']/ time1 - ang2*2**dic3['sog']/time2)
        fea5 = abs(self.get_angle(ang1,ang2))
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
        fea7 = abs(self.get_angle(dic3['thead'], ang2)) if math.ceil(dic3['thead']) not in [0,511,472] else 0 # 目标点航首向和角度差
        return [fea1,fea2,fea3,fea4,fea5,fea6,fea7,fea8]


    @staticmethod
    def get_second(string):
        timeArray = time.strptime(string, "%Y-%m-%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))
        return timeStamp




    def predict_list(self,lis):
        res_dic = dict()
        res_dic['feature'] = list()
        count = len(lis)
        for i in range(count):
            for j in range(len(lis[i])):
                if j in [1,2,3,4,6,7] and not lis[i][j]:
                    if i != 0:
                        lis[i][j] = lis[i-1][j]
                    else:
                        lis[i][j] = lis[i+1][j]
            time_date = int(lis[i][7])
            source = int(lis[i][1])
            lon = float(lis[i][4])
            lat = float(lis[i][3])
            thead = lis[i][8] if lis[i][8] else lis[i][2]
            thead = float(thead if thead else 511)
            sog = float(lis[i][6])
            cog =  ''#float(lis[i][2])
            res_dic['feature'].append({'time': time_date, 'source': source, 'lon': lon, 'lat': lat, 'thead': thead, 'sog': sog, 'cog': cog})
        last_true_index1 = 0
        last_true_index2 = 1
        flag1 = False
        flag2 = False
        for index in range(len(res_dic['feature'])):
            if res_dic['feature'][index]['source'] != 300 and not flag1:
                last_true_index1 = index
                flag1 = True
            elif res_dic['feature'][index]['source'] != 300 and flag1:
                last_true_index2 = index
                flag2 = True
            if index > 10 or (flag1 and flag2):
                break
        if (flag1 and flag2 and last_true_index2 > 10) or (not flag2):
            flag1 = False
            for index in range(len(res_dic['feature'])):
                if res_dic['feature'][index]['source'] == 300 and not flag1:
                    last_true_index1 = index
                    flag1 = True
                elif res_dic['feature'][index]['source'] == 300 and flag1:
                    last_true_index2 = index
        if last_true_index2 > 10:
            last_true_index1 = 0
            last_true_index2 = 1
        for i in range(last_true_index2+1):
            if i == 0:
                res_dic['predict'] = [-1, ]
            else:
                if res_dic['feature'][i]['sog'] < 5:
                    res_dic['predict'].append(-1)
                else:
                    ang1 = self.angles(res_dic['feature'][i-1]['lon'], res_dic['feature'][i-1]['lat'], res_dic['feature'][i]['lon'], res_dic['feature'][i]['lat'])
                    thead = res_dic['feature'][i]['thead']
                    thead = thead if math.ceil(float(thead)) != 0 and math.ceil(float(thead))< 360 else ang1
                    jiajiao1 = abs(self.get_angle(ang1, thead))
                    if jiajiao1 > 100:

                        res_dic['predict'].append(1)
                    else:
                        res_dic['predict'].append(-1)

        flag = 0
        for i in range(last_true_index2+1,count):
            features = self.get_feature(res_dic['feature'][last_true_index1],res_dic['feature'][last_true_index2],res_dic['feature'][i])
            a,b = self.predict(np.array([features]))
            a = int(a[0])
            result = a if int(res_dic['feature'][i]['sog']) > 1 and int(res_dic['feature'][i]['time'] - res_dic['feature'][i-1]['time'] ) < 7200 and int(res_dic['feature'][i]['source']) != 9046  and i != count-1 else -1
            if result == 1:
                flag += 1
            else:
                flag = 0
            if flag > 5:
                a1, b1 = self.predict(np.array([self.get_feature(res_dic['feature'][i-2],res_dic['feature'][i-1],res_dic['feature'][i])]))
                a2, b2 = self.predict(np.array([self.get_feature(res_dic['feature'][i-3],res_dic['feature'][i-1],res_dic['feature'][i])]))
                if int(a1[0]) == -1 and int(a2[0]) == -1:
                    res_dic['predict'].append(-1)
                    last_true_index1 = i-2
                    last_true_index2 = i-1
            else:
                res_dic['predict'].append(result)
            if result == -1:
                last_true_index1 = last_true_index2
                last_true_index2 = i
        return res_dic


if __name__ == '__main__':
    import pandas as pd

    sys.path.append(os.path.join(last_path, 'getData'))
    from getData.hbase_zhengshi import HbaseZS



    m = Map()
    hbase_out = HbaseZS()
    last_path = os.path.dirname(os.getcwd())
    model_path = os.path.join(last_path,r"model\1226_1.model")
    svc = SvcClassifition(model_path)
    mmsi_list = [477752100, 477752200, 477181700, 477942400, 477454300, 477548400, 477167300, 414436000, 477150500, 413828000, 565003000, 574375000, 419001327, 477686500,
            372632000, 636015455, 538004459, 564290000, 538004367, 538004243, 477264400, 477435100, 353242000, 563077300,419001333]



    d = list()
    for i in mmsi_list:
        i =  564290000

        # if i in mmsi_list:
        #     continue

        res = hbase_out.get_data_from_zs(i)
        if len(res) < 3:
            continue
        res_list = list()
        point_list = list()
        for row in res:
            res_list.append([row['mmsi'],row['source'],row['cog'],row['latitude'],row['longitude'],row['rot'],row['sog'],row['time'],row['trueHeading']])
            point_list.append([float(row['longitude']),float(row['latitude'])])
        point_dic = svc.predict_list(res_list)
        print(point_dic)
        start =55
        end = 65
        index_list = list(i[0] for i in list(enumerate(point_dic['predict'])) if i[1] == 1)
        zhixin_list = list()
        if index_list:
            print(i)
            print(index_list)
        for j in index_list:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(res_list[j][7]))))
        # if len(index_list) > 8:
        #     print(i)
        #     print(index_list)
        # while True:
        #     c = []
        #     for k in range(start,end):
        #         if k in index_list:
        #             c.append(k-start)
        #     intersection = [i for i in range(start,end) if i in index_list]
        #     if intersection:
        #         m.draw_point(point_list[start:end],c)
        #         m.draw_line(point_list[start:end],c)
        #         m.show()
        #         print(start)
        #     start += 20
        #     end += 20
        #     if end >= len(res):
        #         break
        # print(index_list)
        c = []
        for k in range(start, end):
            if k in index_list:
                c.append(k - start)
        m.draw_point(point_list[start:end], c)
        m.draw_line(point_list[start:end], c)
        m.show()
        # break
        break

