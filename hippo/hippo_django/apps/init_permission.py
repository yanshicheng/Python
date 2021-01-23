

from .auth.jwt_auth import analysis_token
import re
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from utils.NewResponse import api_response
from django.http import JsonResponse
class RbacMiddleware(MiddlewareMixin):
    """
    用户权限信息校验
    """

    def process_request(self, request):
        """
        当用户请求刚进入时候出发执行
        :param request:
        :return:
        """

        """
        1. 获取当前用户请求的URL
        2. 获取当前用户在session中保存的权限列表 ['/customer/list/','/customer/list/(?P<cid>\\d+)/']
        3. 权限信息匹配
        """

        current_url = request.path_info
        method = request.method
        # 白名单中的URL无需权限验证即可访问
        for valid_url in settings.VALID_URL_LIST:
            if re.match(valid_url, current_url):
                return None
        user_info = analysis_token(request)
        if 'admin' in user_info['user_info']['roles']:
            return None
        flag = False
        # item {'title': '权限查看', 'url': '/api/user/permissions', 'method': 'GET'}
        for item in user_info['permission']:
            reg = f"^{item['url']}$"
            if re.match(reg, current_url) and item['method'] == method:
                flag = True
                break
        if not flag:
            res = {
                'code': 990,
                'data': '无权限访问',
                'message': f'无权限访问. 请联系管理员获取URL:{current_url}, 请求方法: {method}'
            }
            return JsonResponse(res)
            # return JsonResponse(json.dumps(res))

