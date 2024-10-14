def from_str_to_datestr_of_df( df = [],col_name='日期',ddate=True ):
    '''
    written by 方涛，20241014
    本函数主要是为应对数据采集表中报送过来的日期格式不统一的问题
    如2024年5月，2024-5，2024-05-3，202405等。
    仅支持df的单列统一
    
    参数：
        df：Pandas DataFrame
        col_name：需要进行统一格式的日期列名，不支持列表
        ddate：月和日是否强制使用2位，缺省为True

    返回：
        已进行日期统一的Pandas DataFrame
    '''
    def from_str_to_datestr( datestr='1975年5月',ddate=True ):
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
        
    import re
    df = df.copy()
    
    if len(df) == 0:
        return 'Error，df无数据!'

    df[col_name] = df[col_name].astype('str')
    loc_index = df[ (df[ col_name ] != 'None') & (df[ col_name ] != '') ].index
    
    for i in loc_index:
        
        df.loc[i,col_name] = from_str_to_datestr(df.loc[i,col_name],ddate)
            
    return df
