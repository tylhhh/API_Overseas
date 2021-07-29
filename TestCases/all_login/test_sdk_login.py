import unittest,json
from Common.handle_log import logger
from Common.handle_requests import send_requests
from Common.handle_data import clear_EnvData_atts,replace_case_by_regular,replace_data,get_login_sign
from Common.myddt import ddt,data
from Common.handle_excel import HandleExcel
from Common.handle_path import datas_dir

get_excel = HandleExcel(datas_dir+"\\overseas_datas.xlsx", "sdk登录")
cases = get_excel.read_all_datas()
get_excel.close_file()

@ddt
class TestSdkLogin(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        logger.info("**********************************SDK登录用例开始执行*********************************")
        clear_EnvData_atts()

    @data(*cases)
    def test_sdk_login(self,case):
        logger.info("***************执行第{}条用例：{}*********************".format(case["case_id"], case["title"]))
        replace_case_by_regular(case)
        if case["request_data"].find("#sign#") != -1:
            case = replace_data(case, "#sign#",get_login_sign(case["request_data"]))
        resp = send_requests(case["method"], case["url"], case["request_data"])  # Excel当中的请求数据读取出来是字符串，要转换成字典
        if case["expected"]:
            expected = eval(case["expected"])
            logger.info("用例的期望结果为：{}".format(expected))
            try:
                self.assertEqual(resp.json()["ret"], expected["ret"])
                self.assertEqual(resp.json()["msg"], expected["msg"])
            except AssertionError as e:
                logger.exception("断言失败!")
                raise e







