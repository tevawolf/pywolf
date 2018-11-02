from django.http import HttpResponseRedirect
from django.urls import reverse


def logout(request, village_no, day_no):
    """ログアウト"""

    del request.session['login_user']  # （仮実装）
    del request.session['login_id']

    if village_no == 0 and day_no == 0:
        # トップページに戻る  ★★もっといい方法はないものか・・・★★
        return HttpResponseRedirect(reverse('pywolf:index'))

    # 村メイン画面に戻る
    return HttpResponseRedirect(reverse('pywolf:village', args=(village_no, day_no,)))
