import os
# import casbin
# import datetime
# # m = r.sub == p.sub && keyMatch(r.obj, p.obj) && regexMatch(r.act, p.act)
# print(datetime.datetime.utcnow() + datetime.timedelta(minutes=1))
# import re
# ret = re.match(r'.*','PUT')
# if ret:
#     print('成功')
# else:
#     print('失败')
#
# e = casbin.Enforcer("./basic_model.conf", "./basic_policy.csv")
#
# sub = 'zhangsan'
#
# obj = '/data2'
# act = 'PUT'
#
# if e.enforce(sub, obj, act):
#     # permit alice to read data1
#     print('OK')
# else:
#     # deny the request, show an error
#     print('NO')
#
#
#
# from casbin import persist
# class DjangoAdapter(persist.Adapter):
#     def __init__(self, adapter_model):
#         self.adapter_model = adapter_model
#     def load_policy(self, model):
#         for cr in self.adapter_model.objects.all():
#             print(cr)
#             values = [x for x in cr.serializer().values() if x]
#             print(values)
#             # 'p, xiaoming, /api/v1/user/info, GET'
#             persist.load_policy_line(', '.join(values), model)
#
#     def save_policy(self, model):
#         pass
#     def add_policy(self, sec, ptype, rule):
#          pass
#     def remove_policy(self, sec, ptype, rule):
#         pass
#     def remove_filtered_policy(self, sec, ptype, field_index, *field_values):
#          pass

import os
import casbin
from django.conf import settings
# def IsPermissionVerify(username, path, method):
#     adapter_rule = DjangoAdapter(CasbinRule)
#     model_conf_file = os.path.join(settings.BASE_DIR, "conf","rbac_model.conf")
#     print("model_conf_file", model_conf_file)
#     print(username, path, method)
#     e = casbin.Enforcer(model_conf_file, adapter=adapter_rule)
#     # e.add_function("keyMatchMethod", key_match_method_func)
#     return e.enforce(username, path, method)
import sys
# def setup():
#     BASEDIR = os.path.dirname(os.path.abspath(__file__))
#     sys.path.insert(0, BASEDIR)
#     sys.path.insert(0, os.path.abspath(os.path.join(BASEDIR, '..')))
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rbac.settings')
#     import django
#     django.setup()
# def logic():
#     from apps.models import CasbinRule, CasbinPermissions, CasbinRoles, CasbinUsers
#     adapter = DjangoAdapter(CasbinRule)
#     e = casbin.Enforcer("./basic_model.conf", adapter)
#     sub = 'lisi'
#     obj = '/test'
#     act = 'GET'
#     if e.enforce(sub, obj, act):
#         # permit alice to read data1
#         print('验证成功')
#     else:
#         # deny the request, show an error
#         print('NULL')
#     roles_list = []
#     for cr in CasbinPermissions.objects.all():
#         values = [x for x in cr.serializer().values() if x]
#         print(values)
#         print('-' * 120)
#         print(len(values[1]))
#         if len(values[1]) != 1:
#             for roles in values[1]:
#                 new_value = []
#                 new_value.append(values[0])
#                 new_value.append(roles)
#                 new_value.append(values[2])
#                 new_value.append(values[3])
#                 roles_list.append(new_value)
#                 print(new_value)
#         else:
#             values[1] =values[1][0]
#             roles_list.append(values)
#     print(roles_list)
# def main():
#     setup()
#     logic()
#
#
# if __name__ == '__main__':
#     main()





def setup():
    BASEDIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, BASEDIR)
    sys.path.insert(0, os.path.abspath(os.path.join(BASEDIR, '..')))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rbac.settings')
    import django
    django.setup()
def logic():
    from apps.models import UserInfo, CasbinRule, CasbinPermissions, CasbinRoles, CasbinUsers
    current_user = UserInfo.objects.filter(name='devops').first()
    print(current_user)
    # obj = current_user.roles.exclude(permissions__pid__gt=0).values("permissions__id",
    #                                                                                  "permissions__title",
    #                                                                                   "permissions__slug",)
    # print(obj)
    permission_queryset = current_user.roles.filter(permissions__isnull=False,permissions__pid__gt=0).values("permissions__id",
                                                                                     "permissions__title",
                                                                                      "permissions__slug",
                                                                                      "permissions__remarks",
                                                                                    )
    print(permission_queryset)
    print(len(permission_queryset))
    permission_dict = {}
    for item in permission_queryset:
        permission_dict[item['permissions__title']] = {
            'id': item['permissions__id'],
            'title': item['permissions__title'],
            'url': item['permissions__slug'],
            'method': item['permissions__remarks'],
        }
    print(permission_dict)
def main():
    setup()
    logic()


if __name__ == '__main__':
    main()