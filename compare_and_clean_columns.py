def compare_and_clean_columns(df, col1, col2,show_info=True):
    """
    比较并清理DataFrame中的两列。
    列值向col1移动；如果col2为Nan或无差异，删除该列
    参数:
        df: 输入的DataFrame。
        col1: 第一列的名称。
        col2: 第二列的名称。

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
        if show_info:print(f'{col1}和{col2}两列无差异值，已删除{col2}列！')
    else:        
        if show_info:
            df_diff = df[ (df[col1] != df[col2]) & ~df[col2].isnull() ]
            print(f'{col1}和{col2}两列有差异值，共{df_diff.shape[0]}组数据受影响：')
            df_diff_cols = pd.DataFrame({col1:df_diff[col1],col2:df_diff[col2]})
            print(df_diff_cols)
    return df
