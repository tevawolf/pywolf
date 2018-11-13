# Generated by Django 2.1.2 on 2018-11-13 00:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pywolf', '0038_auto_20181110_1437'),
    ]

    operations = [
        migrations.CreateModel(
            name='VillageParticipantExeAbilitySpiritResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_no', models.SmallIntegerField(default=0, verbose_name='日数番号')),
                ('spirit', models.CharField(blank=True, max_length=255, verbose_name='霊能先ID')),
                ('spirit_result', models.BooleanField(default=False, verbose_name='霊能結果(True:人狼,False:人間)')),
                ('village_participant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pywolf.VillageParticipant', verbose_name='村参加者')),
            ],
            options={
                'verbose_name': '村参加者能力行使\u3000霊能結果',
                'verbose_name_plural': '村参加者能力行使\u3000霊能結果',
                'db_table': 'village_participant_exe_ability_spirit_result',
            },
        ),
        migrations.AddField(
            model_name='villageparticipantexeability',
            name='assault_result',
            field=models.BooleanField(default=False, verbose_name='襲撃結果(True:成功,False:失敗)'),
        ),
        migrations.AddField(
            model_name='villageparticipantexeability',
            name='fortune_result',
            field=models.BooleanField(default=False, verbose_name='占い結果(True:人狼,False:人間)'),
        ),
        migrations.AddField(
            model_name='villageparticipantexeability',
            name='guard_result',
            field=models.BooleanField(default=False, verbose_name='護衛結果(True:成功,False:失敗)'),
        ),
        migrations.AlterUniqueTogether(
            name='villageparticipantexeabilityspiritresult',
            unique_together={('village_participant', 'day_no', 'spirit')},
        ),
    ]
