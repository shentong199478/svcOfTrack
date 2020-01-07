# -*-coding:utf-8-*-
import os,sys,time
last_path = os.path.abspath(os.path.join(os.getcwd(), "../.."))
project_path = os.path.abspath(os.path.join(os.getcwd(), "../../.."))
#sys.path.append(os.path.join(os.path.join(project_path,r'hd_packages'),r'src'))
dangqian_path = os.getcwd()
sys.path.append(os.path.join(dangqian_path,'components'))
sys.path.append('/root/bigdata3/components')


from hd_utils import email_util, geo_util, hbase_util, image_util, time_util,task2

sys.path.append(last_path)
from business.config import Config
from models.ship_pos import ShipPos
from svcOfTrack.svcClassification.predict import *
import happybase
class TrailCheck(object):
    def __init__(self, mmsi, bg, ed, delete=False):
        self.delete = delete
        hbase_util.HbaseWebHandle.init("192.168.29.2", "8080")
        self.points = hbase_util.HbaseShipPos().get_ship(mmsi, bg, ed, ShipPos)
        self.points = list(self.points)

        last_path = os.path.join(os.path.join(os.getcwd(),'components'),'svcOfTrack')
        model_path = os.path.join(os.path.join(last_path,'model'), r"1226_1.model")
        model_path = '/root/bigdata3/components/svcOfTrack/model/1226_1.model'
        svc = SvcClassifition(model_path)
        self.svc = svc

    def del_point(self,del_list):
        for i in del_list:
            hbase_util.HbaseShipPos().delete("ship_historical_trace", str(i))
            hbase_util.HbaseShipPos().delete("st_ship_historical_trace", str(i))

    def input_data(self,index_list):
        connection = happybase.Connection(host='192.168.29.104', port=9090)
        #hbase_util.HbaseWebHandle('192.168.29.2','8080')
        table = connection.table('ship_error_point')
        for i in range(len(self.points)):
            if i in index_list:
                data = dict()
                try:
                    data['info:addTime'] = bytes(str(self.points[i].addTime), encoding="utf8")
                    data['info:mmsi'] = bytes(str(self.points[i].mmsi), encoding="utf8")
                    data['info:trueHeading'] = bytes(str(self.points[i].trueHeading), encoding="utf8")
                    data['info:latitude'] = bytes(str(self.points[i].latitude), encoding="utf8")
                    data['info:sog'] = bytes(str(self.points[i].sog), encoding="utf8")
                    data['info:source'] = bytes(str(self.points[i].source), encoding="utf8")
                    data['info:rot'] =  bytes(str(self.points[i].rot), encoding="utf8")
                    data['info:cog'] =  bytes(str(self.points[i].cog), encoding="utf8")
                    data['info:time'] =  bytes(str(self.points[i].time), encoding="utf8")
                    data['info:navStatus'] = bytes(str(self.points[i].navStatus), encoding="utf8")
                    data['info:longitude'] = bytes(str(self.points[i].longitude), encoding="utf8")
                    data['info:is_satelite'] = bytes('1' if self.points[i].is_satelite else '2', encoding="utf8")
                    #data['addTime'] = str(self.points[i].addTime)
                    #data['mmsi'] = str(self.points[i].mmsi)
                    #data['trueHeading'] = str(self.points[i].trueHeading)
                    #data['latitude'] = str(self.points[i].latitude)
                    #data['sog'] = str(self.points[i].sog)
                    #data['source'] = str(self.points[i].source)
                    #data['cog'] =  str(self.points[i].cog)
                    #data['time'] =  str(self.points[i].time)
                    #data['navStatus'] = str(self.points[i].navStatus)
                    #data['longitude'] = str(self.points[i].longitude)
                    #data['is_satelite'] = '1' if self.points[i].is_satelite else '2'
                    with table.batch() as bat:
                        bat.put(self.points[i].rowKey, data)
                    #hbase_util.HbaseWebHandle().insert('ship_error_point', str(self.points[i].rowKey), 'info', data)
                except Exception as e:
                    print(e)
                    continue



    def process(self):
        text_lst = []
        trail_lst = []
        if len(self.points) > 2:
            del_list,index_list = self.check()
        else:
            del_list,index_list = [],[]
        # for i in del_list:
        #     print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(i[9:]))))
        if index_list:
            lengthOfPoint = len(self.points)
            if lengthOfPoint <= 5:
                text = "<br>".join([p.brief for p in [self.points[i] for i in range(lengthOfPoint)]])
                text += "<br>del:{0}".format(",".join(index_list))
                trail = [(self.points[i].longitude, self.points[i+1].latitude) for i in range(lengthOfPoint-1)]
                text_lst.append(text)
                trail_lst.append(trail)
            else:
                index_list_tmp = index_list.copy()
                for i in index_list_tmp:
                    if i == 1:
                        trail = [(self.points[j].longitude, self.points[j].latitude) for j in range(4)]
                        text = "<br>".join([p.brief for p in [self.points[j] for j in range(4)]])
                        text += "<br>del:{0}".format(",".join(['1']))
                    elif i in [lengthOfPoint-1,lengthOfPoint-2]:
                        trail = [(self.points[j].longitude, self.points[j].latitude) for j in range(lengthOfPoint-5,lengthOfPoint)]
                        text = "<br>".join([p.brief for p in [self.points[j] for j in range(lengthOfPoint-5,lengthOfPoint)]])
                        text += "<br>del:{0}".format(",".join([str(i-(lengthOfPoint-5))]))
                    else:
                        del_index = []
                        trail = [(self.points[j].longitude, self.points[j].latitude) for j in range(i-2,i+3)]
                        text = "<br>".join([p.brief for p in [self.points[j] for j in range(i-2,i+3)]])
                        del_index.append('2')
                        for k in [i-1,i+1,i+2]:
                            if k in index_list_tmp:
                                del_index.append(str(k-i+2))
                                index_list_tmp.remove(k)
                        text += "<br>del:{0}".format(",".join(del_index))
                    text_lst.append(text)
                    trail_lst.append(trail)
            if text_lst:
                e = email_util.EmailHandle("shentong_9478@163.com", ["shentong@huadong.net"], "shen1234", "smtp.163.com", 25)
                u = image_util.ImageUtil()
                e.sand_img("",text_lst,[u.line(path) for path in trail_lst])
            self.input_data(index_list)
            self.del_point(del_list)





    def get_del_index(self,res_list):
        return list(i[0] for i in enumerate(res_list) if i[1] == 1)

    def check(self):
        res_list = list()
        for row in self.points:
            res_list.append([row.mmsi,row.source,row.cog,row.latitude,row.longitude,row.rot,row.sog,time.mktime(time.strptime(str(row.time), "%Y-%m-%d %H:%M:%S")),row.trueHeading])
        point_dic = self.svc.predict_list(res_list)
        del_list = list()
        del_index_list = self.get_del_index(point_dic['predict'])
        for i in del_index_list:
            del_list.append(self.points[i].rowKey)
        index_list = list(i[0] for i in list(enumerate(point_dic['predict'])) if i[1] == 1)
        return del_list,index_list




class TrailCheckTask(task2.TaskTimer):
    def __init__(self, name, interval=1800):
        super().__init__(name, time_util.BTime().add(S=-1*interval).str_long,step_max=interval,step_mid=interval,step_min=interval)
        self.reset()
    def process(self, *args):
        ed = time_util.BTime()
        bg = time_util.BTime(ed.int - 86400)
        mmsi_list = [477752100, 477752200, 477181700, 477942400, 477454300, 477548400, 477167300, 414436000, 477150500, 413828000, 565003000, 574375000, 419001327, 477686500,
            372632000, 636015455, 538004459, 564290000, 538004367, 538004243, 477264400, 477435100, 353242000, 563077300,419001333]
        # mmsi_list = [564290000]
        for mmsi in mmsi_list:
            c = TrailCheck(mmsi,bg,ed)
            c.process()
if __name__ == '__main__':
    Config.init("test").init_zk("192.168.29.7,192.168.29.8,192.168.29.9").init_hbase_ship_pos("hbase_web")

    t = TrailCheckTask(Config().app_name)
    t.run_loop()
