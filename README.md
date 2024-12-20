自编python函数，以py文件存在。<br>


## 转换相关 
- num_to_chi : 阿拉伯数字转财务用中文
- num_to_chi_latest ：阿拉伯数字转财务用中文大写，支持负号及小数，最大支持到垓，支持万亿写法
- from_excel_cols_to_list ：excel粘贴列名转换为列表
- from_str_to_list：将带分隔符的字符串转换为列表，from_str_to_list('今天,挺好的',sep=',')
- from_str_to_datestr：将随机的非标准日期字符串转换成标准"1975-05-26"字符串
- from_str_to_datestr_of_df：pandas DataFrame按列转换
## 数据清洗
- clean_merged_df：对刚完成merge合并的DataFrame进行列值对比，列值向左移动，并删除右侧多余列
- compare_and_clean_columns：对比DataFrame中指定的两列值，列值向左移动，并删除右侧多余列；有数值差异不删除
- def compare_and_swap_columns：两列比较，有差异，交换位置；无差异，右侧设为空；右列全为空，删除该列
## AI 相关
- ai_helper ：模拟deeplearning的helper，使用豆包API
## office
- excel_lookup：模拟excel的lookup操作
- read_excel_sheets：单元格内容出现断行且单独占用一行，用此函数将断行内容补充进上一单元格内容
