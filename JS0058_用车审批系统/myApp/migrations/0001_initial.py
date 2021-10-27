# Generated by Django 2.2.4 on 2021-04-14 14:57

import datetime
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone', models.CharField(max_length=64)),
                ('name', models.CharField(max_length=2048)),
                ('role', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no', models.CharField(max_length=64)),
                ('type', models.CharField(max_length=64)),
                ('nums', models.IntegerField()),
                ('knmus', models.CharField(max_length=64)),
                ('address', models.CharField(max_length=2048)),
                ('status', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='CarApply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('basis', models.CharField(max_length=2048, verbose_name='申请依据')),
                ('place', models.CharField(max_length=2048, verbose_name='申请地点')),
                ('cause', models.CharField(max_length=2048, verbose_name='申请事由')),
                ('desti', models.CharField(max_length=2048, verbose_name='申请目的地')),
                ('penum', models.IntegerField(verbose_name='申请人数')),
                ('usetime', models.DateTimeField(verbose_name='申请使用时间')),
                ('gettime', models.DateTimeField(verbose_name='驱车时间')),
                ('flow_rank', models.IntegerField(verbose_name='审核流等级')),
                ('flow_id', models.IntegerField(default=0)),
                ('status', models.CharField(max_length=64, verbose_name='申请状态')),
                ('create_time', models.DateTimeField(default=datetime.datetime(2021, 4, 14, 22, 57, 13, 673188), verbose_name='创建时间')),
            ],
        ),
        migrations.CreateModel(
            name='Dept',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no', models.CharField(max_length=64, verbose_name='部门编号')),
                ('name', models.CharField(max_length=2048)),
            ],
        ),
        migrations.CreateModel(
            name='CarLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option_type', models.CharField(max_length=64)),
                ('remark', models.CharField(max_length=2048)),
                ('create_time', models.DateTimeField(default=datetime.datetime(2021, 4, 14, 22, 57, 13, 672644))),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myApp.Car')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CarApplyLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=64)),
                ('remark', models.CharField(max_length=2048, null=True)),
                ('create_time', models.DateTimeField(default=datetime.datetime(2021, 4, 14, 22, 57, 13, 673814), verbose_name='创建时间')),
                ('update_time', models.DateTimeField(default=datetime.datetime(2021, 4, 14, 22, 57, 13, 673830), verbose_name='更新时间')),
                ('applyId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myApp.CarApply')),
                ('userId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='carapply',
            name='dept',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myApp.Dept'),
        ),
        migrations.AddField(
            model_name='carapply',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='car',
            name='dept',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myApp.Dept'),
        ),
        migrations.AddField(
            model_name='user',
            name='deptId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myApp.Dept'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
