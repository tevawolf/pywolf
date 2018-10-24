from django.db import models
from ..pywolf.masters  import MSysMessageSet
from ..pywolf.masters  import MPosition
from ..pywolf.masters import MVoiceType
from ..pywolf.masters import MChipSet
from ..pywolf.masters import MChip


class PLAccount(models.Model):
    '''PLアカウント'''
    id = models.CharField(primary_key=True, max_length=255)  # ID(内部)
    id_view = models.CharField(max_length=100)  # ID(表示用)
    password = models.CharField(max_length=255)  # パスワード
    commentary = models.TextField(blank=True)  # 説明
    system_user_flg = models.BooleanField(default=False)  # システム用ユーザーフラグ
    delete_flg = models.BooleanField(default=False)  # 削除フラグ


class Village(models.Model):
    '''村'''
    village_no = models.AutoField(primary_key=True)  # 村No
    village_master_account = models.ForeignKey(PLAccount, on_delete=models.SET("削除されたID"))  # 村建てID
    village_name = models.CharField(max_length=255)  # 村名
    discription = models.TextField(blank=True)  # 村説明
    START_CLASS = (
        (1, '自動'),
        (2, '手動'),
        (3, '定員'),
    )
    start_class = models.SmallIntegerField(choices=START_CLASS, default=1)  # 開始区分
    lowest_number = models.SmallIntegerField(default=10)  # 最低人数
    max_number = models.SmallIntegerField(default=16)  # 最大人数
    into_password = models.CharField(max_length=255, blank=True)  # 入村パスワード
    # 自動退村有無フラグ
    # 遅刻見学可否フラグ
    update_time = models.TimeField()  # 更新時間
    UPDATE_INTERVAL = (
        (24, '24時間'),
        (48, '48時間'),
        (72, '72時間'),
    )
    update_interval = models.SmallIntegerField(choices=UPDATE_INTERVAL, default=24)  # 更新間隔
    start_scheduled_date = models.DateField()  # 村開始予定日
    abolition_date = models.DateField()  # 廃村日
    # 編成隠蔽フラグ
    VOICE_NUMBER_CLASS = (
        (1, "回数制"),
        (2, "ポイント(pt)制"),
    )
    voice_number_class = models.SmallIntegerField(choices=VOICE_NUMBER_CLASS, default=1)  # 発言数区分
    # 曖昧残喉フラグ
    # 発言促し回数
    # 発言促し回復区分
    # アクション区分
    # アクション定型文No
    # アクション回数
    # 投票方法区分
    chip_set = models.ForeignKey(MChipSet, on_delete=models.PROTECT)  # チップセット
    system_message = models.ForeignKey(MSysMessageSet,
                                          on_delete=models.PROTECT)  # システム文章
    # 役職希望可否フラグ
    # 自殺票可否フラグ
    # 突然死有無フラグ
    # 護衛手応え有無フラグ
    # ID公開フラグ
    delete_flg = models.BooleanField(default=False)  # 削除フラグ


class VillageOrganizationSet(models.Model):
    '''村編成セット'''
    village_no = models.ForeignKey(Village, on_delete=models.PROTECT)  # 村番号
    organization_set_name = models.CharField(max_length=100)  # 編成セット名称
    participant_number = models.SmallIntegerField()  # 参加者数
    delete_flg = models.BooleanField(default=False)  # 削除フラグ

    class Meta:
        unique_together=(("village_no", "organization_set_name"))

class VillageOrganization(models.Model):
    '''村編成'''
    village_no = models.ForeignKey(Village, on_delete=models.PROTECT)  # 村番号
    organization = models.ForeignKey(VillageOrganizationSet, on_delete=models.CASCADE)  # 編成セット
    serial_number = models.SmallIntegerField()  # 連番
    position = models.ForeignKey(MPosition, on_delete=models.PROTECT)  # 役職
    number = models.SmallIntegerField()  # 人数

    class Meta:
        unique_together=(("village_no", "organization", "serial_number"))


class VillageVoiceSetting(models.Model):
    '''村発言設定'''
    village_no = models.ForeignKey(Village, on_delete=models.PROTECT)  # 村番号
    voice_type = models.ForeignKey(MVoiceType, on_delete=models.PROTECT)  # 発言種別
    voice_number = models.SmallIntegerField(default=0)  # 発言回数設定
    max_str_length = models.SmallIntegerField(default=0)  # 最大文字数
    voice_point = models.SmallIntegerField(default=0)  # 発言ポイント
    max_voice_point = models.SmallIntegerField(default=0)  # 最大ポイント数
    prologue_limit_off_flg = models.BooleanField(default=False)  # プロローグ無制限発言フラグ
    tomb_limit_off_flg = models.BooleanField(default=False)  # 墓下無制限発言フラグ
    epilogue_limit_off_flg = models.BooleanField(default=True)  # エピローグ無制限発言フラグ

    class Meta:
        unique_together=(("village_no", "voice_type"))


