# -*- coding:utf-8 -*-

# from CCPRestSDK import REST
from .CCPRestSDK import REST  # 注意： 当前文件作为启动文件时，不能用 .pack_name来导包

# 说明：主账号，登陆云通讯网站后，可在"控制台-应用"中看到开发者主账号ACCOUNT SID
_accountSid = '8a216da8614f67d20161502e36c900d3'
# 8a216da863f8e6c20164139687e80c1b
# 说明：主账号Token，登陆云通讯网站后，可在控制台-应用中看到开发者主账号AUTH TOKEN
_accountToken = '170c9bafd1aa4d9fa8f9e087cde28af3'
# 6dd01b2b60104b3dbc88b2b74158bac6
# 请使用管理控制台首页的APPID或自己创建应用的APPID
_appId = '8a216da8614f67d20161502e372d00da'
# 8a216da863f8e6c20164139688400c21
# 说明：请求地址，生产环境配置成app.cloopen.com
_serverIP = 'sandboxapp.cloopen.com'

# 说明：请求端口 ，生产环境为8883
_serverPort = "8883"

# 说明：REST API版本号保持不变
_softVersion = '2013-12-26'

"""
# 云通讯官方提供的发送短信代码实例
# 发送模板短信
# @param to 手机号码
# @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
# @param $tempId 模板Id

def sendTemplateSMS(to, datas, tempId):
    # 初始化REST SDK
    rest = REST(serverIP, serverPort, softVersion)
    rest.setAccount(accountSid, accountToken)
    rest.setAppId(appId)

    result = rest.sendTemplateSMS(to, datas, tempId)
    for k, v in result.iteritems():

        if k == 'templateSMS':
            for k, s in v.iteritems():
                print '%s:%s' % (k, s)
        else:
            print '%s:%s' % (k, v)
"""


class CCP(object):
    """发送短信的辅助类，用单例实现"""

    def __new__(cls, *args, **kwargs):
        # hasattr(object, name)的作用是判断对象是否存在对应的属性
        if not hasattr(CCP, '_instance'):
            """判断是否存在类属性，_instance,_istance是类CCP唯一的对象，即单例 """
            cls._instance = super(CCP, cls).__new__(cls, *args, **kwargs)
            # cls._instance = object.__new__(cls, *args, **kwargs)

            # 初始化REST SDK
            cls._instance.rest = REST(_serverIP, _serverPort, _softVersion)
            cls._instance.rest.setAccount(_accountSid, _accountToken)
            cls._instance.rest.setAppId(_appId)

        return cls._instance

    def send_template_SMS(self, to, datas, tempId):
        """
        发送短信模板
        :param to:  手机号码
        :param datas: 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
                      其中 '12' 表示短信验证码， '34' 表示提醒用户验证码过期的时间
        :param tempId: 模板Id
        :return: 0 or -1
        """
        result = self.rest.sendTemplateSMS(to, datas, tempId)
        # 如果不明确sendTemplateSMS()返回的数据是什么，可以打印result看看
        # 如果云通讯发送短信成功，返回的字典数据中键：statusCode 的值为'000000'
        if result.get('statusCode') == '000000':
            # 表示短信发送成功
            return 0
        else:
            return -1


if __name__ == '__main__':
    ccp = CCP()
    # 测试的短信模板编号是 1
    result = ccp.send_template_SMS('18824125362', ['123456', 5], 1)
    print(result)
