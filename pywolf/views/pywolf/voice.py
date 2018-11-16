from django.http import HttpResponseRedirect
from django.urls import reverse
from ...models.pywolf.transactions import Village

from ...common.common import save_voice
from pywolf.enums import VoiceNumberClass


def voice(request, village_no, day_no):
    """発言を投稿して村メイン画面に戻る"""

    use_point = save_voice(village_no=village_no, day_no=day_no,
                           pl=request.session['login_id'],
                           voice_type_key=request.POST['voice_type'],
                           voice_str=request.POST['voice'])

    # 発言数 or 発言pt　消費
    village = Village.objects.get(village_no=village_no)
    voice_status = village._villageparticipant_set.get(pl=request.session['login_id'], cancel_flg=False)
    if village.voice_number_class == VoiceNumberClass.COUNT:
        pass

    # 村メイン画面に戻る
    return HttpResponseRedirect(reverse('pywolf:village', args=(village_no, day_no,)))

