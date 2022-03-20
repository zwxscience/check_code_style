# This is a sample Python script.
import struct
import os
import re
# import numpy as np
import const
from log import Log
from deal_single_line import DealSingle

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def read_file(name):
    fileHandler = open(file_path, "r")
    # Get list of all lines in file
    listOfLines = fileHandler.readlines()
    # Close file
    fileHandler.close()
    return listOfLines


def deal_single_line(filename, listOflines):
    line_no = 1
    ds = DealSingle()
    for line in listOflines:
        ds.check_all(filename, line_no, line.replace('\n', '').replace('\r', ''))
        line_no += 1

def str_all_index( str_, a):
    '''
    Parameters
    ----------
    str_ : string.
    a : str_中的子串

    Returns
    -------
    index_list : list

    首先输入变量2个，输出list，然后中间构造每次find的起始位置start,start每次都在找到的索引+1，后面还得有终止循环的条件

    '''
    index_list = []
    start = 0
    while True:
        x = str_.find(a, start)
        if x > -1:
            start = x + 1
            index_list.append(x)
        else:
            break
    return index_list

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('start prepare some info')

    file_path = 'ivopts.c'
    const.list.append(file_path)
    # init log
    log = Log()
    if os.path.exists(os.path.join(os.getcwd(), const.log_name)):  # 如果文件存在
        os.remove(os.path.join(os.getcwd(), const.log_name))
    log.info('current file:' + file_path)
    if not os.path.exists(file_path): # check path is exist,print error if not
        print('path', file_path, ' does not exist')
    else:
        listOfLines = read_file(file_path)
        deal_single_line(os.path.basename(file_path), listOfLines)
        log.info('All data is processed！')