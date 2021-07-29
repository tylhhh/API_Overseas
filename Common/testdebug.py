import hashlib, json, time, datetime
from urllib.parse import quote
from Common.handle_config import conf
import time


def md5(str):
    str_md5 = hashlib.md5(str.encode(encoding='UTF-8')).hexdigest()
    return str_md5


def get_test_sign(request_data):
    str_parm = ""
    data_dict = eval(request_data)
    list_data = sorted(data_dict)
    for item in list_data:
        if item == "sign":
            list_data.remove("sign")
    for item in list_data:
        json_data = json.dumps(data_dict[item], ensure_ascii=False, separators=(',', ':'))
        if isinstance(json_data, str):
            json_data = quote(json_data)
        str_parm = str_parm + str(item) + "=" + str(json_data) + "&"
    pay_sign = conf.get("data", "pay_sign")
    str_parm = str_parm + pay_sign
    print(str_parm)
    pw_sig = md5(str_parm)
    print(pw_sig)
    return pw_sig


def get_sign(dic_json):
    pay_sign = "47e8e216-764b-4fcb-9d4d-0e2c49fc895e"
    json_data = dict(sorted(dic_json.items()))
    sign_str = ""
    if json_data["sign"]:
        del json_data["sign"]
    for key, value in json_data.items():
        if isinstance(json_data[key], dict) or isinstance(json_data[key], list):
            value = json.dumps(json_data[key], ensure_ascii=False, separators=(',', ':'))  # separators参数的作用是去掉,,:后面的空格
            if isinstance(value, str):
                value = quote(value)
        else:
            value = str(json_data[key])
            if isinstance(value, str):
                value = quote(value)
        sign_str = sign_str + "{}={}".format(key, value) + "&"

    sign_str = sign_str + pay_sign
    print(sign_str)
    sign = md5(sign_str)
    print(sign)
    return sign


def get_pw_sign(request_data):
    str_parm = ''  # 目标md5串
    data_dict = eval(request_data)
    list_data = sorted(data_dict)
    print(list_data)
    for item in list_data:  # 将字典中的key排序,存在在列表中
        if item == "sig":
            list_data.remove("sig")
    for item in list_data:  # 列表去掉sig后，再进行遍历
        str_parm = str_parm + str(item) + "=" + str(data_dict[item])
    app_key = 'ddf9bd6428e62c519db32f416852ff3c'
    str_parm = str_parm + app_key
    print(str_parm)
    sig = md5(str_parm)
    print(sig)
    return sig


if __name__ == '__main__':
    parm = {
        'uid': '3276112',
        'goodsid': 'com.indie.jyjs.ft99yb60',
        'slength': '',
        'speriod': '',
        'type': '0',
        'sign_version': 'v2',
        'order_sn': '2020080534628710356',
        'revenue_payment_local': '99',
        'currency_code': 'USD',
        'sig': '1245454'
    }
    parm1 = json.dumps(parm)
    get_pw_sign(parm1)
