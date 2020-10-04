"""

"""

import argparse
import os
from os.path import isdir
import re
import shutil

parser = argparse.ArgumentParser(
    add_help=True, description="消除（转移）使用Typora等软件时未在文件夹中引用的资源")

parser.add_argument("file", help="指定需要清除的MARKDOWN文件。", type=str)
parser.add_argument("-d", "--dir", help="执行需要清除的目录")
parser.add_argument("-m", "--move", action="store_true",
                    help="当加入此选项之后，将不会删除多余的元素，而是将其转移到新的文件夹中")

args = parser.parse_args()

"""
查找文件目录
"""

print("文件路径：{0}".format(args.file))

img_dir = None
if args.dir is not None:
    img_dir = args.dir
else:
    img_dir = ".".join(args.file.split(".")[:-1]) + ".assets"
print("文件夹路径：{0}".format(img_dir))

if os.path.exists(img_dir) is not True or os.path.isdir(img_dir) is not True:
    print("请检查文件夹路径是否错误")
    exit(-1)

# 收集所有存在的文件名
all_set = set()
for _, _, filelist in os.walk(img_dir):
    all_set = set(filelist)
    break
print("目录中共存在 {0} 个文件".format(len(all_set)))

# 集合
has_set = set()

# 正则
pat = "(!\\[(.*?)\\]\\((.*?)\\))"
pat = re.compile(pat)

# 收集出现过的文件名
with open(args.file, "r", encoding="utf-8") as file:
    for line in file.readlines():
        for pat_str in pat.findall(line):
            has_set.add(os.path.basename(pat_str[2]))

# 求两个集合的差集，差集均为未采用的文件
dif = all_set.difference(has_set)
print("将对目录中的 {0} 个文件进行 {1} ".format(len(dif), "转移" if args.move else "删除"))

if args.move:
    # 转移未采用的文件
    dist_dir = ".".join(args.file.split(".")[:-1]) + ".bad"
    print("正在转移下面的文件到{0}".format(dist_dir))
    if os.path.exists(dist_dir) == False or os.path.isdir(dist_dir) == False:
        os.mkdir(dist_dir)
    for t in dif:
        print(os.path.join(img_dir, t), end="...")
        shutil.move(os.path.join(img_dir, t), os.path.join(dist_dir, t))
        print("OK")
else:
    # 删除未采用的文件
    print("正在删除下面的文件")
    for t in dif:
        print(os.path.join(img_dir, t), end="...")
        os.remove(os.path.join(img_dir, t))
        print("OK")

print("执行成功")
