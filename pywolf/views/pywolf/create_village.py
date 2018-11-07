from django.shortcuts import render

from ...common.common import get_login_info
from ...models.pywolf.masters import MStyleSheetSet
from ...common.common import get_stylesheet
from ...models.pywolf.masters import MChipSet
from ...models.pywolf.masters import MSysMessageSet

from ...models.pywolf.transactions import START_CLASS
from ...models.pywolf.transactions import UPDATE_INTERVAL
from ...models.pywolf.transactions import VOICE_NUMBER_CLASS


def create_village(request):

    # ログイン情報取得
    login_info = get_login_info(request)

    # スタイルシート設定
    stylesheet_set = MStyleSheetSet.objects.all()
    stylesheet = get_stylesheet(request)

    # 日時プルダウンの作成
    hour = [h for h in range(0, 24)]
    minute = [m for m in range(0, 60, 15)]

    # マスタから値を取得する
    chipset = MChipSet.objects.filter(delete_flg=False)
    system_message = MSysMessageSet.objects.filter(delete_flg=False)

    context = {
        'login_info': login_info,
        'stylesheet_set': stylesheet_set,
        'stylesheet': stylesheet,
        'START_CLASS': START_CLASS,
        'update_time_hour': hour,
        'update_time_minute': minute,
        'UPDATE_INTERVAL': UPDATE_INTERVAL,
        'VOICE_NUMBER_CLASS': VOICE_NUMBER_CLASS,
        'chipset': chipset,
        'system_message': system_message,
    }

    return render(request, 'pywolf/create_village.html', context)
