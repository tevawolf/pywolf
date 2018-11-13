from datetime import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse

from ...models.pywolf.masters import MChip
from ...models.pywolf.masters import MPosition
from ...models.pywolf.masters import MVoiceType
from ...models.pywolf.masters import VOICE_TYPE_ID

from ...models.pywolf.transactions import Village
from ...models.pywolf.transactions import VillageParticipant
from ...models.pywolf.transactions import VillageParticipantVoice
from ...models.pywolf.transactions import VillageParticipantVoiceStatus
from ...models.pywolf.transactions import VillageVoiceSetting
from ...models.pywolf.transactions import VillageParticipantExeAbility
from ...models.pywolf.transactions import PLAccount


def entry(request, village_no):
    """入村処理"""
    village = get_object_or_404(Village, pk=village_no)  # 村情報

    # 参加者登録
    participant = VillageParticipant()
    participant.village_no = village
    participant.pl = PLAccount.objects.get(pk=request.session['login_id'])

    # 連番
    if VillageParticipant.objects.filter(village_no=village_no, pl=request.session['login_id']).exists():
        lastpart = \
            VillageParticipant.objects \
        .filter(village_no=village_no, pl=request.session['login_id']) \
        .order_by('-sequence')[0]
        participant.sequence = lastpart.sequence + 1
    else:
        participant.sequence = 0

    participant.chip = MChip.objects.get(pk=request.POST['chip'])
    participant.description = request.POST['description']
    participant.character_name = request.POST['name']
    participant.wish_position = MPosition.objects.get(pk=request.POST['wish_position'])
    participant.position = None
    participant.status = 0
    participant.win_lose_class = 0

    # 村建てフラグの設定
    if participant.pl == village.village_master_account:
        participant.village_denominated_flg = True

    participant.save()

    # 第１発言登録
    voice = VillageParticipantVoice()
    voice.village_no = village
    voice.village_participant = participant
    voice.voice_type = MVoiceType.objects.get(pk=VOICE_TYPE_ID['normal'])
    if(village.villageparticipantvoice_set.exists()):
        lastvoice = village.villageparticipantvoice_set.filter(voice_type_id=VOICE_TYPE_ID['normal']).order_by('-voice_number')
        if lastvoice:
            voice.voice_number = lastvoice[0].voice_number + 1

        lastvoice_order = \
            village.villageparticipantvoice_set.order_by('-voice_order')[0]
        voice.voice_order = lastvoice_order.voice_order + 1
    else:
        voice.voice_number = 0
        voice.voice_order = 0

    voice.use_point = 0
    voice.voice = request.POST['voice']
    voice.voice_datetime = datetime.now()
    voice.delete_flg = False
    voice.save()

    # 投票･能力行使データ作成
    ability = VillageParticipantExeAbility()
    ability.village_participant = participant
    ability.day_no = 0
    ability.save()

    # 発言ステータス作成
    voice_setting = VillageVoiceSetting.objects.filter(village_no_id=village_no)
    for setting in voice_setting:
        voice_status = VillageParticipantVoiceStatus()
        voice_status.village_participant = participant
        voice_status.day_no = 0
        voice_status.voice_type = setting.voice_type
        voice_status.voice_number_remain = setting.voice_number
        voice_status.voice_point_remain = setting.voice_point
        voice_status.save()

    # 村メイン画面に戻る
    return HttpResponseRedirect(reverse('pywolf:village', args=(village_no, 0,)))
