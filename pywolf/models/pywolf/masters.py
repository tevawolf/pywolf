from django.db import models

from pywolf.enums import CampClass
from pywolf.enums import SpeechHearMode

STATICFILES_DIRS = 'pywolf/static/'


class MPosition(models.Model):
    class Meta:
        verbose_name = "役職"
        verbose_name_plural = "役職マスタ"
        db_table = 'm_position'

    position_name = models.CharField(verbose_name='役職名称', max_length=100)  # 役職名称
    CAMP_CLASS = (
        (CampClass.VILLAGE.value, "村人"),
        (CampClass.WOLF.value, "人狼"),
    )
    camp_class = models.SmallIntegerField(verbose_name='陣営区分', choices=CAMP_CLASS, default=1)  # 陣営区分
    vote_enable_flg = models.BooleanField(verbose_name='投票可否フラグ', default=True)  # 投票可否フラグ
    fortune_enable_flg = models.BooleanField(verbose_name='占い可否フラグ', default=False)  # 占い可否フラグ
    spirit_enable_flg = models.BooleanField(verbose_name='霊媒可否フラグ', default=False)  # 霊媒可否フラグ
    guard_enable_flg = models.BooleanField(verbose_name='護衛可否フラグ', default=False)  # 護衛可否フラグ
    share_enable_flg = models.BooleanField(verbose_name='共有可否フラグ', default=False)  # 共有可否フラグ
    assault_enable_flg = models.BooleanField(verbose_name='襲撃可否フラグ', default=False)  # 襲撃可否フラグ
    commentary = models.TextField(verbose_name='説明')  # 説明
    delete_flg = models.BooleanField(verbose_name='削除フラグ', default=False)  # 削除フラグ

    def __str__(self):
        return self.position_name


class MOrganizationSet(models.Model):
    class Meta:
        verbose_name = "編成セット"
        verbose_name_plural = "編成セットマスタ"
        db_table = 'm_organization_set'

    organization_set_name = models.CharField(verbose_name='編成セット名称', max_length=100)  # 編成セット名称
    display_order = models.IntegerField(verbose_name='並び順')  # 並び順
    delete_flg = models.BooleanField(verbose_name='削除フラグ', default=False)  # 削除フラグ

    def __str__(self):
        return self.organization_set_name


class MOrganizationParticipantNumber(models.Model):
    class Meta:
        verbose_name = "編成　参加人数"
        verbose_name_plural = "編成　参加人数マスタ"
        db_table = 'm_organization_participant_number'
        unique_together = ("organization", "participant_number")

    organization = models.ForeignKey(MOrganizationSet, verbose_name='編成セット', on_delete=models.CASCADE)  # 編成セット
    participant_number = models.SmallIntegerField(verbose_name='参加者数')  # 参加者数

    def __str__(self):
        return str(self.participant_number)


class MOrganizationPositionNumber(models.Model):
    class Meta:
        verbose_name = "編成"
        verbose_name_plural = "編成マスタ"
        db_table = 'm_organization_position_number'
        unique_together = ("organization", "participant_number_id", "position_id")

    organization = models.ForeignKey(MOrganizationSet, verbose_name='編成セット', on_delete=models.CASCADE)  # 編成セット
    participant_number_id = models.ForeignKey(MOrganizationParticipantNumber, verbose_name='参加人数', on_delete=models.CASCADE)  # 参加人数
    position_id = models.ForeignKey(MPosition, verbose_name='役職', on_delete=models.PROTECT)  # 役職ID
    number = models.SmallIntegerField(verbose_name='人数')  # 人数


class MVoiceType(models.Model):
    class Meta:
        verbose_name = "発言種別"
        verbose_name_plural = "発言種別マスタ"
        db_table = 'm_voice_type'

    voice_type_name = models.CharField(verbose_name='発言種別名称', max_length=100)  # 発言種別名称
    voice_type_symbol = models.CharField(verbose_name='発言種別記号（例：人狼:*、独り言：-）', max_length=10, blank=True)  # 発言種別記号（例：人狼:*、独り言：-）
    prologue_speech_enable_flg = models.BooleanField(verbose_name='プロローグ発言可否フラグ', default=False)  # プロローグ発言可否フラグ
    commentary = models.TextField(verbose_name='説明', blank=True)  # 説明
    delete_flg = models.BooleanField(verbose_name='削除フラグ', default=False)  # 削除フラグ

    def __str__(self):
        return self.voice_type_name


