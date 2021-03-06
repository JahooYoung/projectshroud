# Generated by Django 2.1.7 on 2019-03-29 14:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.CharField(default='79ebd59596184741', editable=False, max_length=16, primary_key=True, serialize=False)),
                ('mobile', models.CharField(max_length=11, unique=True, verbose_name='手机号码')),
                ('real_name', models.CharField(max_length=20, verbose_name='真实姓名')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='电子邮件')),
                ('date_joined', models.DateField(auto_now_add=True, verbose_name='注册时间')),
                ('is_active', models.BooleanField(default=True)),
                ('is_site_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.CharField(default='32a7d6df508c', editable=False, max_length=16, primary_key=True, serialize=False)),
                ('title', models.CharField(default='', max_length=50, verbose_name='活动名称')),
                ('description', models.TextField(blank=True, verbose_name='描述')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('start_time', models.DateTimeField(verbose_name='开始时间')),
                ('end_time', models.DateTimeField(verbose_name='结束时间')),
                ('location', models.CharField(max_length=50)),
                ('public', models.BooleanField(default=True, verbose_name='是否公开')),
                ('require_approve', models.BooleanField(default=False, verbose_name='注册需要审核')),
            ],
            options={
                'ordering': ('create_time',),
            },
        ),
        migrations.CreateModel(
            name='Transport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transport_type', models.CharField(choices=[('Flight', '航班'), ('Train', '列车'), ('Other', '其他')], max_length=10)),
                ('transport_id', models.CharField(max_length=10, verbose_name='航班/列车号')),
                ('depart_station', models.CharField(blank=True, max_length=20, verbose_name='出发站')),
                ('depart_time', models.DateTimeField(blank=True, verbose_name='出发时间')),
                ('arrival_station', models.CharField(blank=True, max_length=20, verbose_name='到达站')),
                ('arrival_time', models.DateTimeField(verbose_name='到达时间')),
                ('other_detail', models.TextField(verbose_name='详细信息')),
            ],
        ),
        migrations.CreateModel(
            name='UserManageEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserRegisterEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_registered', models.DateTimeField(verbose_name='注册时间')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Event')),
                ('registered_transport', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.Transport')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='admins',
            field=models.ManyToManyField(related_name='admins', through='backend.UserManageEvent', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='event',
            name='host',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_host', to=settings.AUTH_USER_MODEL, verbose_name='创建者'),
        ),
        migrations.AddField(
            model_name='event',
            name='registered_attendee',
            field=models.ManyToManyField(related_name='registered_attendee', through='backend.UserRegisterEvent', to=settings.AUTH_USER_MODEL),
        ),
    ]
