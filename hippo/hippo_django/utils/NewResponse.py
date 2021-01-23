from rest_framework.response import Response

def api_response(data='successful', code=200, **kwargs):
    result = {
        'code': code,
        'data': data,
    }
    result.update(**kwargs)
    return Response(result)