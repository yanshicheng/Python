from django.conf import settings
import jwt
import datetime
def create_token(payload):
    salt = settings.SECRET_KEY
    exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.JWT_TIMEOUT)
    # 构造 header
    headers = {
        'typ': 'jwt',
        'alp': 'HS256'
    }

    payload['exp'] = exp
    return jwt.encode(payload=payload, key=salt, algorithm='HS256', headers=headers).decode('utf-8')
def analysis_token(request):
    '''
    :param request:
    :return:
    '''
    authorization = request.META.get('HTTP_AUTHORIZATION', '')
    auth = authorization.split()
    salt = settings.SECRET_KEY
    payload = jwt.decode(auth[1], salt, True)
    if payload:
        return payload
    else:
        return False
