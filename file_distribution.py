#!/usr/bin/env python
# coding: utf-8

# In[51]:


# %load file_distribution.py
# ——————————————————将一个文件夹中文件分到指定数量不同文件夹——————————————————————

import os
import math
import shutil

path = '.\\2019\\' # 原始文件路径
folderPath = '.\\2019\\'   # 输出文件路径

number = 6 # 每包文件数量
file_list = os.listdir(path)  # 源文件名称列表
Number = math.ceil(len(file_list) / number)  # 目标文件夹数量
folderNumber = -1  # 起始文件夹id ，-1是因为0 % 任意数 = 0
sort_folder_number = [x for x in range(1, Number+1)]
# print(sort_folder_number)

#  创建文件夹
for foldernumber in sort_folder_number:
    new_folder_path = os.path.join(folderPath, '%s' % foldernumber)  # new_folder_path is ‘folderPath\number'
    path1=new_folder_path+'\\'+'1'
    path2=new_folder_path+'\\'+'2'
    path3=new_folder_path+'\\'+'3'
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
    if not os.path.exists(path1):
        os.makedirs(path1)
    if not os.path.exists(path2):
        os.makedirs(path2)
    if not os.path.exists(path3):
        os.makedirs(path3)
    
# 分包
for i in range(0, len(file_list)):
    old_file = os.path.join(path, file_list[i])
    if os.path.isdir(old_file):
        '''if the path is a folder,program will pass it'''
        print('img does not exist ,path=' + old_file + ' it is a dir')
        pass
    elif not os.path.exists(old_file):
        '''if the path does not exist,program will pass it'''
        print('img does not exist ,path=' + old_file)
        pass
    else:
        '''define the number,it decides how many imgs each people process'''
        if (0 == (i % number)):  # 导致folderNumber = -1 ： 0 % 任意数 = 0
            folderNumber += 1
        if(file_list[i].split('.')[2] == 'h23v05'):
            new_file_path = os.path.join(folderPath,str(sort_folder_number[folderNumber]),
                                         str(1),file_list[i])
        if(file_list[i].split('.')[2] == 'h24v05'):
            new_file_path = os.path.join(folderPath,str(sort_folder_number[folderNumber]),
                                         str(1),file_list[i])
        if(file_list[i].split('.')[2]=='h25v05'):
            new_file_path = os.path.join(folderPath,str(sort_folder_number[folderNumber]),
                                         str(2),file_list[i])
        if(file_list[i].split('.')[2]=='h26v05'):
            new_file_path = os.path.join(folderPath,str(sort_folder_number[folderNumber]),
                                         str(2),file_list[i])
        if(file_list[i].split('.')[2]=='h25v06'):
            new_file_path = os.path.join(folderPath,str(sort_folder_number[folderNumber]),
                                         str(3),file_list[i])
        if(file_list[i].split('.')[2]=='h26v06'):
            new_file_path = os.path.join(folderPath,str(sort_folder_number[folderNumber]),
                                         str(3),file_list[i])
        if not os.path.exists(new_file_path):
            shutil.move(old_file, new_file_path)
print('Finish!')
