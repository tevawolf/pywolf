from django.shortcuts import render

from ...models.pywolf.transactions import Village
from ...models.pywolf.transactions import PLAccount
from ...models.pywolf.masters import MStyleSheetSet
from ...common.common import get_stylesheet
from ...common.common import get_login_info


def index(request):
    """トップページ表示"""
    pl_list = PLAccount.objects.filter(delete_flg=False).order_by('id')
    village_list = Village.objects.filter(delete_flg=False).order_by('village_no')

    # ログイン情報取得
    login_info = get_login_info(request)

    # スタイルシート設定
    stylesheet_set = MStyleSheetSet.objects.filter(delete_flg=False)
    stylesheet = get_stylesheet(request)

    context = {
        'village_list': village_list,
        'pl_list': pl_list,
        'login_info': login_info,
        'stylesheet_set': stylesheet_set,
        'stylesheet': stylesheet
    }
    return render(request, 'pywolf/index.html', context)
