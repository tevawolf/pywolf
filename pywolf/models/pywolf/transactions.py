from django.db import models
from django.core import validators
from ..pywolf.masters import MSysMessageSet
from ..pywolf.masters import MPosition
from ..pywolf.masters import MVoiceType
from ..pywolf.masters import MChipSet
from ..pywolf.masters import MChip
from ..pywolf.masters import MStyleSheet
from ..pywolf.masters import MOrganizationSet


class PLAccount(models.Model):
    class Meta:
        verbose_name = "PLアカウント"
        verbose_name_plural = "PLアカウント"
        db_table = 'pl_account'

    id = models.CharField(verbose_name='ID(内部)', primary_key=True, max_length=255)  # ID(内部)
    id_view = models.CharField(verbose_name='ID(表示用)', max_length=100)  # ID(表示用)
    password = models.CharField(verbose_name='パスワード', max_length=255)  # パスワード
    select_style = models.ForeignKey(MStyleSheet, verbose_name='選択スタイルシート', on_delete=models.SET_NULL, null=True)
    commentary = models.TextField(verbose_name='説明', blank=True)  # 説明
    system_user_flg = models.BooleanField(verbose_name='システム用ユーザーフラグ', default=False)  # システム用ユーザーフラグ
    delete_flg = models.BooleanField(verbose_name='削除フラグ', default=False)  # 削除フラグ

    def __str__(self):
        return self.id_view


class Village(models.Model):
    class Meta:
        verbose_name = "村"
        verbose_name_plural = "村情報"
        db_table = 'village'
        get_latest_by = 'village_no'

    village_no = models.AutoField(verbose_name='村No', primary_key=True)  # 村No
    village_master_account = models.ForeignKey(PLAccount, verbose_name='村建てID', on_delete=models.SET("削除されたID"))  # 村建てID
    village_name = models.CharField(verbose_name='村名', max_length=255)  # 村名
    description = models.TextField(verbose_name='村説明', blank=True)  # 村説明
    START_CLASS = (
        (1, '自動'),
        (2, '手動'),
        (3, '定員'),
    )
    start_class = models.SmallIntegerField(verbose_name='開始区分', choices=START_CLASS, default=1)  # 開始区分
    lowest_number = models.SmallIntegerField(verbose_name='最低人数', default=10,
                                             validators=[validators.MinValueValidator(4),
                                                         validators.MaxValueValidator(99)])  # 最低人数
    max_number = models.SmallIntegerField(verbose_name='最大人数', default=16,
                                          validators=[validators.MinValueValidator(4),
                                                      validators.MaxValueValidator(99)])  # 最大人数
    into_password = models.CharField(verbose_name='入村パスワード', max_length=255, blank=True)  # 入村パスワード
    # 自動退村有無フラグ
    # 遅刻見学可否フラグ
    update_time = models.TimeField(verbose_name='更新時間')  # 更新時間
    UPDATE_INTERVAL = (
        (24, '24時間'),
        (48, '48時間'),
        (72, '72時間'),
    )
    update_interval = models.SmallIntegerField(verbose_name='更新間隔', choices=UPDATE_INTERVAL, default=24)  # 更新間隔
    start_scheduled_date = models.DateField(verbose_name='村開始予定日')  # 村開始予定日
    abolition_date = models.DateField(verbose_name='廃村日')  # 廃村日
    # 編成隠蔽フラグ
    VOICE_NUMBER_CLASS = (
        (1, "回数制"),
        (2, "ポイント(pt)制"),
    )
    voice_number_class = models.SmallIntegerField(verbose_name='発言数区分', choices=VOICE_NUMBER_CLASS, default=1)  # 発言数区分
    # 曖昧残喉フラグ
    # 発言促し回数
    # 発言促し回復区分
    # アクション区分
    # アクション定型文No
    # アクション回数
    # 投票方法区分
    chip_set = models.ForeignKey(MChipSet, verbose_name='チップセット', on_delete=models.PROTECT)  # チップセット
    system_message = models.ForeignKey(MSysMessageSet, verbose_name='システム文章', on_delete=models.PROTECT)
    organization_setting = models.ForeignKey(MOrganizationSet, verbose_name='編成セット(村作成時の設定)', on_delete=models.PROTECT)
    # 役職希望可否フラグ
    # 自殺票可否フラグ
    # 突然死有無フラグ
    # 護衛手応え有無フラグ
    # ID公開フラグ
    delete_flg = models.BooleanField(verbose_name='削除フラグ', default=False)  # 削除フラグ

    def __str__(self):
        return "{0}村:{1}".format(self.village_no, self.village_name)


class VillageOrganizationSetting(models.Model):
    class Meta:
        verbose_name = "村編成設定"
        verbose_name_plural = "村編成設定"
        db_table = 'village_organization_setting'

    village_no = models.ForeignKey(Village, verbose_name='村', on_delete=models.PROTECT)  # 村番号
    participant_number = models.SmallIntegerField(verbose_name='参加者数')  # 参加者数
    delete_flg = models.BooleanField(verbose_name='削除フラグ', default=False)  # 削除フラグ

    def __str__(self):
        return "{0} {1}人".format(self.village_no, self.participant_number)


