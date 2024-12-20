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
