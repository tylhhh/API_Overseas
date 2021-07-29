import hashlib, time, datetime, json
from urllib.parse import quote
import re
from Common.handle_config import conf
from Common.handle_log import logger
from jsonpath import jsonpath


class EnvData:
    pass


def clear_EnvData_atts():
    values = dict(EnvData.__dict__)
    for key, value in values.items():
        if key.startswith("__"):
            pass
        else:
            delattr(EnvData, key)


def md5(str):
    str_md5 = hashlib.md5(str.encode(encoding='UTF-8')).hexdigest()
    return str_md5


def pwd_md5(str):
    return md5(str + md5(str))


def replace_by_regular(data):
    res = re.findall("#(.*?)#", data)
    if res:
        for item in res:
            try:
                value = conf.get("data", item)
            except:
                try:
                    value = getattr(EnvData, item)
                except AttributeError:
                    continue
            data = data.replace("#{}#".format(item), str(value))
    return data


def replace_case_by_regular(case):
    for key, value in case.items():
        if value is not None and isinstance(value, str):  # 确保是个字符串
            case[key] = replace_by_regular(value)
    logger.info("正则表达式替换完成之后的请求数据：\n{}".format(case))
    return case


def replace_data(case, mark, real_data):
    for key, value in case.items():
        if value is not None and isinstance(value, str):
            if value.find(mark) != -1:
                case[key] = value.replace(mark, real_data)
    return case


def get_pw_sign(request_data):
    str_parm = ''  # 目标md5串
    data_dict = eval(request_data)
    list_data = sorted(data_dict)
    for item in list_data:  # 将字典中的key排序,存在在列表中
        if item == "sig":
            list_data.remove("sig")
    for item in list_data:  # 列表去掉sig后，再进行遍历
        str_parm = str_parm + str(item) + "=" + str(data_dict[item])  # 转换成字符串拼接key-value值
    private_key = 'ddf9bd6428e62c519db32f416852ff3c'  # paymentwall回调固定的
    str_parm = str_parm + private_key
    sig = md5(str_parm)
    return sig


def get_mol_sign(request_data):
    str_parm = ''  # 目标md5串
    data_dict = eval(request_data)
    list_data = sorted(data_dict)
    for item in list_data:  # 将字典中的key排序,存在在列表中
        if item == "signature":
            list_data.remove("signature")
    for item in list_data:  # 列表去掉signature后，再进行遍历,拼接参数字典中的value值
        str_parm = str_parm + str(data_dict[item])
    secret_key = '6HHT8uQ3V0ZK8ozmvedeTY9uhDaXUsNv'  # mol回调固定的
    str_parm = str_parm + secret_key
    print(str_parm)
    signature = md5(str_parm)
    print(signature)
    return signature


def get_login_sign(request_data):
    str_parm = ""
    data_dict = eval(request_data)
    list_data = sorted(data_dict)
    for item in list_data:
        if item == "sign":
            list_data.remove("sign")
    for item in list_data:
        json_data = json.dumps(data_dict[item], ensure_ascii=False, separators=(',', ':'))
        str_parm = str_parm + str(item) + "=" + str(json_data) + "&" # 字典转换成功json字符串后，拼接key-value值
    pay_sign = conf.get("data", "pay_sign")  # 对应云打包平台里包id为100000052的pay_sign
    str_parm = str_parm + pay_sign
    print(str_parm)
    sign = md5(str_parm)
    print(sign)
    return sign


def get_order_sign(request_data):
    str_parm = ""
    data_dict = eval(request_data)
    list_data = sorted(data_dict)
    for item in list_data:
        if item == "sign":
            list_data.remove("sign")
    for item in list_data:
        json_data = json.dumps(data_dict[item], ensure_ascii=False, separators=(',', ':'))
        if isinstance(json_data,str):
            json_data = quote(json_data)  # url编码
        str_parm = str_parm + str(item) + "=" + str(json_data) + "&"  # value值进行url编码后再进行字典key-value拼接
    app_secret = conf.get("data", "app_secret")  # 对应云打包里包id为100000052的game_union_secret
    str_parm = str_parm + app_secret
    print(str_parm)
    sign = md5(str_parm)
    print(sign)
    return sign


def get_mol_paymentId():
    return "MPO" + str(round(time.time()))


def get_paymentStatusDate():
    return datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')


def get_pw_url_data(response_data):
    res = jsonpath(response_data, '$..url')[0]
    data_list = []
    for item in res.split("&"):  # 分割成列表
        dict_data = {}
        for i in item:
            dict_data[item.split("=")[0]] = item.split("=")[1]
        data_list.append(dict_data)
    return data_list


def get_second_sign(request_data):
    data_dict = eval(request_data)
    sign_str = "{}={}".format("authorize_code", data_dict["authorize_code"]) + "&" \
               + "{}={}".format("jh_app_id", data_dict["jh_app_id"]) + "&" \
               + "{}={}".format("jh_sign", conf.get("data", "app_secret")) + "&" \
               + "{}={}".format("time", data_dict["time"])
    print(sign_str)
    second_sign = md5(sign_str)
    print(second_sign)
    return second_sign



