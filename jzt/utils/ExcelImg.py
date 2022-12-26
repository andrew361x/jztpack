# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 09:57:27 2018

@author: LT004
"""

import sys
import os
import xlrd
import zipfile
import base64
import shutil

class jztProReportPicture:
    """图片保存在[myfile]_pics的文件夹中"""
    
    def __init__(self,file_path=None,file_name =None):
        self.file_path = file_path
        self.file_name = file_name
        self.zipfileName = self.file_name.replace(".xlsx",".zip")
        self.foldname  = self.file_name.replace(".xlsx","")

    def change_file_name(self):
        """
        修改指定目录下的文件类型名
        :param file_path:
        :param old:
        :param new:
        :return:
        """
        fullpath = os.path.join(self.file_path,self.file_name)
        if not os.path.exists(fullpath):
            print('No such File! :%s' % fullpath)
            return False

        if os.path.exists(self.zipfileName):
            os.remove(self.zipfileName)
        #os.rename(old_path, new_path)
        shutil.copyfile(fullpath,os.path.join(self.file_path,self.zipfileName))      #复制文件

    def unzip_file(self):
        """
        解压缩指定目录下的Zip文件
        :param file_path:
        :return:
        """
        #file_list = os.listdir(file_path)
        #for file_name in file_list:
        print("file_path>>>",self.file_path)
        print("zip_filename>>>",self.zipfileName)
        file_zip = zipfile.ZipFile(os.path.join(self.file_path, self.zipfileName), 'r')
        print("zipdir>>>",self.foldname)
        for files in file_zip.namelist():
            file_zip.extract(files, os.path.join(self.file_path, self.foldname))  # 解压到指定文件目录
        file_zip.close()

    def unzip_excel_pic2base64(self):
        """
        解压缩的excel目录下获取图片并转成base64编码
        :param file_path:
        :param file_name:
        :return:
        """
        pic_dir = 'xl\media'
        pic_path = os.path.join(self.file_path, self.foldname, pic_dir)
        print("pic_path>>>",pic_path)
        if not os.path.exists(pic_path):
            print ('No such directory!:%s' % pic_path)
            return "Nothing"
        file_list = os.listdir(pic_path)
        new_path = os.path.join(self.file_path, self.foldname+"_pics")
        if os.path.exists(new_path):
            shutil.rmtree(new_path)
        os.mkdir(new_path)
        try:
            for files in file_list:
                if files.endswith('.png'):
                    path = os.path.join(pic_path, files)
                    print("pic_path>",path," ::: newpath>",self.file_path+"\\"+files)
                    shutil.copyfile(path,new_path+"\\"+files)
                    #return staionReport().img2base64(path) # 转成base64方法
            print("copying done!")
        except Exception as exc:
            print ('unzip_excel_pic2base64 Error!',exc)
            return "Error"
        
        
    def clear(self):
        shutil.rmtree(self.foldname)
        os.remove(self.zipfileName)


    def excel_pic_read(self):
            """
            读取excel中的图片base64
            :param file_path:
            :param file_name:
            :return:图片的base64编码字符串
            """
            self.change_file_name() 
            self.unzip_file( ) 
            return self.unzip_excel_pic2base64( )