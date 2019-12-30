from map import Map
# from ..hbase_out.hbase_outport import HbaseUtil
import os,sys
last_path = os.path.dirname(os.getcwd())
sys.path.append(os.path.join(last_path,'hbase_out'))
from hbase_outport import *

if __name__ == "__main__":
    m = Map()
    hbase_out = HbaseUtil()
    # hbase_out.scanTable('ship_historical_trace')
    res = hbase_out.scanfilter('ship_historical_trace', "SingleColumnValueFilter('info', 'mmsi', =, 'substring:100901881')")
    a = list()
    for i in res:
        a.append([float(i[3]),float(i[4])])
    m.draw_point(a)
    m.draw_line(a)