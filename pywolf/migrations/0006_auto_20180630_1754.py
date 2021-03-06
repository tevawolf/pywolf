# Generated by Django 2.0.6 on 2018-06-30 08:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pywolf', '0005_auto_20180630_1729'),
    ]

    operations = [
        migrations.RenameField(
            model_name='village',
            old_name='system_message_no',
            new_name='system_message_id',
        ),
        migrations.AddField(
            model_name='village',
            name='chip_set_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='pywolf.MChipSet'),
            preserve_default=False,
        ),
    ]
