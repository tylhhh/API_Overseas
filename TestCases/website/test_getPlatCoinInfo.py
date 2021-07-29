import unittest
from jsonpath import jsonpath
from Common.handle_log import logger
from Common.handle_requests import send_requests
from Common.handle_data import clear_EnvData_atts,EnvData,pwd_md5
from Common.handle_config import conf

class TestGetPlatCoinInfo(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        logger.info("**********************************登录前置*********************************")
        clear_EnvData_atts()
        login_data = {"user_name": conf.get("data", "user_name"), "password": pwd_md5(conf.get("data", "password"))}
        resp = send_requests("POST", "/v1/webPay/login", login_data )
        setattr(EnvData, "access_token", jsonpath(resp.json(), "$..access_token")[0])


    @classmethod
    def tearDown(self) -> None:
        logger.info("*****************************获取钱包配置信息用例结束******************************")

    def test_getcoininfo(self):
        logger.info("*****************************获取钱包配置信息用例开始******************************")
        coininfo_url = "/v1/webPay/getPlatCoinInfo"
        coininfo_data = {"region_code": "zh-tw", "area_name": "HK", "access_token":EnvData.access_token}
        resp = send_requests("POST", coininfo_url, coininfo_data)
        try:
            self.assertEqual(resp.json()["ret"], 1)
            self.assertEqual(resp.json()["msg"], '获取平台币信息成功')
        except AttributeError as e:
            logger.exception("断言失败")
            raise e







