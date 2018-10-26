# Generated by Django 2.1.2 on 2018-10-26 04:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pywolf', '0020_auto_20180904_1631'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mchip',
            options={'verbose_name': 'キャラチップ', 'verbose_name_plural': 'キャラチップマスタ'},
        ),
        migrations.AlterModelOptions(
            name='mchipset',
            options={'verbose_name': 'チップセット', 'verbose_name_plural': 'チップセットマスタ'},
        ),
        migrations.AlterModelOptions(
            name='morganization',
            options={'verbose_name': '編成', 'verbose_name_plural': '編成マスタ'},
        ),
        migrations.AlterModelOptions(
            name='morganizationset',
            options={'verbose_name': '編成セット', 'verbose_name_plural': '編成セットマスタ'},
        ),
        migrations.AlterModelOptions(
            name='mposition',
            options={'verbose_name': '役職', 'verbose_name_plural': '役職マスタ'},
        ),
        migrations.AlterModelOptions(
            name='mpositionvoicesetting',
            options={'verbose_name': '役職別発言設定', 'verbose_name_plural': '役職別発言設定マスタ'},
        ),
        migrations.AlterModelOptions(
            name='msysmessage',
            options={'verbose_name': 'システム文章', 'verbose_name_plural': 'システム文章マスタ'},
        ),
        migrations.AlterModelOptions(
            name='msysmessageset',
            options={'verbose_name': 'システム文章セット', 'verbose_name_plural': 'システム文章セットマスタ'},
        ),
        migrations.AlterModelOptions(
            name='mvoicesetting',
            options={'verbose_name': '発言設定', 'verbose_name_plural': '発言設定マスタ'},
        ),
        migrations.AlterModelOptions(
            name='mvoicesettingset',
            options={'verbose_name': '発言設定セット', 'verbose_name_plural': '発言設定セットマスタ'},
        ),
        migrations.AlterModelOptions(
            name='mvoicetype',
            options={'verbose_name': '発言種別', 'verbose_name_plural': '発言種別マスタ'},
        ),
        migrations.AlterModelOptions(
            name='placcount',
            options={'verbose_name': 'PLアカウント', 'verbose_name_plural': 'PLアカウント'},
        ),
        migrations.AlterModelOptions(
            name='village',
            options={'verbose_name': '村情報', 'verbose_name_plural': '村情報'},
        ),
        migrations.AlterModelOptions(
            name='villageorganization',
            options={'verbose_name': '村編成', 'verbose_name_plural': '村編成'},
        ),
        migrations.AlterModelOptions(
            name='villageorganizationset',
            options={'verbose_name': '村編成セット', 'verbose_name_plural': '村編成セット'},
        ),
        migrations.AlterModelOptions(
            name='villageparticipant',
            options={'verbose_name': '村参加者', 'verbose_name_plural': '村参加者'},
        ),
        migrations.AlterModelOptions(
            name='villageparticipantexeability',
            options={'verbose_name': '村参加者能力行使', 'verbose_name_plural': '村参加者能力行使'},
        ),
        migrations.AlterModelOptions(
            name='villageparticipantvoice',
            options={'verbose_name': '村参加者発言', 'verbose_name_plural': '村参加者発言'},
        ),
        migrations.AlterModelOptions(
            name='villageparticipantvoicestatus',
            options={'verbose_name': '村参加者発言ステータス', 'verbose_name_plural': '村参加者発言ステータス'},
        ),
        migrations.AlterModelOptions(
            name='villageprogress',
            options={'verbose_name': '村進行', 'verbose_name_plural': '村進行'},
        ),
        migrations.AlterModelOptions(
            name='villagevoicesetting',
            options={'verbose_name': '村発言設定', 'verbose_name_plural': '村発言設定'},
        ),
        migrations.RenameField(
            model_name='village',
            old_name='discription',
            new_name='description',
        ),
    ]