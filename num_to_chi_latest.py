def num_to_chi( num = '1234.56',is_mi = True ):
    '''
    主要用于金融财务方面，阿拉伯数字转换成中文大写，支持负号；
    最大值支持到垓；
    小数点仅支持2位。
    
    参数：
        num：用户输入要转换成中文大写的数字，可以是数字和字符串形式；如果是小数，四舍五入至2位；
        is_mi：在兆位使用万亿，与国家面向大众时的直白表达相一致，缺省为True。

    返回：
        字符串，中文大写
    
    '''
    import re
    #######################函数定义、字典定义######################################
    # 定义将千分位的数字转换成汉字大写
    def thousand_to_chi( num_or_str = '1234567890' ):
        thousand_to_chi = ''
        int_num = str( num_or_str )
        lenth = len( int_num )
        for i in range(len(int_num)):
            if int_num[i] == '0' :
                if thousand_to_chi[-1:] != '零':
                    thousand_to_chi = thousand_to_chi + dic_chi[int_num[i]] 
            else:
                thousand_to_chi = thousand_to_chi + dic_chi[int_num[i]] + dic_no[lenth-i] 
        # 末尾的零删除
        thousand_to_chi = thousand_to_chi if thousand_to_chi[-1:] != '零' else thousand_to_chi[:-1]
        return ( thousand_to_chi )
    # 定义字典
    dic_no = {1:'',2:'拾',3:'佰',4:'仟'}
    dic_unit = {1:'',2:'万',3:'亿',4:'兆',5:'垓'}
    dic_chi = {
            '0': '零', '1': '壹', '2': '贰', '3': '叁', '4': '肆',
            '5': '伍', '6': '陆', '7': '柒', '8': '捌', '9': '玖'
               }
    #############################################################################
    
    ### 参数部分 ###
    num = str( num )
    is_mi = is_mi
    ### 参数部分结束 ###

    #处理负号
    if num[0:1] == '-':
        is_minus = True
        num = num[1:]
    else:
        is_minus = False
    
    int_num,float_num = '',''
    try:
        int_num,float_num = num.split('.')
    except:
        int_num = num
        
    ## 1. 处理整数部分
    
    pattern = r'\d{1,4}'  # 匹配1到4个任意字符
    # 使用 re.findall 并反转字符串和结果列表
    result = re.findall(pattern, int_num[::-1])[::-1]  
    
    # 将每个分组反转
    result = [group[::-1] for group in result]  
    
    lenth = len( result )
    num_to_chi = ''
    for i in range( lenth ):
        ttc = thousand_to_chi( result[i] )
        if ttc == '':
            ttc = '零'
        else:
            ttc = ttc + dic_unit[ lenth - i ]
        num_to_chi = num_to_chi + ttc
    # 删除字符串开头可能的'零'
    re.sub('^零','',num_to_chi)
    
    ## 2. 处理小数部分
    lenth = len(float_num)
    if lenth == 0:
        num_to_chi = num_to_chi + '元整'
    else:
        float_num = '.' + float_num
        float_num = round( float(float_num),2 )
    
        float_num = str( float_num )
        float_num = float_num.split('.')[1]
        
        num_to_chi = num_to_chi + '元'
        
        ## 处理小数部分
        if float(float_num) == 0:
            num_to_chi = num_to_chi + '整'
        else:
            for i in range( len( float_num ) ):
                num_to_chi = num_to_chi + dic_chi[float_num[i]] + ('角' if i==0 else '分')
    # 删除字符串中间可能出现的无意义零，比如将壹兆伍仟亿零零元整 -> 壹兆伍仟亿元整
    num_to_chi = re.sub('[零]+元','元',num_to_chi)
    
    # 如果用万亿表示兆，则进行后而的处理；
    if is_mi == True:
        num_to_chi = re.sub('兆','万亿',num_to_chi)
        num_to_chi = re.sub('(.+)万亿(.+)亿',r'\1万\2亿',num_to_chi)

    # 处理负号问题
    if is_minus == True:
        num_to_chi = '负' + num_to_chi
    return ( num_to_chi )
