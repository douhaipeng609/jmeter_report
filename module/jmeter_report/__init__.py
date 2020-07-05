# -*- coding: utf-8 -*-
# @Time : 2020-03-17 12:56
# @Author : Hunk
# @File : __init__.py.py

from base.logger import *
from module.jmeter_report import jmeter_report_file
from module.jmeter_report import jmeter_report_htmlRewrite


Jmeter_report_file = jmeter_report_file.jmeter_report_file()
# jmeter_报告改写后的路径
HtmlRewrite = jmeter_report_htmlRewrite.html('/Users/dhp/Documents/j_NEW')
@logged
def html_structure(report_path) -> bool:

    if Jmeter_report_file.file_copy(report_path):
        if HtmlRewrite.html_Rewrite_start():
            LOGGER.info('报告改写成功')
            return True
        LOGGER.info('报告改写失败')
        return False
    LOGGER.error('报告复制失败')
    return False


if __name__ == '__main__':
    # 原jmeter_html报告地址
    print(html_structure('/Users/dhp/Documents/jmeter_re'))
