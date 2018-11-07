from django.http import HttpResponseRedirect
from django.urls import reverse

from ...models.pywolf.transactions import PLAccount

import hashlib


def login(request, village_no, day_no):
    """ログイン"""

    id = request.POST['id']
    password = request.POST['password']

    id = hashlib.sha256(id.encode('utf-8')).hexdigest()
    password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    try:
        account = PLAccount.objects.get(id=id, password=password)
    except:
        account = None

    if account is not None:
        request.session['login_user'] = account.id_view
        request.session['login_id'] = id
        if request.session.get('login_message', False):
            del request.session['login_message']
        request.session['stylesheet'] = account.select_style_id
    else:
        request.session['login_message'] = 'IDが存在しないか、passwordが間違っています。'

    if village_no == 0 and day_no == 0:
        # トップページに戻る  ★★もっといい方法はないものか・・・★★
        return HttpResponseRedirect(reverse('pywolf:index'))
    elif village_no == 999999 and day_no == 999999:
        # 村の作成ページに戻る  ★★もっといい方法はないものか・・・★★
        return HttpResponseRedirect(reverse('pywolf:create_village'))

    # 村メインページに戻る
    return HttpResponseRedirect(reverse('pywolf:village', args=(village_no, day_no,)))
