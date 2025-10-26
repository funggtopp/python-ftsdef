# 判断文件格式是否合规
def check_file_format(file_path,compare_str,compare_col=0):
    '''`
    检查Excel文件格式是否符合预期。
    1.如果有多个表，返回多表名；
    2.如果比较字符串没有包含在指定列[compare_col]的第一个单元格内，返回错误信息。
    此函数用来快速校对某文件格式是否符合预期，避免后续处理出错。

    参数：
        file_path: str，Excel文件路径
        compare_str: str，用于对比的字符串
        compare_col: int，指定列的索引，默认值为0（第一列）
    返回值：
        output_msgs: list，包含错误信息的列表，如果没有错误则为空列表
        df: pandas DataFrame，读取的Excel文件内容
    '''
    output_msgs = []
    # 先读取该文件所有sheet
    xls = pd.ExcelFile(file_path)
    if len(xls.sheet_names)>1:
        output_msgs.append(f"----Error:{file_path.split(os.sep)[-1]} 有多个sheet: {xls.sheet_names}，需手动确认...")

    df = pd.read_excel(file_path)
    if compare_str not in df.columns.values[compare_col]:
        output_msgs.append(f"----Error:{file_path.split(os.sep)[-1]} 似乎不是预期的格式，需手动确认...")
    if len(output_msgs)>0: output_msgs = ['\n'] + output_msgs + ['\n']
    return output_msgs,df

def count_people(sentence):
    '''
    解析句子中的人数信息，返回总人数
    该函数能够处理以下几种情况：
    1) "A班和B班各N人" 之类的结构
    2) "X班Y人"（班后直接跟人数）
    3) 剩余的 "N人"（纯数字或中文数字）
    参数：
        sentence: str，包含人数信息的句子
    返回值：
        total: int，总人数'''
    import re
    total = 0
    def chinese_to_int(s):
        if s.isdigit():
            return int(s)
        ch = {'零':0,'一':1,'二':2,'两':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9}
        if not s:
            return 0
        if '十' in s:
            parts = s.split('十')
            left = parts[0]
            right = parts[1] if len(parts) > 1 else ''
            val = 0
            if left == '':
                val += 10
            else:
                val += ch.get(left,0) * 10
            if right != '':
                val += ch.get(right,0)
            return val
        return ch.get(s, 0)
    # 1) 处理 “A班和B班各N人” 之类的结构
    pattern_each = re.compile(r'([一二三四五六七八九十\d]+班(?:[和、,，]?[一二三四五六七八九十\d]+班)*)各([一二三四五六七八九十\d]+)人')
    for m in pattern_each.finditer(sentence):
        classes_part = m.group(1)
        num_each = chinese_to_int(m.group(2))
        classes = re.findall(r'([一二三四五六七八九十\d]+)班', classes_part)
        total += len(classes) * num_each
    sentence = pattern_each.sub('', sentence)

    # 2) 处理 “X班Y人”（班后直接跟人数）
    pattern_class_num = re.compile(r'([一二三四五六七八九十\d]+)班([一二三四五六七八九十\d]+)人')
    for m in pattern_class_num.finditer(sentence):
        num = chinese_to_int(m.group(2))
        total += num
    sentence = pattern_class_num.sub('', sentence)

    # 3) 处理剩余的 “N人”（纯数字或中文数字）
    pattern_num = re.compile(r'([一二三四五六七八九十\d]+)人')
    for m in pattern_num.finditer(sentence):
        total += chinese_to_int(m.group(1))

    return total

def sum_cols_with_re(df,start_col,end_col,excel_file_name):
    '''
    对 df 中从 start_col 到 end_col 的列进行求和，返回求和结果列表
    处理过程中如果遇到无法直接求和的情况，尝试用 count_people 进行处理
    例如：某些单元格中可能包含“3班各40人”之类的文本，需要解析后计算总人数
    该函数返回一个列表，包含每一列的求和结果
    参数：
        df: pandas DataFrame，包含需要求和的数据
        start_col: str，起始列名
        end_col: str，结束列名
        excel_file_name: str，当前处理的Excel文件名，用于错误提示
    返回值：
        sum_values: list，包含每一列的求和结果

    '''

    tmp_df = df.loc[:,start_col:end_col]
    try:
        sum_values = list(tmp_df.agg('sum').values)
    except:
        print(f"\n\n---Review:{excel_file_name} 未普查数据求和失败，更换方式再次求和，请注意手工核对...\n\n")        
        sum_values = []
        for col in tmp_df.columns:
            try:
                col_sum = pd.to_numeric(tmp_df[col]).sum()
            except:
                col_sum = 0
                for idx in tmp_df.index:
                    tmp = tmp_df.at[idx, col]
                    try:
                        col_sum += tmp
                    except:
                        col_sum += count_people(tmp)
                    
            sum_values.append(col_sum)
    return sum_values

def sum_list(alist):
    '''
    对一个列表进行求和，返回一个列表
    如果列表中包含无法求和的元素，则将这些元素保留在结果列表中
    例如：输入 [10, 20, '无数据', 30]，返回 [60, '无数据']
    参数：
        alist: list，包含需要求和的元素
    返回值：
        result: list，包含求和结果和无法求和的元素，如果无内容则返回空列表
    '''
    total = 0
    a = []
    for item in alist:
        try:
            total += int(item)
        except:
            item = item.strip().replace('无','')
            if item != '': a.append(item)
    if total == 0 and len(a)>0:
        return a
    elif total >0 and len(a)==0:
        return [total]
    elif total >0 and len(a)>0:
        return [total]+a
    else:
        return []

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
    返回：
        处理完成的DataFrame；
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

