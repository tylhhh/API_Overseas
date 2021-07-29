
import unittest

from Common.handle_requests import send_requests
from Common.handle_log import logger
from Common.handle_config import conf
from Common.handle_data import pwd_md5

class TestWebLogin(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        logger.info("*****************************登录用例开始********************************")

    @classmethod
    def tearDown(self) -> None:
        logger.info("*****************************登录用例结束********************************")

    def test_web_login(self):
        login_url= "/v1/webPay/login"
        login_data = {"user_name": conf.get("data", "user_name"), "password": pwd_md5(conf.get("data", "password"))}
        resp = send_requests("POST", login_url, login_data)
        try:
            self.assertEqual(resp.json()["ret"], 1)
            self.assertEqual(resp.json()["msg"],'success')
        except AttributeError as e:
            logger.exception("断言失败")
            raise e




