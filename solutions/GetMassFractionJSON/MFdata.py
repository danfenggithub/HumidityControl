import json
import re
import numpy as np

# 批量计算由 https://www.buildenvi.com/gongju/psychrometrics 提供
#
# 1.生成所需文件T_RH.txt 温度范围：[-60，60] 湿度范围：[0,100]
# with open("T_RH.txt", 'w', encoding="utf-8") as file:
#     for t in range(-60, 61):
#         for rh in range(0, 101):
#             file.write(str(t) + ',' + str(rh) + '\n')

# 2.在 https://www.buildenvi.com/gongju/psychrometrics 生成自己需要范围的数据,直接复制"结果输出（部分）"到T_RH_MF.txt

# 3.把table格式转换为复合的json数据格式
# path = "T_RH_MF.txt"
# # 读取文件
# with open(path, 'r', encoding="utf-8") as file:
#     # 定义一个用于切割字符串的正则
#     seq = re.compile("\t")
#     next(file)
#     result = []
#     # 逐行读取
#     itemin = "{"
#     itemout = "{"
#     i = 0
#     for line in file:
#         lst = seq.split(line)
#
#         itemin = itemin + "\"" + lst[1] + "\"" + ":" + lst[2] + ","
#         # print(itemin)
#         if i == 100:
#             itemin = itemin.rstrip(",")
#             itemin = itemin + "}"
#             itemout = itemout + "\"" + lst[0] + "\"" + ":" + itemin + ","
#             itemin = "{"
#             i = -1
#
#         i = i + 1
#     itemout = itemout.rstrip(",")
#     itemout = itemout + "}"
#
# # 关闭文件
# with open('MFdata.json', 'w') as dump_f:
#     # json.dump(result, dump_f)
#     dump_f.write(str(itemout))



# # Reading data back
# with open('MFdata.json', 'r') as f:
#     data = json.load(f)
#     print(data['25']['40'])


