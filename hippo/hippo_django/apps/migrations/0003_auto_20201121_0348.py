# Generated by Django 2.2.2 on 2020-11-20 19:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0002_auto_20201119_1908'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='一级菜单')),
                ('slug', models.CharField(max_length=64, unique=True, verbose_name='标识')),
            ],
            options={
                'verbose_name': '一级菜单表',
                'verbose_name_plural': '一级菜单表',
                'db_table': 'user_rbac_menus',
            },
        ),
        migrations.CreateModel(
            name='Permissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='标题')),
                ('slug', models.CharField(max_length=64, unique=True, verbose_name='标识')),
                ('url', models.CharField(max_length=128, unique=True, verbose_name='含正则的URL')),
                ('remarks', models.TextField(blank=True, default=None, null=True, verbose_name='备注')),
                ('menu', models.ForeignKey(blank=True, help_text='如果是 Null 就不是二级菜单, 如果是则是二级菜单', null=True, on_delete=django.db.models.deletion.CASCADE, to='apps.Menus', verbose_name='所属菜单')),
                ('pid', models.ForeignKey(blank=True, help_text='非菜单权限,需要选择一个可以作为菜单的权限用于做为默认展开,自关联到自己', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parents', to='apps.Permissions', verbose_name='关联的权限')),
            ],
            options={
                'verbose_name': '权限表',
                'verbose_name_plural': '权限表',
                'db_table': 'user_rbac_permissions',
            },
        ),
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, unique=True, verbose_name='角色名称')),
                ('slug', models.CharField(max_length=64, unique=True, verbose_name='标识')),
                ('remarks', models.TextField(blank=True, default=None, null=True, verbose_name='备注')),
                ('permissions', models.ManyToManyField(blank=True, to='apps.Permissions', verbose_name='拥有的所有权限')),
            ],
            options={
                'verbose_name': '角色表',
                'verbose_name_plural': '角色表',
                'db_table': 'user_rbac_roles',
            },
        ),
        migrations.AddField(
            model_name='userinfo',
            name='roles',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='apps.Roles', verbose_name='角色'),
        ),
    ]
