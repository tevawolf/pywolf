from datetime import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse

from pywolf.models.pywolf.masters import MChip
from pywolf.models.pywolf.masters import MPosition
from pywolf.models.pywolf.masters import MVoiceType

from pywolf.models.pywolf.transactions import Village
from pywolf.models.pywolf.transactions import VillageParticipant
from pywolf.models.pywolf.transactions import VillageParticipantVoice
from pywolf.models.pywolf.transactions import VillageParticipantVoiceStatus
from pywolf.models.pywolf.transactions import VillageVoiceSetting
from pywolf.models.pywolf.transactions import VillageParticipantExeAbility
from pywolf.models.pywolf.transactions import PLAccount

from pywolf.enums import VoiceTypeId

from ....common.common import save_voice

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
    type_system = MVoiceType.objects.get(pk=VoiceTypeId.SYSTEM.value)

    save_voice(village_no=village, day_no=0, pl=sys_user, voice_type_key=type_system,
               voice_str='{}人目、{} {}'.format(
                    village.villageparticipant_set.filter(
                        pl__system_user_flg=False, pl__dummy_user_flg=False, cancel_flg=False, delete_flg=False
                    ).count() + 1, participant.description, participant.character_name),
               system_voice_flg=True)

    # 第１発言登録
    save_voice(village_no=village, day_no=0, pl=participant, voice_type_key=MVoiceType.objects.get(pk=VoiceTypeId.NORMAL.value),
               voice_str=request.POST['voice'])

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
