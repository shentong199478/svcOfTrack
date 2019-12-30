from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import  time

class Map:
    def __init__(self):
        # self.get_map()
        pass

    def get_map(self):
        self.map = Basemap()  # 实例化一个map
        self.map.drawcoastlines()  # 画海岸线
        self.map.drawmapboundary(fill_color='white')
        self.map.fillcontinents(color='white', lake_color='white')  # 画大洲，颜色填充为白色
        # m.fillcontinents(color='none',lake_color='white') # 如果color设置为none,则地图为透明

        parallels = np.arange(-90., 90., 10.)  # 这两行画纬度，范围为[-90,90]间隔为10
        self.map.drawparallels(parallels, labels=[False, True, True, False])
        meridians = np.arange(-180., 180., 20.)  # 这两行画经度，范围为[-180,180]间隔为10
        self.map.drawmeridians(meridians, labels=[True, False, False, True])

    def draw_map(self,lon,lat):
        lon,lat = self.map(lon,lat)
        self.map.scatter(lon, lat, s=100)  # 标注出所在的点，s为点的大小，还可以选择点的性状和颜色等属性
        plt.show()

    def draw_point(self,point_list,flag_list):
        for i in range(len(point_list)):
            if i not in flag_list:
                plt.scatter(point_list[i][0],point_list[i][1],s=10,c='grey')
            else:
                plt.scatter(point_list[i][0],point_list[i][1],s=10,c='red')

        for i in range(len(point_list)):
            # plt.text(point_list[i], point_list[i, 1], i)
            plt.annotate(str(i), xy=(point_list[i][0], point_list[i][1]), xytext=(point_list[i][0], point_list[i][1]))


    def draw_line(self,point_list,flag_list):
        a = list()
        b = list()
        for i in range(len(point_list)):
            if i not in flag_list:
                a.append(point_list[i][0])
                b.append(point_list[i][1])
        plt.plot(a,b)

    def show(self):
        plt.show()
        # plt.ion()
        # plt.pause(20)
        # plt.close

if __name__ == '__main__':
    m = Map()

    m.draw_point([[06.886795,-6.097192],[06.79231,-6.1132]],[])
    m.draw_line([(06.886795,-6.097192),(06.79231,-6.1132)],[])
    m.show()




