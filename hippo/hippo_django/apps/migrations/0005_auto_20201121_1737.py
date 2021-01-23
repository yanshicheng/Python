# Generated by Django 2.2.2 on 2020-11-21 09:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0004_auto_20201121_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='department',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='users', to='apps.Department', verbose_name='部门'),
        ),
        migrations.RemoveField(
            model_name='userinfo',
            name='roles',
        ),
        migrations.AddField(
            model_name='userinfo',
            name='roles',
            field=models.ManyToManyField(blank=True, null=True, to='apps.Roles', verbose_name='角色'),
        ),
    ]
