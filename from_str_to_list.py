def from_str_to_list( mystr = 'ok',sep=','):
    '''
    written by 方涛，20241013
    
    从excel或粘贴板中直接粘贴过来的字符串，带分隔符（只支持，和空格）的转换成列表形式

    换行符、英文引号 均作删除处理，空格不作为分隔符时也删除
    
    参数：
        mystr: 可能包含双引号和换行符等。
        举例：mystr = <三引号>
                姓名	性别	出生年月	学历	"工作单位
                及职务"	入党时间	"党组织关系所在
                党支部及任职"	学会任职	联系方式	备注
                <三引号>
        sep：分隔符(,或空格)，缺省为英文逗号；
             同时缺省制表符 \t 为分隔符。

    返回：
        列表list
    '''
    import re
    if sep == ',':
        mystr = re.sub('[  　\n"]','',mystr)
        mystr = re.sub('[\t+,+，+]',',',mystr)
        mystr = re.sub(',+',',',mystr)
    if sep == ' ' or sep == '　':
        mystr = re.sub('[\n"]','',mystr)
        mystr = re.sub('[\t+ +　+]',',',mystr)
        mystr = re.sub(',+',',',mystr)
    mystr = mystr.split(',')
    return mystr
