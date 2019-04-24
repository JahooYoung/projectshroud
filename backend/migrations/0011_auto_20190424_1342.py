# Generated by Django 2.1.7 on 2019-04-24 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0010_auto_20190424_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userregisterevent',
            name='application_text',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='userregisterevent',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='userregisterevent',
            name='date_approved',
            field=models.DateTimeField(null=True, verbose_name='批准时间'),
        ),
    ]
