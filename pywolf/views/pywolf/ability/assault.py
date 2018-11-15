from django.http import HttpResponseRedirect
from django.urls import reverse

from pywolf.models.pywolf.transactions import VillageParticipant
from pywolf.models.pywolf.transactions import VillageParticipantExeAbility

import hashlib


def assault(request, village_no, day_no):
    """襲撃セット処理"""
    assault_id = request.POST['assault']
    login_id = request.session.get('login_id', False)
    participant = VillageParticipant.objects.get(village_no=village_no, pl=login_id, cancel_flg=False)
    ability = VillageParticipantExeAbility.objects.get(village_participant_id=participant.id, day_no=day_no)

    ability.assault = hashlib.sha256(assault_id.encode('utf-8')).hexdigest()

    ability.save()

    # 村メイン画面に戻る
    return HttpResponseRedirect(reverse('pywolf:village', args=(village_no, day_no)))