class VillageOrganization(models.Model):
    class Meta:
        verbose_name = "村編成"
        verbose_name_plural = "村編成"
        db_table = 'village_organization'
        unique_together = ("organization", "position")

    organization = models.ForeignKey(VillageOrganizationSetting, verbose_name='村編成設定', on_delete=models.CASCADE)
    position = models.ForeignKey(MPosition, verbose_name='役職', on_delete=models.PROTECT)  # 役職
    number = models.SmallIntegerField(verbose_name='人数')  # 人数


class VillageVoiceSetting(models.Model):
    class Meta:
        verbose_name = "村発言設定"
        verbose_name_plural = "村発言設定"
        db_table = 'village_voice_setting'
        unique_together = ("village_no", "voice_type")

    village_no = models.ForeignKey(Village, verbose_name='村', on_delete=models.PROTECT)  # 村番号
    voice_type = models.ForeignKey(MVoiceType, verbose_name='発言種別', on_delete=models.PROTECT)  # 発言種別
    voice_number = models.SmallIntegerField(verbose_name='発言回数設定', default=0)  # 発言回数設定
    max_str_length = models.SmallIntegerField(verbose_name='最大文字数', default=0)  # 最大文字数
    voice_point = models.SmallIntegerField(verbose_name='発言ポイント', default=0)  # 発言ポイント
    max_voice_point = models.SmallIntegerField(verbose_name='最大ポイント数', default=0)  # 最大ポイント数
    prologue_limit_off_flg = models.BooleanField(verbose_name='プロローグ無制限発言フラグ', default=False)  # プロローグ無制限発言フラグ
    tomb_limit_off_flg = models.BooleanField(verbose_name='墓下無制限発言フラグ', default=False)  # 墓下無制限発言フラグ
    epilogue_limit_off_flg = models.BooleanField(verbose_name='エピローグ無制限発言フラグ', default=True)  # エピローグ無制限発言フラグ


class VillageParticipant(models.Model):
    class Meta:
        verbose_name = "村参加者"
        verbose_name_plural = "村参加者"
        db_table = 'village_participant'
        unique_together = ("village_no", "pl", "sequence")

    village_no = models.ForeignKey(Village, verbose_name='村', on_delete=models.PROTECT)  # 村番号
    pl = models.ForeignKey(PLAccount, verbose_name='PL', on_delete=models.PROTECT)  # PL
    sequence = models.IntegerField(verbose_name='連番', default=0)
    chip = models.ForeignKey(MChip, verbose_name='チップ', on_delete=models.PROTECT) # チップ
    description = models.CharField(verbose_name='肩書', max_length=30)  # 肩書
    character_name = models.CharField(verbose_name='キャラクタ名', max_length=30)  # キャラクタ名
    wish_position = models.ForeignKey(
        MPosition, verbose_name='希望役職', on_delete=models.PROTECT,
        related_name='%(class)s_wish_position_id')  # 希望役職
    position = models.ForeignKey(
        MPosition, verbose_name='役職', on_delete=models.PROTECT,
        related_name='%(class)s_position_id', null=True, blank=True)  # 役職
    STATUS = (
        (0, "生存"),
        (1, "処刑死"),
        (2, "襲撃死"),
        (9, "突然死"),
        (10, "退村"),
    )
    status = models.SmallIntegerField(verbose_name='状態', choices=STATUS, default=0)  # 状態
    WIN_LOSE_CLASS = (
        (0, "未決着"),
        (1, "勝利"),
        (2, "敗北"),
        (9, "突然死"),
    )
    win_lose_class = models.SmallIntegerField(verbose_name='勝敗区分', choices=WIN_LOSE_CLASS, default=0)  # 勝敗区分
    memo = models.TextField(verbose_name='メモ', blank=True)  # メモ
    village_denominated_flg = models.BooleanField(verbose_name='村建てフラグ', default=False)  # 村建てフラグ
    system_user_flg = models.BooleanField(verbose_name='システム用ユーザーフラグ', default=False)  # システム用ユーザーフラグ
    cancel_flg = models.BooleanField(verbose_name='退村フラグ', default=False)
    delete_flg = models.BooleanField(verbose_name='削除フラグ', default=False)  # 削除フラグ

    def __str__(self):
        return "{0} {1}(連番{2}):{3}".format(self.village_no, self.pl, self.sequence, self.character_name)


class VillageProgress(models.Model):
    class Meta:
        verbose_name = "村進行"
        verbose_name_plural = "村進行"
        db_table = 'village_progress'
        unique_together = ("village_no", "day_no")
        get_latest_by = 'day_no'

    village_no = models.ForeignKey(Village, verbose_name='村', on_delete=models.PROTECT)  # 村番号
    day_no = models.SmallIntegerField(verbose_name='日数番号', default=0)  # 日数番号
    VILLAGE_STATUS = (
        (0, "プロローグ"),
        (1, "進行中"),
        (2, "エピローグ"),
        (3, "終了"),
        (4, "廃村"),
    )
    village_status = models.SmallIntegerField(verbose_name='村状態', choices=VILLAGE_STATUS, default=0)  # 村状態

    def __str__(self):
        return "{0}:{1}日目".format(self.village_no, self.day_no)


