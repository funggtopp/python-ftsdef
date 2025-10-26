def read_excel_sheets_for_No_NaN(file_name='',sheet_name='',skip=[0,0],to_str_column=[],to_concat_column=[],index_col_name='序号'):
    '''
    主要用于excel表格中出现断行且断行单独占用单元格的情况；主要表现为：断行占用两个或多个垂直单元格；断行单元格相邻单元格为NaN。
    特别注意：
        索引列在有断行情况时应为NaN；否则，本函数无效！！！
        必须有索引列；默认为'序号'；否则，函数出错！！！
    主要参数：
        file_name：缺省=''，文件名；
        sheet_name：缺省=''，文件内表名；
        skip：缺省=[0,0]，文件首尾跳过行数；有合并单元格式的表头时，一般为[1,0]；有末尾汇总行时，一般为[0,1]；
        to_str_column：缺省=[],读取时转换为字符串的列，如['序号','立项年度']；
        to_concat_column：缺省=[],需要处理的有断行问题的列，如['项目名称']；
        index_col_name：缺省='序号'，索引列，此列在有断行情况时应为NaN；否则，本函数无效；
    '''
    dtype={}
    for item in to_str_column:
        dtype[item]=str
    df = pd.read_excel(file_name,sheet_name=sheet_name,skiprows=skip[0],skipfooter=skip[1],dtype=dtype)
    for index in df[ df.loc[:,index_col_name].isnull()].index:
        for item in to_concat_column:
            df.loc[index-1,item] = df.loc[index-1,item] + df.loc[index,item]
    df = df.drop(df[df[index_col_name].isnull()].index)
    df[index_col_name] = df[index_col_name].astype('int')
    df = df.set_index(index_col_name,drop=True)
    return df
