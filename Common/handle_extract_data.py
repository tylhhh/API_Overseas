import jsonpath
from Common.handle_data import EnvData, get_pw_url_data


def extract_data(extract_exprs,response_dict):
    """
    根据jsonpath提取表达式，从响应结果当中，提取数据并设置为环境变量EnvData类的类属性，作为全局变量使用。
    :param extract_exprs: 从excel当中读取出来的，提取表达式的字符串。
    :param response_dict: http请求之后的响应结果。
    :return:Nonoe
    """
    # 将提取表达式转换成字典
    extract_dict = eval(extract_exprs)
    # 遍历字典，key作为全局变量名，value是jsonpath提取表达式。
    for key,value in extract_dict.items():
        # 提取
        res = str(jsonpath.jsonpath(response_dict,value)[0])
        print(res)
        # 设置环境变量
        setattr(EnvData,key,res)

def extract_pw_data(response_data,extract_exprs):
    extract_dict = eval(extract_exprs)
    for key,value in extract_dict.items():
        # 提取
        res = str(jsonpath.jsonpath(get_pw_url_data(response_data),value)[0])
        print(res)
        # 设置环境变量
        setattr(EnvData,key,res)











