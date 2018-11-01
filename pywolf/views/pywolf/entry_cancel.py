from ...models.pywolf.transactions import VillageParticipant

from django.http import HttpResponseRedirect
from django.urls import reverse


def entry_cancel(request, village_no):
    """退村処理"""
    participant = VillageParticipant.objects \
        .filter(village_no=village_no, pl=request.session['login_id']).order_by('-sequence')[0]

    participant.cancel_flg = True

    participant.save()

    # 村メイン画面に戻る
    return HttpResponseRedirect(reverse('pywolf:village', args=(village_no, 0,)))
