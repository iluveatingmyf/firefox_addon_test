import glob
import sys
import xlrd

'''
0:id, 1:name, 2:developer, 3:desp, 4：cate，
5：star，6：comment，7：user，8：url，9：war， 10：msg， 
11：http， 12 Dsplong， 13：Dspcn， 14：Suptlang，
'''

def cal_percentage(rlist):
    one = rlist.count(1)
    return one/len(rlist)

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

def coverage(id_list, war, msg, http):
    wf = '0'
    mf='0'
    hf='0'
    result = {
        '000':[],
        '001':[],
        '010':[],
        '011':[],
        '100':[],
        '101':[],
        '110':[],
        '111':[]
    }
    '''
     0=000, 没有任何指纹
     1=001 ,只有http指纹
     2=010,只有msg指纹
     3=011，只有http和msg指纹
     4=100, 只有war
     5= 101, 
    '''
    length = len(war)
    for count in range(1,length):
        if len(war[count])>1:
            wf = '1'
        if len(msg[count])>1:
            mf = '1'
        if len(http[count])>1:
            hf ='1'
        flag = wf+mf+hf
        result[flag].append(count)
        wf = '0'
        mf = '0'
        hf = '0'
    #print(length)
    return result

def table_sta(msg_statistics,http_statistics, index_dict,id_list, war, msg, http):
    mlist=msg[1:]
    hlist=[]
    x_index = http[1:]
    x_result = []
    for temp in x_index:
        reverse_list = process_string(temp)
        filter = []
        for item in reverse_list:
            if item not in filter:
                filter.append(item)
        # 经过内部去重、排序的独立指纹
        filtered = sorted(filter, key=lambda i: len(i), reverse=True)
        hlist.append(filtered)




    #010的情况—— 只有msg的情况
    zoz_index = index_dict['010']
    zoz_result = []
    for entry in zoz_index:
        temp = msg[entry]
        for item in msg_statistics.keys():
            if temp == item:
                #print(temp)
                count = msg_statistics[temp]
                zoz_result.append(count)
    #print(cal_percentage(zoz_result))

    #001的情况——只有http的情况
    zzo_index = index_dict['001']
    zzo_result = []
    for entry in zzo_index:
        temp2 = http[entry]
        reverse_list = process_string(temp2)
        filter = []
        for item in reverse_list:
            if item not in filter:
                filter.append(item)
        # 经过内部去重、排序的独立指纹
        filtered = sorted(filter, key=lambda i: len(i), reverse=True)
        #print(filtered)
        for item in http_statistics.values():
            if filtered == item['fingerprint']:
                zzo_result.append(item['count'])
    #print(cal_percentage(zzo_result))

    # 101的情况——有http和war时，http的识别率
    ozo_index = index_dict['101']
    ozo_result = []
    for entry in ozo_index:
        temp3 = http[entry]
        _reverse_list = process_string(temp3)
        filter = []
        for item in _reverse_list:
            if item not in filter:
                filter.append(item)
        # 经过内部去重、排序的独立指纹
        _filtered = sorted(filter, key=lambda i: len(i), reverse=True)
        # print(filtered)
        for item in http_statistics.values():
            if _filtered == item['fingerprint']:
                ozo_result.append(item['count'])
    #print(len(ozo_result))
    #print(cal_percentage(ozo_result))

    # 110的情况——有msg和war时，msg的识别率
    ooz_index = index_dict['110']
    ooz_result = []
    for entry in ooz_index:
        temp4 = msg[entry]
        for item in msg_statistics.keys():
            if temp4 == item:
                count = msg_statistics[temp4]
                ooz_result.append(count)
    #print(len(ooz_result))
    #print(cal_percentage(ooz_result))

    # 011的情况——有http和msg时，http的识别率
    zoo_index = index_dict['011']
    zoo_result = []
    _zoo_result = []
    msg_list = []
    http_list = []
    for entry in zoo_index:
        temp5 = http[entry]

        _temp5 = msg[entry]
        msg_list.append(_temp5)

        _reverse_list_ = process_string(temp5)
        filter = []
        for item in _reverse_list_:
            if item not in filter:
                filter.append(item)
        # 经过内部去重、排序的独立指纹
        _filtered_ = sorted(filter, key=lambda i: len(i), reverse=True)
        http_list.append(_filtered_)
        for item in http_statistics.values():
            if _filtered_ == item['fingerprint']:
                zoo_result.append(item['count'])

        for item in msg_statistics.keys():
            if _temp5 == item:
                count = msg_statistics[_temp5]
                _zoo_result.append(count)
    final_one = combine_mh(msg_list, http_list)

    # 111的情况——
    ooo_index = index_dict['111']
    ooo_result = []
    _ooo_result = []
    msg_l= []
    http_l = []
    for entry in ooo_index:
        temp6 = http[entry]
        _temp6 = msg[entry]
        msg_l.append(_temp6)

        _reverse_list_ = process_string(temp6)
        filter = []
        for item in _reverse_list_:
            if item not in filter:
                filter.append(item)
        # 经过内部去重、排序的独立指纹
        _filtered_ = sorted(filter, key=lambda i: len(i), reverse=True)
        http_l.append(_filtered_)
        for item in http_statistics.values():
            if _filtered_ == item['fingerprint']:
                ooo_result.append(item['count'])


        for item in msg_statistics.keys():
            if _temp6 == item:
                count = msg_statistics[_temp6]
                _ooo_result.append(count)
    final_two = combine_mh(msg_l, http_l)
    final_end = final_one + final_two
    #cal_uniq_mh(final_one,final_end)




