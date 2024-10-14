def from_str_to_datestr( datestr='1975年5月',ddate=True ):
    '''
    written by 方涛，20241014
    各类随机日期变换为标准的'1975-05-26'形式的字符串
    参数：
        datestr：字符串，如1975年5月，1975.5，19750526等
        ddate：月日采用双数输出，缺省为True
    返回：
        字符串：如'1975-05-26'
    '''
    import re
    tmp = datestr
    unistr = ''
    try:
        tmp = int(tmp)
        tmp = str(tmp)
        tmp_year = tmp[0:4]
        tmp_month = tmp[4:6]
        unistr = tmp_year + '-' + tmp_month
        if len(tmp) >6:
            ntial = min(len(tmp),8)
            tmp_day = tmp[6:ntial]
            unistr = unistr + '-' + tmp_day
        
    except:
        tmp = re.sub('[.年月]','-',tmp)
        tmp = re.sub(r"[日-]$", "", tmp)
        tmp = re.sub(" +", "", tmp)
        unistr = tmp
        
    if ddate == True:
        ## 处理需要双数显示的月日
        list_date = unistr.split('-')
        for j in range(len(list_date)):
            if len(list_date[j]) == 1:
                list_date[j] = '0' + list_date[j]
        unistr ='-'.join(list_date)

    return unistr