class MPositionVoiceSetting(models.Model):
    class Meta:
        verbose_name = "役職別発言設定"
        verbose_name_plural = "役職別発言設定マスタ"
        db_table = 'm_position_voice_setting'
        unique_together = ("position", "voice_type")

    position = models.ForeignKey(MPosition, verbose_name='役職', on_delete=models.CASCADE)  # 役職
    voice_type = models.ForeignKey(MVoiceType, verbose_name='発言種別', on_delete=models.CASCADE)  # 発言種別
    SPEECH_HEAR_MODE = (
        (SpeechHearMode.IMPOSSIBLE.value, "発言・閲覧不可"),
        (SpeechHearMode.NOT_SPEECH_HEAR_OTHER.value, "発言不可・他人発言のみ閲覧可"),
        (SpeechHearMode.SPEECH_HEAR_SELF, "発言可・自己発言のみ閲覧可"),
        (SpeechHearMode.SPEECH_HEAR, "発言可・自己・他人発言ともに閲覧可"),
    )
    speech_hear_mode = models.SmallIntegerField(verbose_name='発言・閲覧モード', choices=SPEECH_HEAR_MODE, default=0)  # 発言・閲覧モード
    commentary = models.TextField(verbose_name='説明', blank=True)  # 説明


class MVoiceSettingSet(models.Model):
    class Meta:
        verbose_name = "発言設定セット"
        verbose_name_plural = "発言設定セットマスタ"
        db_table = 'm_voice_setting_set'

    voice_setting_set_name = models.CharField(verbose_name='発言設定セット名称', max_length=100)  # 発言設定セット名称
    commentary = models.TextField(verbose_name='説明', blank=True)  # 説明
    display_order = models.IntegerField(verbose_name='並び順')  # 並び順
    delete_flg = models.BooleanField(verbose_name='削除フラグ', default=False)  # 削除フラグ

    def __str__(self):
        return self.voice_setting_set_name


class MVoiceSetting(models.Model):
    class Meta:
        verbose_name = "発言設定"
        verbose_name_plural = "発言設定マスタ"
        db_table = 'm_voice_setting'
        unique_together = ("voice_setting", "voice_type")

    voice_setting = models.ForeignKey(MVoiceSettingSet, verbose_name='発言設定セット', on_delete=models.CASCADE)  # 発言設定セット
    voice_type = models.ForeignKey(MVoiceType, verbose_name='発言種別', on_delete=models.PROTECT)  # 発言種別
    voice_number = models.SmallIntegerField(verbose_name='発言回数設定', default=0)  # 発言回数設定
    max_str_length = models.SmallIntegerField(verbose_name='最大文字数', default=0)  # 最大文字数
    voice_point = models.SmallIntegerField(verbose_name='発言ポイント', default=0)  # 発言ポイント
    max_voice_point = models.SmallIntegerField(verbose_name='最大ポイント数', default=0)  # 最大ポイント数



class MChipSet(models.Model):
    class Meta:
        verbose_name = "チップセット"
        verbose_name_plural = "チップセットマスタ"
        db_table = 'm_chip_set'

    chip_set_name = models.CharField(verbose_name='チップセット名称', max_length=100)  # チップセット名称
    author_name = models.CharField(verbose_name='作者名', max_length=100)  # 作者名
    character_number = models.SmallIntegerField(verbose_name='キャラクター人数', default=0)  # キャラクター人数
    animation_flg = models.BooleanField(verbose_name='アニメーションフラグ', default=False)  # アニメーションフラグ
    description_change_enable_flg = models.BooleanField(verbose_name='肩書き変更可否フラグ', default=False)  # 肩書き変更可否フラグ
    character_name_change_enable_flg = models.BooleanField(verbose_name='キャラクタ名変更可否フラグ', default=False)  # キャラクタ名変更可否フラグ
    display_order = models.IntegerField(verbose_name='並び順')  # 並び順
    delete_flg = models.BooleanField(verbose_name='削除フラグ', default=False)  # 削除フラグ

    def __str__(self):
        return self.chip_set_name


