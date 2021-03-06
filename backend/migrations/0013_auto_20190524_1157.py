# Generated by Django 2.2.1 on 2019-05-24 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0012_event_description_html'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='end_time',
            field=models.DateTimeField(db_index=True, verbose_name='结束时间'),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_time',
            field=models.DateTimeField(db_index=True, verbose_name='开始时间'),
        ),
        migrations.AlterUniqueTogether(
            name='transport',
            unique_together={('user', 'event')},
        ),
        migrations.AlterUniqueTogether(
            name='usermanageevent',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='userregisterevent',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='usermanageevent',
            constraint=models.UniqueConstraint(fields=('user', 'event'), name='unique_registration'),
        ),
        migrations.AddConstraint(
            model_name='userregisterevent',
            constraint=models.UniqueConstraint(fields=('user', 'event'), name='unique_registration'),
        ),
    ]
