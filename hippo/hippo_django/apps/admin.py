from django.contrib import admin

# Register your models here.



from . import models

for table in models.__all__:
    admin.site.register(getattr(models,table))



from .models import CasbinRule
# 定义Admin
class CasbinRuleAdmin(admin.ModelAdmin):
    list_display = [
        'ptype',
        'v0',
        'v1',
        'v2',
        'v3',
        'v4',
        'v5',
     ]
    search_fields = ('v0', 'v1')
admin.site.register(CasbinRule, CasbinRuleAdmin)