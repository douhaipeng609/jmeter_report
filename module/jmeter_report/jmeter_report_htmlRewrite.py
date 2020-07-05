# -*- coding: utf-8 -*-
# @Time : 2020-03-17 13:00
# @Author : Hunk
# @File : jmeter_report_htmlRewrite.py
import os
import shutil
import re

from bs4 import BeautifulSoup
from base.logger import *


class html:
    @logged
    def __init__(self, html_path):
        self.index_path = '{}{}'.format(html_path, '/templates/index.html')
        CustomsGraphs_path = '{}{}'.format(
            html_path, '/static/content/pages/CustomsGraphs.html')
        OverTime_path = '{}{}'.format(
            html_path, '/static/content/pages/OverTime.html')
        ResponseTimes_path = '{}{}'.format(
            html_path, '/static/content/pages/ResponseTimes.html')
        Throughput_path = '{}{}'.format(
            html_path, '/static/content/pages/Throughput.html')
        self.static_path = [
            CustomsGraphs_path,
            OverTime_path,
            ResponseTimes_path,
            Throughput_path]

    @logged
    def html_Rewrite(self, path, Label, Rawrite_type, attribute='') -> bool:
        """
               重写HTML方法
               :param path: html路径
               :param Label: 标签
               :param Rawrite_type: 方法类型0方法1，1方法2
               :param attribute: 方法1时候是属性，方法2时候是要修改的字符串
               :return: 修改成功返回True,修改失败返回False
               """
        try:
            with open(path, 'r', encoding='utf-8') as file:
                html = file.read()
                bs = BeautifulSoup(html, "html.parser")
                if Rawrite_type == 0:
                    label_list = bs.findAll(Label)
                    b_list = []
                    i = 0
                    for label in label_list:
                        b_list.append(
                            "{}{}{}".format(
                                "{{ url_for('static', path='", label[attribute], "') }}"))
                        label[attribute] = b_list[i]
                        i += 1
                    with open(path, 'w') as fp:
                        fp.write(bs.prettify())
                        i = -1
                        label_list_check = bs.findAll(Label)
                        for label_check in label_list_check:
                            i += 1
                            if label_check[attribute] == b_list[i]:
                                LOGGER.info('方法1修改成功')
                                return True

                            else:
                                LOGGER.error('方法1修改失败')
                                return False
                elif Rawrite_type == 1:
                    label_list = bs.findAll(href=re.compile(Label))
                    for label in label_list:
                        label['href'] = attribute
                        continue
                    with open(path, 'w') as fp:
                        fp.write(bs.prettify())
                        label_list_check = bs.findAll(
                            href=re.compile(attribute))
                        for label_check in label_list_check:
                            if label_check['href'] == attribute:
                                LOGGER.info('方法2修改成功')
                                return True
                            else:
                                LOGGER.error('方法2修改失败')
                                return False

                else:
                    LOGGER.error('方法不存在')
                    return False
        except Exception as e:
            LOGGER.error('操作异常：%s' % e)
            return False

    @logged
    def html_Rewrite_start(self):
        if self.html_Rewrite(
            self.index_path,
            'script',
            0,
            'src') and self.html_Rewrite(
            self.index_path,
            'a',
            0,
            'href') and self.html_Rewrite(
            self.index_path,
            'link',
            0,
                'href'):
            if self.html_Rewrite(
                self.index_path,
                'index.html',
                1,
                    'jmeter_report'):
                LOGGER.info('跟地址重写成功')
                i_list = []
                for i in self.static_path:
                    if self.html_Rewrite(i, 'index.html', 1, '/jmeter_report'):
                        i_list.append(i)
                        LOGGER.info('static目录重写成功')
                    else:
                        LOGGER.info('static目录重写失败')
                        return False
                if set(i_list).issuperset(self.static_path):
                    LOGGER.info('全部重写成功')
                    return True
                else:
                    LOGGER.error('最后一点点失败了')
                    return True

            else:
                LOGGER.error('跟地址重写失败')
                return False
        else:
            LOGGER.error('标签重写失败')
            return False


if __name__ == '__main__':
    j = html('/Users/dhp/Documents/j_NEW')
    print(j.html_Rewrite_start())
