import os
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 测试用例路径
cases_dir = os.path.join(base_dir, "TestCases")
# 测试数据的路径
datas_dir = os.path.join(base_dir,"TestDatas")
# 测试报告
reports_dir = os.path.join(base_dir,"Outputs\\reports")
# 日志的路径
logs_dir = os.path.join(base_dir,"Outputs\\logs")
# 配置文件路径
conf_dir = os.path.join(base_dir,"Conf")
# 登录用例路径
login_dir = os.path.join(base_dir, "TestCases", "all_login")


