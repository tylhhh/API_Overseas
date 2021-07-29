import unittest,json
from jsonpath import jsonpath
from Common.handle_log import logger
from Common.handle_requests import send_requests
from Common.handle_data import clear_EnvData_atts,pwd_md5,replace_case_by_regular,replace_data,get_pw_sign,get_mol_paymentId,get_paymentStatusDate,get_mol_sign
from Common.handle_config import conf
from Common.myddt import ddt,data
from Common.handle_excel import HandleExcel
from Common.handle_path import datas_dir
from Common.handle_extract_data import extract_data,extract_pw_data

get_excel = HandleExcel(datas_dir+"\\overseas_datas.xlsx", "mol回调")
cases = get_excel.read_all_datas()
get_excel.close_file()


@ddt
class TestMolRecall(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        logger.info("**********************************mol回调开始*********************************")
        clear_EnvData_atts()

    @data(*cases)
    def test_mol_recall(self,case):
        logger.info("***************执行第{}条用例：{}*********************".format(case["case_id"], case["title"]))

        if case["request_data"].find("#password#") != -1:
            case = replace_data(case,"#password#", pwd_md5(conf.get("data", "password")))
        replace_case_by_regular(case)
        if case["request_data"].find("#paymentId#") != -1:
            case = replace_data(case, "#paymentId#", get_mol_paymentId())
        if case["request_data"].find("#paymentStatusDate#") != -1:
            case = replace_data(case, "#paymentStatusDate#", get_paymentStatusDate())
        if case["request_data"].find("#signature#") != -1:
            case = replace_data(case, "#signature#", get_mol_sign(case["request_data"]))
        resp = send_requests(case["method"], case["url"], case["request_data"])  # Excel当中的请求数据读取出来是字符串，要转换成字典
        if case["extract_data"]:
            extract_data(case["extract_data"],resp.json())

        if case["expected"]:
            expected = eval(case["expected"])
            logger.info("用例的期望结果为：{}".format(expected))
            try:
                self.assertTrue(resp.text)
            except AssertionError as e:
                logger.exception("断言失败!")
                raise e