class VillageParticipantVoiceStatus(models.Model):
    class Meta:
        verbose_name = "村参加者発言ステータス"
        verbose_name_plural = "村参加者発言ステータス"
        db_table = 'village_participant_voice_status'
        unique_together = ("village_participant", "day_no", "voice_type")

    village_participant = models.ForeignKey(VillageParticipant, verbose_name='村参加者', on_delete=models.PROTECT)  # 村参加者ID
    day_no = models.SmallIntegerField(verbose_name='日数番号', default=0)  # 日数番号
    voice_type = models.ForeignKey(MVoiceType, verbose_name='発言種別', on_delete=models.PROTECT)  # 発言種別
    voice_number_remain = models.SmallIntegerField(verbose_name='残り発言回数')  # 残り発言回数
    voice_point_remain = models.SmallIntegerField(verbose_name='残り発言ポイント数')  # 残り発言ポイント数


class VillageParticipantVoice(models.Model):
    class Meta:
        verbose_name = "村参加者発言"
        verbose_name_plural = "村参加者発言"
        db_table = 'village_participant_voice'
        unique_together = ("village_no", "day_no", "voice_type", "voice_number")

    village_no = models.ForeignKey(Village, verbose_name='村', on_delete=models.PROTECT)  # 村番号
    village_participant = models.ForeignKey(VillageParticipant, verbose_name='村参加者', on_delete=models.PROTECT)  # 村参加者ID
    day_no = models.SmallIntegerField(verbose_name='日数番号', default=0)  # 日数番号
    voice_type = models.ForeignKey(MVoiceType, verbose_name='発言種別', on_delete=models.PROTECT)  # 発言種別
    voice_number = models.SmallIntegerField(verbose_name='発言番号（種別毎）')  # 発言番号（種別毎）
    voice_order = models.SmallIntegerField(verbose_name='発言順（村での通し番号）')  # 発言順（村での通し番号）
    use_point = models.SmallIntegerField(verbose_name='使用発言ポイント')  # 使用発言ポイント
    voice = models.TextField(verbose_name='発言', blank=True)  # 発言
    good_pl = models.CharField(verbose_name='イイねしたPL', max_length=255, blank=True)  # イイねしたPL
    voice_datetime = models.DateTimeField(verbose_name='発言日時')  # 発言日時
    system_voice_flg = models.BooleanField(verbose_name='システムメッセージフラグ', default=False)  # システムメッセージフラグ
    cancel_flg = models.BooleanField(verbose_name='発言取り消しフラグ', default=False)
    delete_flg = models.BooleanField(verbose_name='削除フラグ', default=False)  # 削除フラグ


class VillageParticipantExeAbility(models.Model):
    class Meta:
        verbose_name = "村参加者能力行使"
        verbose_name_plural = "村参加者能力行使"
        db_table = 'village_participant_exe_ability'
        unique_together = ("village_participant", "day_no")

    village_participant = models.ForeignKey(VillageParticipant, verbose_name='村参加者', on_delete=models.PROTECT)  # 村参加者
    day_no = models.SmallIntegerField(verbose_name='日数番号', default=0)  # 日数番号
    vote = models.CharField(verbose_name='投票先ID', max_length=255, blank=True)  # 投票先ID
    fortune = models.CharField(verbose_name='占い先ID', max_length=255, blank=True)  # 占い先ID
    fortune_result = models.BooleanField(verbose_name='占い結果(True:人狼,False:人間)', default=False, null=False)
    guard = models.CharField(verbose_name='護衛先ID', max_length=255, blank=True)  # 護衛先ID
    guard_result = models.BooleanField(verbose_name='護衛結果(True:成功,False:失敗)', default=False, null=False)
    assault = models.CharField(verbose_name='襲撃先ID', max_length=255, blank=True)  # 襲撃先ID
    assault_result = models.BooleanField(verbose_name='襲撃結果(True:成功,False:失敗)', default=False, null=False)  # 成否がわかるのは手ごたえあり設定の場合のみ

    def __str__(self):
        return "{0} : {1}日目".format(self.village_participant, self.day_no)


class VillageParticipantExeAbilitySpiritResult(models.Model):
    class Meta:
        verbose_name = "村参加者能力行使　霊能結果"
        verbose_name_plural = "村参加者能力行使　霊能結果"
        db_table = 'village_participant_exe_ability_spirit_result'
        unique_together = ("village_participant", "day_no", "spirit")

    village_participant = models.ForeignKey(VillageParticipant, verbose_name='村参加者', on_delete=models.PROTECT)  # 村参加者
    day_no = models.SmallIntegerField(verbose_name='日数番号', default=0)  # 日数番号
    spirit = models.CharField(verbose_name='霊能先ID', max_length=255, blank=True)
    spirit_result = models.BooleanField(verbose_name='霊能結果(True:人狼,False:人間)', default=False, null=False)

    def __str__(self):
        return "{0} : {1}日目 : {2}".format(self.village_participant, self.day_no, self.spirit)
