import unittest,json
from jsonpath import jsonpath
from Common.handle_log import logger
from Common.handle_requests import send_requests
from Common.handle_data import clear_EnvData_atts,EnvData,pwd_md5,replace_case_by_regular,replace_data,get_pw_sign
from Common.handle_config import conf
from Common.myddt import ddt,data
from Common.handle_excel import HandleExcel
from Common.handle_path import datas_dir
from Common.handle_extract_data import extract_data,extract_pw_data

get_excel = HandleExcel(datas_dir+"\\overseas_datas.xlsx", "pw回调")
cases = get_excel.read_all_datas()
get_excel.close_file()


@ddt
class TestPwRecall(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        logger.info("**********************************paymentwall回调开始*********************************")
        clear_EnvData_atts()

    @data(*cases)
    def test_pw_recall(self,case):
        logger.info("***************执行第{}条用例：{}*********************".format(case["case_id"], case["title"]))
        if case["request_data"].find("#password#") != -1:
            case = replace_data(case,"#password#", pwd_md5(conf.get("data", "password")))
        case = replace_case_by_regular(case)
        if case["request_data"].find("#sig#") != -1:
            case = replace_data(case, "#sig#", get_pw_sign(case["request_data"]))
        resp = send_requests(case["method"], case["url"], case["request_data"])  # Excel当中的请求数据读取出来是字符串，要转换成字典
        if case["extract_data"]:
            if case["extract_data"].find("order_sn") != -1:
                extract_pw_data(resp.json(), case["extract_data"])
            else:
                extract_data(case["extract_data"],resp.json())

        if case["expected"]:
            expected = eval(case["expected"])
            logger.info("用例的期望结果为：{}".format(expected))
            expected = eval(case["expected"])
            try:
                self.assertEqual(resp.text, expected["result"])
            except AssertionError as e:
                logger.exception("断言失败!")
                raise e







