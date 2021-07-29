import unittest,time
from Common.handle_log import logger
from Common.handle_requests import send_requests
from Common.handle_data import clear_EnvData_atts,replace_case_by_regular,replace_data,get_login_sign,get_order_sign,get_second_sign,get_pw_sign
from Common.myddt import ddt,data
from Common.handle_excel import HandleExcel
from Common.handle_path import datas_dir
from Common.handle_extract_data import extract_data,extract_pw_data

get_excel = HandleExcel(datas_dir+"\\overseas_datas.xlsx", "sdk下单")
cases = get_excel.read_all_datas()
get_excel.close_file()

@ddt
class TestSdkOrder(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        logger.info("**********************************SDK下单用例开始执行*********************************")
        clear_EnvData_atts()

    @data(*cases)
    def test_sdk_order(self,case):
        logger.info("***************执行第{}条用例：{}*********************".format(case["case_id"], case["title"]))
        replace_case_by_regular(case)
        if case["request_data"].find("#login_sign#") != -1:
            case = replace_data(case, "#login_sign#", get_login_sign((case["request_data"])))
        if case["request_data"].find("#time#") != -1:
            case = replace_data(case, "#time#", str(round(time.time())))
        if case["request_data"].find("#jh_sign#") != -1:
            case = replace_data(case, "#jh_sign#", get_second_sign(case["request_data"]))
        if case["request_data"].find("#order_sign#") != -1:
            case = replace_data(case, "#order_sign#",get_order_sign(case["request_data"]))
        resp = send_requests(case["method"], case["url"], case["request_data"])
        if case["extract_data"]:
            extract_data(case["extract_data"], resp.json())
        if case["expected"]:
            expected = eval(case["expected"])
            logger.info("用例的期望结果为：{}".format(expected))
            try:
                self.assertEqual(resp.json()["ret"], expected["ret"])
                self.assertEqual(resp.json()["msg"], expected["msg"])
            except AssertionError as e:
                logger.exception("断言失败!")
                raise e







