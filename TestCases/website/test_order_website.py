import unittest,json
from jsonpath import jsonpath
from Common.handle_log import logger
from Common.handle_requests import send_requests
from Common.handle_data import clear_EnvData_atts,EnvData,pwd_md5,replace_case_by_regular,replace_data
from Common.handle_config import conf
from Common.myddt import ddt,data
from Common.handle_excel import HandleExcel
from Common.handle_path import datas_dir

get_excel = HandleExcel(datas_dir+"\\overseas_datas.xlsx", "官网下单")
cases = get_excel.read_all_datas()
get_excel.close_file()
print(cases)

@ddt
class TestOrderWeb(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        logger.info("**********************************登录前置*********************************")
        clear_EnvData_atts()
        login_data = {"user_name": conf.get("data", "user_name"), "password": pwd_md5(conf.get("data", "password"))}
        resp = send_requests("POST", "/v1/webPay/login", login_data )
        setattr(EnvData, "access_token", jsonpath(resp.json(), "$..access_token")[0])  # 注意转换成字符串
        setattr(EnvData, "user_id", jsonpath(resp.json(), "$..user_id")[0])


    @classmethod
    def tearDown(cls) -> None:
        logger.info("*****************************下单用例结束******************************")

    @data(*cases)
    def test_order_web(self,case):
        logger.info("***************执行第{}条用例：{}*********************".format(case["case_id"], case["title"]))
        case = replace_case_by_regular(case)
        resp = send_requests(case["method"], case["url"], case["request_data"])  # Excel当中的请求数据读取出来是字符串，要转换成字典
        if case["expected"]:
            expected = eval(case["expected"])
            logger.info("用例的期望结果为：{}".format(expected))
        expected = eval(case["expected"])
        try:
            self.assertEqual(resp.json()["ret"], expected["ret"])
            self.assertEqual(resp.json()["msg"], expected["msg"])
        except AssertionError as e:
            logger.exception("断言失败!")
            raise e







