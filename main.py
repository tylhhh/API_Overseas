import unittest
from BeautifulReport import BeautifulReport
from Common.handle_path import cases_dir,reports_dir

s = unittest.TestLoader().discover(cases_dir)

br = BeautifulReport(s)
br.report("海外接口自动化测试报告","report_html",reports_dir)