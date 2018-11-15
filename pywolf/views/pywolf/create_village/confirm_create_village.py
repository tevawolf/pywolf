from django.shortcuts import render

from pywolf.common.common import get_stylesheet
from pywolf.models.pywolf.transactions import Village

from pywolf.forms.pywolf.create_village_form import VillageForm

import hashlib


def confirm_create_village(request):
    """村の作成　入力内容確認"""

    # スタイルシート設定
    stylesheet = get_stylesheet(request)

    form = VillageForm(request.POST)
    is_valid = form.is_valid()

    # セレクトボックスの選択値は文字列に変換
    start_class_str = get_choice_str(Village.START_CLASS, form.cleaned_data['start_class'])
    update_interval_str = get_choice_str(Village.UPDATE_INTERVAL, form.cleaned_data['update_interval'])
    voice_number_class_str = get_choice_str(Village.VOICE_NUMBER_CLASS, form.cleaned_data['voice_number_class'])

    # パスワード設定あり／なし
    hidden_password = ''
    password_setting = 'なし'
    if form.cleaned_data['into_password']:
        password_setting = 'あり'
        hidden_password = hashlib.sha256(form.cleaned_data['into_password'].encode('utf-8')).hexdigest()

    context = {
        'stylesheet': stylesheet,
        'form': form,
        'start_class_str': start_class_str,
        'update_interval_str': update_interval_str,
        'voice_number_class_str': voice_number_class_str,
        'hidden_password': hidden_password,
        'password_setting': password_setting,
    }

    if not is_valid:
        return render(request, 'pywolf/create_village/create_village.html', context)
    else:
        return render(request, 'pywolf/create_village/confirm_create_village.html', context)


def get_choice_str(choice, data):
    for c in choice:
        if c[0] == data:
            return c[1]
