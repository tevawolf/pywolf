from django.db import models


class MPosition(models.Model):
    '''役職マスタ'''
    position_name = models.CharField(max_length=100)  # 役職名称
    CAMP_CLASS = (
        (1, "村人"),
        (2, "人狼"),
    )
    camp_class = models.SmallIntegerField(choices=CAMP_CLASS, default=1)  # 陣営区分
    vote_enable_flg = models.BooleanField(default=True)  # 投票可否フラグ
    fortune_enable_flg = models.BooleanField(default=False)  # 占い可否フラグ
    spirit_enable_flg = models.BooleanField(default=False)  # 霊媒可否フラグ
    guard_enable_flg = models.BooleanField(default=False)  # 護衛可否フラグ
    share_enable_flg = models.BooleanField(default=False)  # 共有可否フラグ
    assault_enable_flg = models.BooleanField(default=False)  # 襲撃可否フラグ
    commentary = models.TextField()  # 説明
    delete_flg = models.BooleanField(default=False)  # 削除フラグ

    def __str__(self):
        return self.position_name


class MOrganizationSet(models.Model):
    '''編成セットマスタ'''
    organization_set_name = models.CharField(max_length=100)  # 編成セット名称
    participant_number = models.SmallIntegerField()  # 参加者数
    delete_flg = models.BooleanField(default=False)  # 削除フラグ


class MOrganization(models.Model):
    '''編成マスタ'''
    organization = models.ForeignKey(MOrganizationSet, on_delete=models.CASCADE)  # 編成セット
    sequence_number = models.SmallIntegerField(default=0)  # 連番
    position_id = models.ForeignKey(MPosition, on_delete=models.PROTECT)  # 役職ID
    number = models.SmallIntegerField()  # 人数

    class Meta:
        unique_together=(("organization", "sequence_number"))


VOICE_TYPE_ID = {"normal": 1, "wolf": 2, "self": 3, "system": 4, "grave": 5, }

class MVoiceType(models.Model):
    '''発言種別マスタ'''
    voice_type_name = models.CharField(max_length=100)  # 発言種別名称
    voice_type_symbol = models.CharField(max_length=10, blank=True)  # 発言種別記号（例：人狼:*、独り言：-）
    prologue_speech_enable_flg = models.BooleanField(default=False)  # プロローグ発言可否フラグ
    commentary = models.TextField(blank=True)  # 説明
    delete_flg = models.BooleanField(default=False)  # 削除フラグ

    def __str__(self):
        return self.voice_type_name


class MPositionVoiceSetting(models.Model):
    '''役職別発言設定マスタ'''
    position = models.ForeignKey(MPosition, on_delete=models.CASCADE)  # 役職
    voice_type = models.ForeignKey(MVoiceType, on_delete=models.CASCADE)  # 発言種別
    SPEECH_HEAR_MODE = (
        (0, "発言・閲覧不可"),
        (1, "発言不可・他人発言のみ閲覧可"),
        (2, "発言可・自己発言のみ閲覧可"),
        (3, "発言可・自己・他人発言ともに閲覧可"),
    )
    speech_hear_mode = models.SmallIntegerField(choices=SPEECH_HEAR_MODE, default=0)
    commentary = models.TextField(blank=True)  # 説明

    class Meta:
        unique_together=(("position", "voice_type"))


class MVoiceSettingSet(models.Model):
    '''発言設定セットマスタ'''
    voice_type_set_name = models.CharField(max_length=100)  # 発言設定セット名称
    commentary = models.TextField(blank=True)  # 説明
    display_order = models.IntegerField()  # 並び順
    delete_flg = models.BooleanField(default=False)  # 削除フラグ


class MVoiceSetting(models.Model):
    '''発言設定マスタ'''
    voice_setting = models.ForeignKey(MVoiceSettingSet, on_delete=models.CASCADE)  # 発言設定セット
    voice_type = models.ForeignKey(MVoiceType, on_delete=models.PROTECT)  # 発言種別
    voice_number = models.SmallIntegerField(default=0)  # 発言回数設定
    max_str_length = models.SmallIntegerField(default=0)  # 最大文字数
    voice_point = models.SmallIntegerField(default=0)  # 発言ポイント
    max_voice_point = models.SmallIntegerField(default=0)  # 最大ポイント数

    class Meta:
        unique_together=(("voice_setting", "voice_type"))


class MChipSet(models.Model):
    '''チップセットマスタ'''
    chip_set_name = models.CharField(max_length=100)  # チップセット名称
    author_name = models.CharField(max_length=100)  # 作者名
    character_number = models.SmallIntegerField(default=0)  # キャラクター人数
    animation_flg = models.BooleanField(default=False)  # アニメーションフラグ
    description_change_enable_flg = models.BooleanField(default=False)  # 肩書き変更可否フラグ
    character_name_change_enable_flg = models.BooleanField(default=False)  # キャラクタ名変更可否フラグ
    delete_flg = models.BooleanField(default=False)  # 削除フラグ


class MChip(models.Model):
    '''キャラチップマスタ'''
    chip_set = models.ForeignKey(MChipSet, on_delete=models.CASCADE)  # チップセット
    sequence_number = models.SmallIntegerField(default=0)  # 連番
    image_file_path = models.FileField(upload_to='pywolf/static/pywolf/chips/')  # 画像ファイルパス
    image_width = models.SmallIntegerField(default=90)  # 画像幅
    image_height = models.SmallIntegerField(default=130)  # 画像高さ
    description = models.CharField(max_length=30)  # 肩書
    character_name = models.CharField(max_length=30)  # キャラクタ名
    delete_flg = models.BooleanField(default=False)  # 削除フラグ

    class Meta:
        unique_together=(("chip_set", "sequence_number"))


class MSysMessageSet(models.Model):
    '''システム文章セットマスタ'''
    system_message_set_name = models.CharField(max_length=100)  # システム文書セット名称
    commentary = models.TextField(blank=True)  # 説明
    display_order = models.IntegerField(default=0)  # 並び順
    delete_flg = models.BooleanField(default=False)  # 削除フラグ


class MSysMessage(models.Model):
    '''システム文章マスタ'''
    system_message_set = models.ForeignKey(MSysMessageSet, on_delete=models.CASCADE)  # システム文章セット
    sequence_number = models.SmallIntegerField(default=0)  # 連番
    system_message_name = models.CharField(max_length=100)  # システム文書名称
    message = models.TextField(blank=True)  # 本文
    delete_flg = models.BooleanField(default=False)  # 削除フラグ

    class Meta:
        unique_together=(("system_message_set", "sequence_number"))

