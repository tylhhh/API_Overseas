
import requests
from Common.handle_config import conf
from Common.handle_log import logger



def send_requests(method, url, data=None):
    headers = {"Content-Type": "application/json;charset=UTF-8"}
    url = pre_url(url)
    data = pre_data(data)
    logger.info("请求头为：{}".format(headers))
    logger.info("请求方法为：{}".format(method))
    logger.info("请求url为：{}".format(url))
    logger.info("请求数据为：{}".format(data))
    method = method.upper()
    if method == "GET":
        resp = requests.get(url, params=data,headers= headers)
    elif method == "POST":
        resp = requests.post(url, json=data,headers= headers)
    logger.info("响应状态码：{}".format(resp.status_code))
    logger.info("响应数据为：{}".format(resp.text))
    return resp



def pre_url(url):
    base_url = conf.get("server", "base_url")
    if url.startswith("/"):
        return base_url + url
    else:
        return base_url + "/" + url


def pre_data(data):
    """
    如果data是字符串，则转换成字典对象
    :param data:
    :return:
    """
    if data is not None and isinstance(data, str):
        if data.find("null") != -1:
            data = data.replace("null","none")
        data = eval(data)
    return data



if __name__ == '__main__':
    data = {'user_name': 1002809223, 'password': '82790085228cf8a1e3bac41f45271e5f'}
    send_requests("post", "/v1/webPay/login", data)