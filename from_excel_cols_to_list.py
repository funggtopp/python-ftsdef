def from_excel_cols_to_list( mystr = 'ok' ):
    '''
    从excel中直接粘贴过来的列名转换成列表形式
    参数：
        mystr: 从excel中直接粘贴过来的列名。列名可能包含双引号和换行符等。
        举例：
        mystr = '''
                姓名	性别	出生年月	学历	"工作单位
                及职务"	入党时间	"党组织关系所在
                党支部及任职"	学会任职	联系方式	备注
                '''
    返回：
        列表list，列名。
    '''
    mystr = mystr
    mystr = mystr.replace('\n','')
    mystr = mystr.replace('\t',',')
    mystr = mystr.replace('"','')

    mystr = mystr.split(',')
    return mystr
