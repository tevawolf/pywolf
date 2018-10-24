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
    else:
        request.session['login_message'] = 'IDが存在しないか、passwordが間違っています。'

    # 村メイン画面に戻る
    return HttpResponseRedirect(reverse('pywolf:village', args=(village_no, day_no,)))