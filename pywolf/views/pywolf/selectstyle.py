from ...models.pywolf.transactions import PLAccount

from django.http import HttpResponseRedirect
from django.urls import reverse


def selectstyle(request, village_no, day_no):
    """スタイルシート選択"""

    # セッションに選択したスタイルシートセットを保持
    set_id = request.POST['stylesheet']
    request.session['stylesheet'] = set_id

    # ログインしていたら、PLアカウントにもスタイルシートセットを保存
    if 'login_id' in request.session:
        pl = PLAccount.objects.get(id=request.session['login_id'])
        pl.select_style_id = set_id
        pl.save()

    if village_no == 0 and day_no == 0:
        # トップページに戻る  ★★もっといい方法はないものか・・・★★
        return HttpResponseRedirect(reverse('pywolf:index'))

    # 村メイン画面に戻る
    return HttpResponseRedirect(reverse('pywolf:village', args=(village_no, day_no,)))
