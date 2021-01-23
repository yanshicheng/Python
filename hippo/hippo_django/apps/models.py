from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, User
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
# Create your models here.
__all__ = ['Department', 'UserInfo', 'Roles','Permissions',  'Menus', 'CasbinPermissions', 'CasbinRoles', 'CasbinUsers']

# 一级菜单表
class Menus(models.Model):
    title = models.CharField(verbose_name='菜单名称', max_length=32)
    slug = models.CharField(verbose_name='标识', max_length=64, unique=True)
    url = models.CharField(verbose_name='含正则的URL', max_length=128, unique=True)
    roles = models.ManyToManyField(verbose_name='所属角色', to='Roles',  help_text='菜单属于哪个角色')
    pid = models.IntegerField(verbose_name='是否为主菜单', null=True, blank=True, help_text='为0则是一级菜单,指定id则是指定id的二级菜单')
    class Meta:
        db_table = 'user_rbac_menus'
        verbose_name = '菜单表'
        verbose_name_plural = '菜单表'




class Permissions(models.Model):
    """
    权限表
    """
    title = models.CharField(verbose_name='标题', max_length=32)
    slug = models.CharField(verbose_name='标识', max_length=64)
    remarks = models.TextField('备注', blank=True, null=True, default=None)
    pid = models.IntegerField(verbose_name='是否为分类', null=True, blank=True, help_text='0为权限分类指定ID则属于二级')
    def __str__(self):
        return self.title
    class Meta:
        db_table = 'user_rbac_permissions'
        verbose_name = '权限表'
        verbose_name_plural = '权限表'


class Roles(models.Model):
    """
    角色
    """
    title = models.CharField(verbose_name='角色名称', max_length=32, unique=True)
    slug = models.CharField(verbose_name='标识', max_length=64, unique=True)
    permissions = models.ManyToManyField(verbose_name='拥有的所有权限', to='Permissions', blank=True)
    remarks = models.TextField('备注', blank=True, null=True, default=None)

    def __str__(self):
        return self.title
    class Meta:
        db_table = 'user_rbac_roles'
        verbose_name = '角色表'
        verbose_name_plural = '角色表'

# 定义管理类
class UserManager(BaseUserManager):
    use_in_migrations = True
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)  # 创建对象 UserProfile(email='', password='')
        user.set_password(password)  # 把密码加密
        user.save(using=self._db)  # 保存到数据库
        return user
    # 创建普通用户
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    # 创建超级用户
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)
# 定义部门
class Department(models.Model):
    title = models.CharField(max_length=32, verbose_name="部门名称")
    count = models.IntegerField(verbose_name="人数", default=0)

    def __str__(self):
        return self.title
    class Meta:
        db_table = 'user_department'
        verbose_name = '部门管理'
        verbose_name_plural = "部门管理"
# 定义UserProfile这个类的管理类
#
class UserInfo(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('邮箱', max_length=255,unique=True, db_index=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('是否允许用户登录admin站点.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    name = models.CharField('名字',max_length=32, db_index=True)
    department = models.ForeignKey('Department', verbose_name='部门', on_delete=models.PROTECT, related_name='users')
    roles = models.ManyToManyField(verbose_name='角色',to='Roles')
    phone = models.CharField('手机号码', max_length=32,  blank=True, null=True,validators=[RegexValidator(r'^1[3-9]\d{9}$',), ])
    remarks = models.TextField('备注', blank=True, null=True, default=None)
    date_joined = models.DateTimeField('创建时间', auto_now_add=True)
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'  # 用来唯一确定auth中的用户
    REQUIRED_FIELDS = ['name']  # auth指定除了上面两个配置项的字段还有那些字段要必填

    class Meta:
        db_table = 'user_userinfo'
        verbose_name = '用户管理'
        verbose_name_plural = "用户管理"
    #
    def get_full_name(self):
        # The user is identified by their email address
        return self.name

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):  # __unicode__ on Python 2
        return self.name
    # 给ORM添加管理类
    objects = UserManager()



class CasbinRule(models.Model):
    CHOICE_PTYPE = (
        ('p', 'p'),
        ('g', 'g'),
    )
    ptype = models.CharField(max_length=1, choices=CHOICE_PTYPE,verbose_name="p | g")
    v0 = models.CharField(max_length=32, verbose_name="⽤户组 | ⽤户")
    v1 = models.CharField(max_length=32, verbose_name="PATH | ⽤户组")
    v2 = models.CharField(max_length=32, null=True, blank=True,verbose_name="METHOD")
    v3 = models.CharField(max_length=32, null=True, blank=True)
    v4 = models.CharField(max_length=32, null=True, blank=True)
    v5 = models.CharField(max_length=32, null=True, blank=True)
    class Meta:
        db_table = 'casbin_rule'
        verbose_name_plural = verbose_name = 'RESTful权限系统'
    def serializer(self):
        return {
         'ptype': self.ptype,
         'v0': self.v0,
         'v1': self.v1,
         'v2': self.v2,
         'v3': self.v3,
         'v4': self.v4,
         'v5': self.v5,
        }

class CasbinPermissions(models.Model):
    CHOICE_PTYPE = (
        ('p', '角色'),
        ('g', '角色组'),
    )
    CHOICE_METHOD = (
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('DELETE', 'DELETE'),
        ('PUT', 'PUT'),
    )
    title = models.CharField(verbose_name='权限名称', max_length=32)
    ptype = models.CharField(max_length=1, choices=CHOICE_PTYPE,verbose_name="数据类型p | g")
    url = models.CharField(verbose_name='含正则的URL', max_length=128)
    method = models.CharField(max_length=2010, choices=CHOICE_METHOD,default='GET',verbose_name="请求方法")
    roles = models.ManyToManyField(verbose_name='所属角色', to='CasbinRoles',  help_text='权限归属那个角色或者角色组', blank=True, )
    def __str__(self):
        return self.title
    class Meta:
        db_table = 'CasbinPermissions'
        verbose_name_plural = verbose_name = 'casbin权限'
    def serializer(self):
        res = []
        if self.ptype == 'p':
            res = [roles.title for roles in self.roles.all()]
        else:
            for roles in self.roles.all():
                if roles.pid == 0:
                    obj = CasbinRoles.objects.filter(pid=roles.id).values('title')
                    for item in obj:
                        res.append(str(item['title']))
                else:
                    res.append(roles.title)

        return {
         'ptype': self.ptype,
         'roles': res,
         'url': self.url ,
         'method': self.method,
        }
class CasbinRoles(models.Model):
    pid = models.IntegerField(verbose_name='类型', help_text='0 为权限组,')
    title = models.CharField(verbose_name='角色/角色组名称', max_length=32)
    def __str__(self):
        return self.title
    class Meta:
        db_table = 'CasbinRoles'
        verbose_name_plural = verbose_name = 'casbin角色'

class CasbinUsers(models.Model):
    name = models.CharField(verbose_name='角色/角色组名称', max_length=32)
    roles = models.ManyToManyField(verbose_name='绑定角色', help_text='绑定角色', to='CasbinRoles',blank=True, )
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'CasbinUsers'
        verbose_name_plural = verbose_name = 'casbin用户'