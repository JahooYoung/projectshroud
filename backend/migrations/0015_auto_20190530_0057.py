# Generated by Django 2.2.1 on 2019-05-29 16:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0014_auto_20190530_0041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkin',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Event'),
        ),
    ]
