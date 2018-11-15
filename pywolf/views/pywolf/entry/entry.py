from datetime import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse

from pywolf.models.pywolf.masters import MChip
from pywolf.models.pywolf.masters import MPosition
from pywolf.models.pywolf.masters import MVoiceType
from pywolf.models.pywolf.masters import VOICE_TYPE_ID

from pywolf.models.pywolf.transactions import Village
from pywolf.models.pywolf.transactions import VillageParticipant
from pywolf.models.pywolf.transactions import VillageParticipantVoice
from pywolf.models.pywolf.transactions import VillageParticipantVoiceStatus
from pywolf.models.pywolf.transactions import VillageVoiceSetting
from pywolf.models.pywolf.transactions import VillageParticipantExeAbility
from pywolf.models.pywolf.transactions import PLAccount

import hashlib


def entry(request, village_no):
    """入村処理"""
    village = get_object_or_404(Village, pk=village_no)  # 村情報

    # 入村パスワードチェック
    if village.into_password:
        password = hashlib.sha256(request.POST['into_password'].encode('utf-8')).hexdigest()
        if village.into_password != password:
            request.session['entry_message'] = '入村パスワードの入力が間違っています。'
            # 村メイン画面に戻る
            return HttpResponseRedirect(reverse('pywolf:village', args=(village_no, 0,)))

    if request.session.get('entry_message', False):
        del request.session['entry_message']

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

    participant.chip = MChip.objects.get(pk=request.POST['chips'])
    participant.description = request.POST['description']
    participant.character_name = request.POST['character_name']
    participant.wish_position = MPosition.objects.get(pk=request.POST['wish_position'])
    participant.position = None
    participant.status = 0
    participant.win_lose_class = 0

    # 村建てフラグの設定
    if participant.pl == village.village_master_account:
        participant.village_denominated_flg = True

    participant.save()

    # 「X人目、○○○○○」
    sys_user = village.villageparticipant_set.get(pl=PLAccount.objects.get(system_user_flg=True))
    type_system = MVoiceType.objects.get(pk=VOICE_TYPE_ID['system'])

    sys_voice = VillageParticipantVoice()
    sys_voice.village_no = village
    sys_voice.day_no = 0
    sys_voice.village_participant = sys_user
    if(village.villageparticipantvoice_set.exists()):
        lastvoice = village.villageparticipantvoice_set.filter(voice_type_id=VOICE_TYPE_ID['system']).order_by('-voice_number')
        if lastvoice:
            sys_voice.voice_number = lastvoice[0].voice_number + 1

        lastvoice_order = \
            village.villageparticipantvoice_set.order_by('-voice_order')[0]
        sys_voice.voice_order = lastvoice_order.voice_order + 1
    else:
        sys_voice.voice_number = 0
        sys_voice.voice_order = 0

    sys_voice.use_point = 0
    sys_voice.voice_datetime = datetime.now()
    sys_voice.good_pl = ''
    sys_voice.voice_type = type_system
    sys_voice.voice = '{}人目、{} {}'.format(
        village.villageparticipant_set.filter(
            pl__system_user_flg=False, pl__dummy_user_flg=False, cancel_flg=False, delete_flg=False
        ).count() + 1, participant.description, participant.character_name)
    sys_voice.system_voice_flg = True
    sys_voice.save()

    # 第１発言登録
    voice = VillageParticipantVoice()
    voice.village_no = village
    voice.village_participant = participant
    voice.voice_type = MVoiceType.objects.get(pk=VOICE_TYPE_ID['normal'])

    lastvoice = village.villageparticipantvoice_set.filter(voice_type_id=VOICE_TYPE_ID['normal']).order_by(
        '-voice_number')
    if lastvoice:
        voice.voice_number = lastvoice[0].voice_number + 1
    else:
        voice.voice_number = 0

    voice.voice_order = sys_voice.voice_order + 1
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
