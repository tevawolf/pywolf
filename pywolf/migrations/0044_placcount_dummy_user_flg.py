# Generated by Django 2.1.2 on 2018-11-13 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pywolf', '0043_auto_20181113_1601'),
    ]

    operations = [
        migrations.AddField(
            model_name='placcount',
            name='dummy_user_flg',
            field=models.BooleanField(default=False, verbose_name='ダミー用ユーザーフラグ'),
        ),
    ]
