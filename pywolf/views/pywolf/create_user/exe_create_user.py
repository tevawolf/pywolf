from django.shortcuts import render
from pywolf.forms.pywolf.create_user_form import PLAccountForm
from pywolf.common.common import get_stylesheet

import hashlib


def exe_create_user(request):
    """ユーザー作成　情報登録"""

    # スタイルシート設定
    stylesheet = get_stylesheet(request)

    form = PLAccountForm(request.POST)
    if form.is_valid():
        non_save_user = form.save(commit=False)
        non_save_user.id = hashlib.sha256(form.cleaned_data['id_view'].encode('utf-8')).hexdigest()
        non_save_user.select_style = stylesheet[0].stylesheet_set
        non_save_user.system_user_flg = False
        non_save_user.dummy_user_flg = False
        non_save_user.delete_flg = False
        non_save_user.save()

        context = {
            'form': form,
            'stylesheet': stylesheet,
        }
        return render(request, 'pywolf/create_user/complete_create_user.html', context)

    else:
        context = {
            'stylesheet': stylesheet,
            'form': form,
        }
        return render(request, 'pywolf/create_user/create_user.html', context)