def cal_uniq_mh(final_one,final):
    result = []
    print(len(final_one))
    for item in final_one:
        count = final.count(item)
        result.append(count)
        if count>1:
            print(item)
    print(result)
    print(cal_percentage(result))

def combine_mh(msg_list, http_list):
    final = []
    for i in range(len(msg_list)):
        tup = [msg_list[i]]
        for item in http_list[i]:
            tup.append(item)
        final.append(tup)
    return final












def combine_msg_to_http(name, msg_list, http_list):
    length = len(name)
    result = []
    for i in range(length):
        p_msg = msg_list[i]
        temp_http = process_string(http_list[i])
        filter = []
        for item in temp_http:
            if item not in filter:
                filter.append(item)
        p_http = sorted(filter, key=lambda i: len(i), reverse=True)
        combine = [p_msg,p_http]
        result.append(combine)
    return result

def return_combine_result(name, result, msg_list, http_list):
    length = len(name)
    final = {}

    test= []

    for i in range(length):
        p_msg = msg_list[i]
        temp_http = process_string(http_list[i])
        filter = []
        for item in temp_http:
            if item not in filter:
                filter.append(item)
        p_http = sorted(filter, key=lambda i: len(i), reverse=True)
        combine =[p_msg, p_http]
        final[name[i]]= {'count':result.count(combine), 'fingerprint':combine}
        test.append(result.count(combine))
    print(set(test))
    return final





def process_string(str_list):
    result = []
    if str_list[0] == '[' and len(str_list)>1:
        origin = str_list[1:-1]
        for item in origin.split(','):
            result.append(item[1:-1])
    else:
        result.append(str_list)
    return result

def cal_msg(msg_list):
    #列表去重
    result = {}
    msg_unique_list = list(set(msg_list))
    unique_len = len(msg_unique_list)
    for item in msg_unique_list:
        count = msg_list.count(item)
        result[item]= count
    #print('The count of unique :', unique_len)
    #print(result)
    return result


def cal_http(http_list):
    result = {}
    final = []
    origin = []
    for item_list in http_list[1:]:
        #每个指纹的初始数组
        reverse_list = process_string(item_list)
        filter = []
        for item in reverse_list:
            if item not in filter:
                filter.append(item)
        #经过内部去重、排序的独立指纹
        filtered = sorted(filter, key=lambda i: len(i), reverse=True)
        #origin没有经过外部整体去重的指纹集合
        origin.append(filtered)
        #final是经过去重的整体指纹集合
        if filtered not in final:
            final.append(filtered)
    index = 0
    for entry in final:
        count = origin.count(entry)
        result[index]={'count':count, 'fingerprint':entry}
        index += 1
    print(result)
    print('The count of unique:', len(result),len(final),len(origin))
    return result


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
        book = xlrd.open_workbook('./Data/allmeta222.xlsx')
        sheet = book.sheet_by_index(0)
        rows = sheet.nrows
        row = sheet.row_values(1)

        msg_statistics = cal_msg(sheet.col_values(10))
        http_statistics = cal_http(sheet.col_values(11))
        coverage_sta = coverage(sheet.col_values(0),sheet.col_values(9), sheet.col_values(10), sheet.col_values(11))
        table_sta(msg_statistics,http_statistics, coverage_sta, sheet.col_values(0),sheet.col_values(9), sheet.col_values(10), sheet.col_values(11))
        for key in coverage_sta.keys():
            count = len(coverage_sta[key])
            print(key , ':', count)


        #print(http_statistics)
        #combine_statistics = combine_msg_to_http(sheet.col_values(1),sheet.col_values(10),sheet.col_values(11))
        #c_result = return_combine_result(sheet.col_values(1),combine_statistics,sheet.col_values(10),sheet.col_values(11))
        #print(c_result)


       # print(msg_statistics)
        #print(http_statistics)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
