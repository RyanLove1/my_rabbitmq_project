# coding:utf-8
# 导入控制返回的JSON格式的类
from rest_framework.renderers import JSONRenderer
class customrenderer(JSONRenderer):
    # 重构render方法
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context:
            status_code=renderer_context.get('response').status_code
            status_text=renderer_context.get('response').status_text

            #修改code
            if status_code==200 or status_code==201:
                status_code=0
                status_text=u'请求成功'
            if status_code==401:
                status_text=u'您的登录信息已过期，请重新登录'

            if status_code==400 and "type_name" in data.keys() and data["type_name"][0] == "具有 物品类型 的 item type 已存在。":
                status_text = u'物品类型已存在!'

            if status_code==400 and "name" in data.keys() and data["name"][0] == "具有 商品名称 的 commodity 已存在。":
                status_text = u'商品已存在!'

            # 岳松阳的版本更新需要用到外层的code
            if isinstance(data, dict) and data.get('code')==1:
                status_code=1
            if isinstance(data, dict) and data.get('msg'):
                status_text = data.pop('msg')
            if isinstance(data, dict) and  data.get('code'):
                status_code = data.pop('code')
            #小程序要求
            if isinstance(data, dict) and  data.get('noregist'):
                status_code = 405

            # 重新构建返回的JSON字典
            ret = {
                'msg': status_text,
                'code': status_code,
                'data': data,
            }

            # 返回JSON数据
            return super().render(ret, accepted_media_type, renderer_context)
        else:
            return super().render(data, accepted_media_type, renderer_context)