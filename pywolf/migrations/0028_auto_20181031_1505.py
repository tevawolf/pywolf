# Generated by Django 2.1.2 on 2018-10-31 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pywolf', '0027_auto_20181031_1333'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='villageprogress',
            options={'get_latest_by': 'day_no', 'verbose_name': '村進行', 'verbose_name_plural': '村進行'},
        ),
        migrations.AddField(
            model_name='villageparticipantvoice',
            name='cancel_flg',
            field=models.BooleanField(default=False, verbose_name='発言取り消しフラグ'),
        ),
    ]
