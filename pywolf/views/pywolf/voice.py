from django.http import HttpResponseRedirect
from django.urls import reverse

from ...models.pywolf.transactions import Village
from ...models.pywolf.transactions import VillageParticipant
from ...models.pywolf.transactions import VillageParticipantVoice
from ...models.pywolf.transactions import PLAccount
from ...models.pywolf.masters import MVoiceType

from datetime import datetime


def voice(request, village_no, day_no):
    '''発言を投稿して村メイン画面に戻る'''

    voice = VillageParticipantVoice()
    voice.village_no = Village.objects.get(pk=village_no)
    voice.village_participant = VillageParticipant.objects.get(pl=request.session['login_id'])
    voice.day_no = day_no
    vt = request.POST['voice_type']
    voice.voice_type = MVoiceType.objects.get(pk=vt)
    lastvoice = \
        Village.objects.get(pk=village_no). \
            villageparticipantvoice_set.order_by('-voice_number')[0]
    voice.voice_number = lastvoice.voice_number + 1
    voice.voice_order = lastvoice.voice_order + 1
    voice.use_point = 0
    v = request.POST['voice']
    voice.voice = v
    voice.good_pl = PLAccount.objects.get(pk=request.session['login_id'])
    voice.voice_datetime = datetime.now()
    voice.delete_flg = False
    voice.save()

    # 村メイン画面に戻る
    return HttpResponseRedirect(reverse('pywolf:village', args=(village_no, day_no,)))