class MChip(models.Model):
    class Meta:
        verbose_name = "キャラチップ"
        verbose_name_plural = "キャラチップマスタ"
        db_table = 'm_chip'
        unique_together = ("chip_set", "sequence_number")

    chip_set = models.ForeignKey(MChipSet, verbose_name='チップセット', on_delete=models.CASCADE)  # チップセット
    sequence_number = models.SmallIntegerField(verbose_name='連番', default=0)  # 連番
    image_file_path = models.FileField(verbose_name='画像ファイルパス', upload_to=STATICFILES_DIRS + 'pywolf/chips/')  # 画像ファイルパス
    image_width = models.SmallIntegerField(verbose_name='画像幅', default=90)  # 画像幅
    image_height = models.SmallIntegerField(verbose_name='画像高さ', default=130)  # 画像高さ
    description = models.CharField(verbose_name='肩書', max_length=30)  # 肩書
    character_name = models.CharField(verbose_name='キャラクタ名', max_length=30)  # キャラクタ名
    dummy_flg = models.BooleanField(verbose_name='ダミーキャラクタフラグ', default=False)
    dummy_voice_pro = models.TextField(verbose_name='ダミー発言：プロローグ', null=True, blank=True)
    dummy_voice_first = models.TextField(verbose_name='ダミー発言：１日目', null=True, blank=True)
    delete_flg = models.BooleanField(verbose_name='削除フラグ', default=False)  # 削除フラグ

    def __str__(self):
        return '{} {}'.format(self.description, self.character_name)

    def get_path(self):
        return str(self.image_file_path).replace(STATICFILES_DIRS, '')


class MSysMessageSet(models.Model):
    class Meta:
        verbose_name = "システム文章セット"
        verbose_name_plural = "システム文章セットマスタ"
        db_table = 'm_system_message_set'

    system_message_set_name = models.CharField(verbose_name='システム文書セット名称', max_length=100)  # システム文書セット名称
    commentary = models.TextField(verbose_name='説明', blank=True)  # 説明
    display_order = models.IntegerField(verbose_name='並び順', default=0)  # 並び順
    delete_flg = models.BooleanField(verbose_name='削除フラグ', default=False)  # 削除フラグ

    def __str__(self):
        return self.system_message_set_name


class MSysMessage(models.Model):
    class Meta:
        verbose_name = "システム文章"
        verbose_name_plural = "システム文章マスタ"
        db_table = 'm_system_message'
        unique_together = ("system_message_set", "sequence_number")

    system_message_set = models.ForeignKey(MSysMessageSet, verbose_name='システム文章セット', on_delete=models.CASCADE)  # システム文章セット
    sequence_number = models.SmallIntegerField(verbose_name='連番', default=0)  # 連番
    system_message_name = models.CharField(verbose_name='システム文書名称', max_length=100)  # システム文書名称
    message = models.TextField(verbose_name='本文', blank=True)  # 本文
    delete_flg = models.BooleanField(verbose_name='削除フラグ', default=False)  # 削除フラグ

    def __str__(self):
        return self.system_message_name


class MStyleSheetSet(models.Model):
    class Meta:
        verbose_name = "スタイルシートセット"
        verbose_name_plural = "スタイルシートセットマスタ"
        db_table = 'm_stylesheet_set'

    stylesheet_set_name = models.CharField(verbose_name='スタイルシートセット名称', max_length=100)
    commentary = models.TextField(verbose_name='説明', blank=True)  # 説明
    display_order = models.IntegerField(verbose_name='並び順', default=0)  # 並び順
    delete_flg = models.BooleanField(verbose_name='削除フラグ', default=False)  # 削除フラグ

    def __str__(self):
        return self.stylesheet_set_name


class MStyleSheet(models.Model):
    class Meta:
        verbose_name = "スタイルシート"
        verbose_name_plural = "スタイルシートマスタ"
        db_table = 'm_stylesheet'
        unique_together = ("stylesheet_set", "sequence_number")

    stylesheet_set = models.ForeignKey(MStyleSheetSet, verbose_name='スタイルシートセット', on_delete=models.CASCADE)
    sequence_number = models.SmallIntegerField(verbose_name='連番', default=0)  # 連番
    stylesheet_name = models.CharField(verbose_name='スタイルシート名', max_length=100)
    file_path = models.FileField(verbose_name='ファイルパス', upload_to=STATICFILES_DIRS + 'pywolf/')
    commentary = models.TextField(verbose_name='説明', blank=True)  # 説明
    delete_flg = models.BooleanField(verbose_name='削除フラグ', default=False)

    def __str__(self):
        return self.stylesheet_name

    def get_path(self):
        return str(self.file_path).replace(STATICFILES_DIRS, '')
