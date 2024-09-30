def num_to_chi( num = '1234.12' ):
    '''
    阿拉伯数字转为中文金融用大写；仅支持到999万亿以下。
    输入：
        num：字符串或数字，内容必须为 1234.23 的数字形式。整数或小数均可。
    输出：
        num_to_chi：壹仟贰佰叁拾肆元贰角叁分

    '''
    num = str( num )
    int_num,float_num = num.split('.')
    
    dic_unit = {1:'',2:'拾',3:'佰',4:'仟',5:'万',6:'拾',7:'佰', 8:'仟', 9:'亿',
                10:'拾',11:'佰',12:'仟',13:'万',14:'拾',15:'佰',16:'仟'
               }
    dic_chi = {
            '0': '零', '1': '壹', '2': '贰', '3': '叁', '4': '肆',
            '5': '伍', '6': '陆', '7': '柒', '8': '捌', '9': '玖'
                }
    ## 处理整数部分
    lenth = len(int_num)
    num_to_chi = ''
    for i in range(lenth):
        if int_num[i] == '0' :
            if num_to_chi[-1:] != '零':
                num_to_chi = num_to_chi + dic_chi[int_num[i]] 
            if dic_unit[lenth-i] in ['万','亿']:
                num_to_chi = num_to_chi[:-1] + dic_unit[lenth-i]
                if num_to_chi[-2:-1] in ['亿']:
                    #pass
                    num_to_chi = num_to_chi[:-1]+'零'
        else:
            num_to_chi = num_to_chi + dic_chi[int_num[i]] + dic_unit[lenth-i] 
    
    
    lenth = len(float_num)
    if lenth == 0:
        num_to_chi = num_to_chi + '元整'
    else:
        num_to_chi = num_to_chi + '元'
        if lenth <2 :
            float_num = float_num + '00'
        float_num = float_num[:2]
        ## 处理小数部分
        if float(float_num) == 0:
            num_to_chi = num_to_chi + '整'
        else:
            num_to_chi = num_to_chi + dic_chi[float_num[0]] + '角' + dic_chi[float_num[1]] + '分'
    
    return ( num_to_chi )

