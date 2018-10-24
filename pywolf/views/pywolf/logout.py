from django.http import HttpResponseRedirect
from django.urls import reverse


def logout(request, village_no, day_no):
    """ログアウト"""

    request.session.flush()  # （仮実装）

    # 村メイン画面に戻る
    return HttpResponseRedirect(reverse('pywolf:village', args=(village_no, day_no,)))