###--
def compare_and_clean_columns(df, col1, col2,show_info=True):
    """
    比较并清理DataFrame中的两列。
    列值向col1移动；如果col2为Nan或无差异，删除该列
    参数:
        df: 输入的DataFrame。
        col1: 第一列的名称。
        col2: 第二列的名称。
        show_info：显示差异值，默认显示

    返回:
        清理后的DataFrame。
    """
    if col1 not in df.columns or col2 not in df.columns:
        print("指定的列名不存在于DataFrame中。")
        return df

    # 1. 比较两列值，相同则将 col2 设为 NaN，不同则保持原值 (这一步没有问题)
    df[col2] = np.where(df[col1] == df[col2], np.nan, df[col2])

    # 2. 只有当 col1 为 NaN 时，才将 col2 的值移到 col1 (这是关键的修改)
    df[col1] = np.where(df[col1].isnull(), df[col2], df[col1])  # 使用 np.where 进行条件赋值
    df[col2]=np.where(df[col1]==df[col2], np.nan, df[col2])

    # 3. 如果 col2 列全为 NaN，则删除该列
    if df[col2].isnull().all():
        df = df.drop(columns=col2)
        if show_info:print(f'{col2}列已全为空值，删除！')
    else:        
        if show_info:
            df_diff = df[ (df[col1] != df[col2]) & ~df[col2].isnull() ]
            print(f'{col1}和{col2}两列有差异值，共{df_diff.shape[0]}组数据受影响：')
            df_diff_cols = pd.DataFrame({col1:df_diff[col1],col2:df_diff[col2]})
            print(df_diff_cols)
    return df

###--
def clean_merged_df(df):
    """
    清理merge合并后的 DataFrame (后缀分别_x和_y)
    对_X列和_y列进行清理，列值向_x移动；如果_y列无差异，删除该列
    
    参数:
        df: 刚完成merge合并后的 DataFrame

    返回:
        清理后的 DataFrame
    """
    
    # 1. 比较 _x 和 _y 列，相同则将 _y 设为 NaN
    for col in df.columns:
        if col.endswith('_x'):
            col_y = col[:-2] + '_y'
            if col_y in df.columns:
                df[col_y] = np.where(df[col] == df[col_y], np.nan, df[col_y])
    
    # 2. 如果只有一列有数据，将数据移到 _x 列
    for col in df.columns:
        if col.endswith('_x'):
            col_y = col[:-2] + '_y'
            if col_y in df.columns:
                df[col] = df[col].fillna(df[col_y])
                df[col_y] = np.where(df[col]==df[col_y], np.nan, df[col_y])
                
    
    # 3. 删除 _y 列，并重命名列
    cols_to_drop = []
    for col in df.columns:
        if col.endswith('_y'):
          if df[col].isnull().all():
            cols_to_drop.append(col)
            original_col=col[:-2]
            if original_col+'_x' in df.columns:
              df=df.rename(columns={original_col+'_x': original_col})
    
    df = df.drop(columns=cols_to_drop)

    return df

###--
def compare_and_swap_columns(df, col1, col2,show_info=True):
    """
    比较并交换DataFrame中的两列位置。
    相同列值保留col1值，col2设为Nan；非相同值交换位置；如果col2为Nan或无差异，删除该列
    参数:
        df: 输入的DataFrame。
        col1: 第一列的名称。
        col2: 第二列的名称。
        show_info：显示差异值，默认显示

    返回:
        清理后的DataFrame。
    """
    if col1 == col2:
        print('两列名字相同，不进行任何操作返回！')
        return None
    if col1 not in df.columns or col2 not in df.columns:
        print("指定的列名不存在于DataFrame中。")
        return None

    # 直接在原DataFrame上操作
    mask = df[col1] == df[col2]

    # 将相同值的col2设置为NaN
    df.loc[mask, col2] = np.nan

    # 交换非相同值的位置
    mask = (df[col1] != df[col2]) & ~df[col2].isnull()
    df.loc[mask, [col1, col2]] = df.loc[mask, [col2, col1]].values

    #处理col2为Nan或无差异的情况
    if df[col2].isnull().all() or (df[col1] == df[col2]).all():
        df = df.drop(columns=col2)
        if show_info:print(f"{col2}列已删除，因为它所有值均为NaN或与{col1}无差异。")
        if col1.endswith('_x') or col1.endswith('_y'):
            df = df.rename( columns = {col1:col1[:-2]} )
    return df

###--
def to_concat_df_broken_lines(df,cols=[],index_col_name='序号'):
    '''
    断行合并
    DataFrame中某一列中的值出现了断行的情况；断行的值向上合并
    
    特别注意：
        index_col_name索引列必须存在，且断行时为空

    参数：
        df：需要处理的DataFrame
        cols：出现断行情况的列名，数组形式，如['项目名称']
        index_col_name，缺省='序号'，索引列名

    返回：
        处理完成的DataFrame
    '''
    mask = df[df[index_col_name].isnull()].index
    for combine_col in cols:
        for index in mask[::-1]:
            df.loc[index-1,combine_col] += df.loc[index,combine_col]
    df = df.drop(mask)
    return df