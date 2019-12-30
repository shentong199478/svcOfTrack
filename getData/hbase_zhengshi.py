import os,sys
sys.path.append(r'D:\shentong\shiptracker_python\hd_packages\src')
from hd_utils.time_util import *
from hd_utils.hbase_util  import HbaseShipPos
import string
import time,datetime
from excel_use import *



class HbaseZS:
    def __init__(self):
        pass
    # bg = time_util.BTime.from_str("2019-11-13 13:14:00")
    # ed = time_util.BTime.from_str("2019-12-02 11:00:00")
    # print(bg)
    # print(type(bg))


    #返回有序的两小时内船的信息
    def get_data_from_zs(self,mmsi):
        ed = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 先获得时间数组格式的日期
        threeDayAgo = (datetime.datetime.now() - datetime.timedelta(days = 2))
        # 转换为时间戳
        # timeStamp = int(time.mktime(threeDayAgo.timetuple()))
        # 转换为其他字符串格式
        bg = threeDayAgo.strftime("%Y-%m-%d %H:%M:%S")
        # bg = '2019-12-14 00:00:00'
        # ed = '2019-12-18 00:00:00'  24-27
        bg = '2019-12-01 00:00:00'
        ed = '2019-12-10 00:00:00'
        bg = BTime.from_str(bg)
        ed = BTime.from_str(ed)



        a = HbaseShipPos("192.168.29.2", "8080")

        #
        # mmsi_list = [477752100, 477752200, 477181700, 477942400, 477454300, 477548400, 477167300, 414436000, 477150500, 413828000, 565003000, 574375000, 419001327, 477686500,
        #             372632000, 636015455, 538004459, 564290000, 538004367, 538004243, 477264400, 477435100, 353242000, 563077300,419001333]


    #写入excel
    # value_title = [["time", "time2","source", "lon1", "lon2", "ang1","ang2","thead1","thead2","thead3","thead4","sog1",\
    #     "sog2","sog3","cog1","cog2","cog3","last_is_ture","predict","index"], ]
    # b = ExcelTools()
    # for mmsi in mmsi_list:
    #     book_name_xls = r'data\%s.xls' % mmsi
    #     sheet_name_xls = '1'
    #     value_title = [['mmsi','thead','lat','lon','sog','source','rot','cog','time']]
    #     b.write_excel_xls(book_name_xls, sheet_name_xls, value_title)
    #     for row in a.get(mmsi, bg, ed):
    #         print(row)
            # res = [[row['mmsi'],row['trueHeading'],row['latitude'],row['longitude'],row['sog'],row['source'],row['rot'],row['cog'],row['time']]]
    #         b.write_excel_xls_append(book_name_xls, res)


        # for mmsi in mmsi_list:
        m= [row for row in a.get(mmsi, bg, ed)]

        m.sort(key=lambda x: int(x["time"]))
        return m


if __name__ == '__main__':
    import os,sys
    sys.path.append(r'D:\shentong\shiptracker_python\hd_packages\src')
    from hd_utils.time_util import *
    from hd_utils.hbase_util  import HbaseShipPos
    import string
    import time,datetime
    from hbase_out.excel_use import *
    #
    #
    #
    #
    # bg = time_util.BTime.from_str("2019-12-11 13:14:00")
    # ed = time_util.BTime.from_str("2019-12-12 11:00:00")
    bg = time_util.BTime.from_str("2019-12-28 00:00:00")
    ed = time_util.BTime.from_str("2019-12-30 00:00:00")
    # # print(bg)
    # # print(type(bg))
    # ed = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #
    # # 先获得时间数组格式的日期
    # threeDayAgo = (datetime.datetime.now() - datetime.timedelta(days = 2))
    # # 转换为时间戳
    # # timeStamp = int(time.mktime(threeDayAgo.timetuple()))
    # # 转换为其他字符串格式
    # bg = threeDayAgo.strftime("%Y-%m-%d %H:%M:%S")
    # bg = BTime.from_str(bg)
    # ed = BTime.from_str(ed)
    #
    #
    #
    a = HbaseShipPos("192.168.29.2", "8080")

    # #
    # # data=['3744240001575853080','3744240001575840000','3744240001575830160','3744240001575825120','3744240001575797880','3744240001575751560','3744240001575748560','3744240001575744240','3744240001575700560','3744240001575678840','3744240001575661080','3744240001575657000','3744240001575622800','3744240001575580680','3744240001575578640','3744240001575535200']
    mmsi_list = [477752100, 477752200, 477181700, 477942400, 477454300, 477548400, 477167300, 414436000, 477150500, 413828000, 565003000, 574375000, 419001327, 477686500,
                372632000, 636015455, 538004459, 564290000, 538004367, 538004243, 477264400, 477435100, 353242000, 563077300,419001333]

    for row in a.get(538004459,bg,ed):
        print(row)

    #写入excel
    # value_title = [["time", "time2","source", "lon1", "lon2", "ang1","ang2","thead1","thead2","thead3","thead4","sog1",\
    #     "sog2","sog3","cog1","cog2","cog3","last_is_ture","predict","index"], ]
    # b = ExcelTools()
    # for mmsi in mmsi_list:
    #     book_name_xls = r'data\%s.xls' % mmsi
    #     sheet_name_xls = '1'
    #     value_title = [['mmsi','thead','lat','lon','sog','source','rot','cog','time']]
    #     b.write_excel_xls(book_name_xls, sheet_name_xls, value_title)
    #     for row in a.get(mmsi, bg, ed):
    #         print(row)
            # res = [[row['mmsi'],row['trueHeading'],row['latitude'],row['longitude'],row['sog'],row['source'],row['rot'],row['cog'],row['time']]]
    #         b.write_excel_xls_append(book_name_xls, res)
    # zs = HbaseZS()
    #
    #
    # for mmsi in mmsi_list:
    #     r = zs.get_data_from_zs(mmsi)
    #     print(r)


