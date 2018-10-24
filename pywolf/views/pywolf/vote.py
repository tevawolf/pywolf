from django.http import HttpResponseRedirect
from django.urls import reverse

from ...models.pywolf.transactions import VillageParticipant
from ...models.pywolf.transactions import VillageParticipantExeAbility

import hashlib


def vote(request, village_no, day_no):
    vote_id = request.POST['vote']
    login_id = request.session.get('login_id', False)
    participant = VillageParticipant.objects.get(village_no=village_no, pl=login_id)
    ability = VillageParticipantExeAbility.objects.get(village_participant=participant, day_no=day_no)

    ability.vote = hashlib.sha256(vote_id.encode('utf-8')).hexdigest()

    ability.save()

    # 村メイン画面に戻る
    return HttpResponseRedirect(reverse('pywolf:village', args=(village_no, day_no)))