class VillageParticipant(models.Model):
    '''村参加者'''
    village_no = models.ForeignKey(Village, on_delete=models.PROTECT)  # 村番号
    pl = models.ForeignKey(PLAccount, on_delete=models.PROTECT)  # PL
    chip = models.ForeignKey(MChip, on_delete=models.PROTECT) # チップ
    description = models.CharField(max_length=30)  # 肩書
    character_name = models.CharField(max_length=30)  # キャラクタ名
    wish_position = models.ForeignKey(
        MPosition, on_delete=models.PROTECT,
        related_name='%(class)s_wish_position_id')  # 希望役職
    position = models.ForeignKey(
        MPosition, on_delete=models.PROTECT,
        related_name='%(class)s_position_id')  # 役職
    STATUS = (
        (0, "生存"),
        (1, "処刑死"),
        (2, "襲撃死"),
        (9, "突然死"),
        (10, "退村"),
    )
    status = models.SmallIntegerField(choices=STATUS, default=0)  # 状態
    WIN_LOSE_CLASS = (
        (0, "未決着"),
        (1, "勝利"),
        (2, "敗北"),
        (9, "突然死"),
    )
    win_lose_class = models.SmallIntegerField(choices=WIN_LOSE_CLASS, default=0)  # 勝敗区分
    memo = models.TextField(blank=True)
    village_denominated_flg = models.BooleanField(default=False)  # 村建てフラグ
    system_user_flg = models.BooleanField(default=False)  # システム用ユーザーフラグ
    delete_flg = models.BooleanField(default=False)  # 削除フラグ

    class Meta:
        unique_together=(("village_no", "pl"))


class VillageProgress(models.Model):
    '''村進行'''
    village_no = models.ForeignKey(Village, on_delete=models.PROTECT)  # 村番号
    day_no = models.SmallIntegerField(default=0)  # 日数番号
    VILLAGE_STATUS = (
        (0, "プロローグ"),
        (1, "進行中"),
        (2, "エピローグ"),
        (3, "終了"),
        (4, "廃村"),
    )
    village_status = models.SmallIntegerField(choices=VILLAGE_STATUS, default=0)  # 村状態

    class Meta:
        unique_together=(("village_no", "day_no"))


class VillageParticipantVoiceStatus(models.Model):
    '''村参加者発言ステータス'''
    village_participant = models.ForeignKey(VillageParticipant, on_delete=models.PROTECT)  # 村参加者ID
    day_no = models.SmallIntegerField(default=0)  # 日数番号
    voice_type = models.ForeignKey(MVoiceType, on_delete=models.PROTECT)  # 発言種別
    voice_number_remain = models.SmallIntegerField()  # 残り発言回数
    voice_point_remain = models.SmallIntegerField()  # 残り発言ポイント数

    class Meta:
        unique_together=(("village_participant", "day_no"))


class VillageParticipantVoice(models.Model):
    '''村参加者発言'''
    village_no = models.ForeignKey(Village, on_delete=models.PROTECT)  # 村番号
    village_participant = models.ForeignKey(VillageParticipant, on_delete=models.PROTECT)  # 村参加者ID
    day_no = models.SmallIntegerField(default=0)  # 日数番号
    voice_type = models.ForeignKey(MVoiceType, on_delete=models.PROTECT)  # 発言種別
    voice_number = models.SmallIntegerField()  # 発言番号（種別毎）
    voice_order = models.SmallIntegerField()  # 発言順（村での通し番号）
    use_point = models.SmallIntegerField()  # 使用発言ポイント
    voice = models.TextField(blank=True)  # 発言
    good_pl = models.CharField(max_length=255, blank=True)  # イイねしたPL
    voice_datetime = models.DateTimeField()  # 発言日時
    system_voice_flg = models.BooleanField(default=False)  # システムメッセージフラグ
    delete_flg = models.BooleanField(default=False)  # 削除フラグ

    class Meta:
        unique_together=(("village_no", "day_no", "voice_type", "voice_number"))


class VillageParticipantExeAbility(models.Model):
    '''村参加者能力行使'''
    village_participant = models.ForeignKey(VillageParticipant, on_delete=models.PROTECT)
    day_no = models.SmallIntegerField(default=0)  # 日数番号
    vote = models.CharField(max_length=255, blank=True)  # 投票先ID
    fortune = models.CharField(max_length=255, blank=True)  # 占い先ID
    guard = models.CharField(max_length=255, blank=True)  # 護衛先ID
    assault = models.CharField(max_length=255, blank=True)  # 襲撃先ID

    class Meta:
        unique_together=(("village_participant", "day_no"))

