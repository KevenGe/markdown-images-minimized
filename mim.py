"""

"""

import argparse
import os
from os.path import isdir
import re

parser = argparse.ArgumentParser(
    add_help=True, description="消除（转移）使用Typora等软件时未在文件夹中引用的资源")

parser.add_argument("file", help="指定需要清除的MARKDOWN文件。", type=str)
parser.add_argument("-d", "--dir", help="执行需要清除的目录")

args = parser.parse_args()

"""
查找文件目录
"""

img_dir= None
if args.dir is not None:
    img_dir = args.dir
else:
    img_dir = ".".join(args.file.split(".")[:-1]) +".assets"
print("文件夹路径：{0}".format(img_dir))

if os.path.exists(img_dir) is not True or os.path.isdir(img_dir) is not True:
    print("请检查文件夹路径是否错误")
    exit(-1)

# 收集所有存在的文件名
all_set = set()
for _,_,filelist in os.walk(img_dir):
    all_set = set(filelist)
    break

# 集合
has_set = set()

# 正则
pat = "(!\\[(.*?)\\]\\((.*?)\\))"
pat = re.compile(pat)

# 收集出现过的文件名
with open(args.file, "r", encoding="utf-8") as file:
    for line in file.readlines():
        for pat_str in pat.findall(line):
            print(os.path.basename(pat_str[2]))
            has_set.add(os.path.basename(pat_str[2]))

# 求两个集合的差集，差集均为未采用的文件
dif = all_set.difference(has_set)

# 删除未采用的文件
for t in dif:
    print(os.path.join(img_dir, t))
    os.remove(os.path.join(img_dir, t))
