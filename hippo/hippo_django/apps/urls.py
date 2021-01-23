from django.contrib import admin
from django.urls import path, re_path, include
from .views.department import Department
from .views import userinfo
from .views import roles
urlpatterns = [
    path('department', Department.as_view({
        'get': 'list',
        'post': 'create',
    })),
    path('department/<int:pk>', Department.as_view({
        'delete': 'destroy',
        'put': 'update',
    })),

    path('login', userinfo.JwtLogin.as_view(),name='login'),
    path('logout', userinfo.JwtLogout.as_view(),name='logout'),
    path('set-password', userinfo.SetPassword.as_view(),name='set-password'),
    path('reset-password', userinfo.ResetPassword.as_view(),name='reset-password'),
    path('userinfo', userinfo.JwtUserInfo.as_view({"get": "list"}),name='userinfo'),
    path('userinfo/<int:pk>', userinfo.JwtUserInfo.as_view({
        "put": "update",
    }),name='userinfo'),

    path('management', userinfo.UserManagement.as_view({
        "get": "list",
        'post': 'create',
    }), name='userinfo'),
    path('management/<int:pk>', userinfo.UserManagement.as_view({
        "put": "update",
        'delete': 'destroy',
        'get': 'details'
    }), name='management'),
    path('permissions', roles.PermissionsManagements.as_view({
        "get": "list",
        'post': 'create',
    }), name='userinfo'),
    path('permissions-data', roles.PermissionsAllData.as_view(), name='permissions-data'),
    path('permissions/<int:pk>', roles.PermissionsManagements.as_view({
        "put": "update",
        'delete': 'destroy',
        'get': 'details'
    }), name='management'),

    path('menus', roles.MenusManagements.as_view({
        "get": "list",
        'post': 'create',
    }), name='userinfo'),
    path('menus/<int:pk>', roles.MenusManagements.as_view({
        "put": "update",
        'delete': 'destroy',
        'get': 'details'
    }), name='management'),
    path('roles', roles.RolesManagement.as_view({
        "get": "list",
        'post': 'create',
    }), name='userinfo'),
    path('roles/<int:pk>', roles.RolesManagement.as_view({
        "put": "update",
        'delete': 'destroy',
        'get': 'details'
    }), name='management'),
]