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
