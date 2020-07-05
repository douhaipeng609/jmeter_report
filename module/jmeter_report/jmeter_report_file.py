# -*- coding: utf-8 -*-
# @Time : 2020-03-17 12:58
# @Author : Hunk
# @File : jmeter_report_file.py

import os
import shutil

from base.logger import *


class jmeter_report_file:
    """将报告路径复制到指定文件夹的方法，并按照渲染规则进行分配
    """
    @logged
    def __init__(self):
        self.files_standard = {
            'index.html',
            'content',
            'statistics.json',
            'sbadmin2-1.0.7'}
        self.path_report = '/Users/dhp/Documents/j_NEW'
        self.path_report_templates = '{}{}'.format(
            self.path_report, '/templates')
        self.path_report_static = '{}{}'.format(self.path_report, '/static')

    @logged
    def file_copy(self,path) -> bool:
        if self.files_standard.issubset(set(os.listdir(path))):
            try:
                if os.path.exists(self.path_report):
                    shutil.rmtree(self.path_report)
                    os.mkdir(self.path_report)
                    self.copy_path(path)
                else:
                    self.copy_path(path)
                return True
            except Exception as e:
                LOGGER.info('拷贝文件失败：%s' % e)
                return False
        else:
            LOGGER.error('缺失必要文件：%s' % os.listdir(path))
            LOGGER.info(self.files_standard)
            return False

    @logged
    def copy_path(self,path) -> bool:
        try:
            os.mkdir(self.path_report_templates)
            # os.mkdir(self.path_report_static)
            shutil.copy(
                '{}{}'.format(
                    path,
                    '/index.html'),
                self.path_report_templates)
            shutil.copy(
                '{}{}'.format(
                    path,
                    '/statistics.json'),
                self.path_report_templates)
            # shutil.copyfile(self.path,'', self.path_report_static)
            if not os.path.exists(self.path_report_static):
                shutil.copytree(path, self.path_report_static)
                os.remove(
                    '{}{}'.format(
                        self.path_report_static,
                        '/index.html'))
                os.remove(
                    '{}{}'.format(
                        self.path_report_static,
                        '/statistics.json'))
            LOGGER.info('拷贝路径成功')
            return True
        except Exception as e:
            LOGGER.error('操作异常：%s' %e)


            return False


if __name__ == '__main__':
    j = jmeter_report_file()
    j.file_copy('/Users/dhp/Documents/jmeter_re')
