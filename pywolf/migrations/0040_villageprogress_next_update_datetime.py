# Generated by Django 2.1.2 on 2018-11-13 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pywolf', '0039_auto_20181113_0918'),
    ]

    operations = [
        migrations.AddField(
            model_name='villageprogress',
            name='next_update_datetime',
            field=models.DateTimeField(default='2018/01/01 00:00:00', verbose_name='次回更新日時'),
            preserve_default=False,
        ),
    ]