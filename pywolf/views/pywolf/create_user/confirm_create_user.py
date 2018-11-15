from django.shortcuts import render

from pywolf.common.common import get_stylesheet

from pywolf.forms.pywolf.create_user_form import PLAccountForm

import hashlib


def confirm_create_user(request):
    """ユーザー作成　入力内容確認"""

    # スタイルシート設定
    stylesheet = get_stylesheet(request)

    form = PLAccountForm(request.POST)
    is_valid = form.is_valid()

    # パスワード設定あり／なし
    hidden_password = ''
    if form.cleaned_data['password']:
        hidden_password = hashlib.sha256(form.cleaned_data['password'].encode('utf-8')).hexdigest()

    context = {
        'stylesheet': stylesheet,
        'form': form,
        'hidden_password': hidden_password,
    }

    if not is_valid:
        return render(request, 'pywolf/create_user/create_user.html', context)
    else:
        return render(request, 'pywolf/create_user/confirm_create_user.html', context)
