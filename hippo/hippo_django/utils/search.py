from django.db.models import Q

'''
模糊查询
'''

def SearchFunc(queryset , field_list ,search_content, op='OR'):
        q = Q()
        q.connector = op
        for field in field_list:
            q.children.append(Q((f'{field}__icontains', search_content )))
        query_set = queryset.filter(q)
        return query_set


