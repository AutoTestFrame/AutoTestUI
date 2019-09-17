# -*- coding: utf-8 -*-

import unittest
import json
import hashlib
from tools.read_excel import Excel
from interface.api_obj import HttpClientTest


def md5(data):
    """md5加密方法"""
    string = json.dumps(data)
    m = hashlib.md5()
    m.update(string.encode(encoding='utf-8'))
    return m.hexdigest()


def is_json_contain(result, expect, errmsg=''):
    """验证接口测试用例结果
    result={
        "code":"000"
        "name":"admin"，
        "info":{"id":"1"，"phone":"12345645789"}}
    expect={"name":"admin"}
    """
    if not isinstance(result, dict):
        errmsg += '实际结果不是字典格式'
        return False, errmsg
    if not isinstance(expect, dict):
        errmsg += '预期结果不是字典格式'
        return False, errmsg
    for key, value in expect.items():
        if key not in result:
            errmsg += '实际结果中未找到{}这个key'.format(key)
            return False, errmsg
        elif isinstance(result[key], dict) and isinstance(expect[key], dict):
            print('111')
            re = is_json_contain(result[key], expect[key])
            if re is not True:
                return re
        elif expect[key] != result[key]:
            print('222')
            errmsg += '{0}的预期结果是{1}，而实际结果是{2}'.format(key, expect[key], result[key])
            return False, errmsg

    return True, errmsg


class ApiTestCase(unittest.TestCase, HttpClientTest):
    excel_path = r'D:\PythonCode\AutoTestUI\interface\interface.xls'
    data_list = Excel(excel_path).read_excel(1)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testcase(self):
        '''
        数据驱动：（1000个接口用例。是不是写1000个以test开头的方法）
        先读取excel数据，每一行代表一条用例，
        这个方法一次执行所有的用例，将测试执行结果写入excel
        生产测试报告，
        :return:
        '''
        for datas in self.data_list:
            url = datas['url']
            name = datas["接口名"]
            methond = datas['请求方法']
            data = datas['入参']
            result = datas['断言']
            extract= datas['提取变量']
            if methond == 'get':
                self.request(url + name, methond, json.loads(data))
            elif methond == 'post':
                self.request(url + name, methond, data.encode('utf-8'))

    def request(self, url, methond, data=None, result=None, extract=None):
        res = HttpClientTest(url=url, methond=methond, data=data).run()
        print('响应结果:',methond,type(res),res)   #打印每一个用例的响应值
        # print(type(result),result)          #每个用例的断言
        # result = json.loads(result)
        # re = is_json_contain(res, result)
        # print(re)
        # if extract:
        #     d = {extract: res[extract]}
        #     ReadYaml().write_yaml(d)
        # self.assertTrue(re[0])
        # print(re[1])


if __name__ == '__main__':
    unittest.main()
