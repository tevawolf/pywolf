from django.shortcuts import render

from ...common.common import get_login_info
from ...models.pywolf.masters import MStyleSheetSet
from ...common.common import get_stylesheet
from ...models.pywolf.masters import MPosition

from ...forms.pywolf.create_village_form import VillageForm


def create_village(request):
    """村の作成ページ表示"""

    # ログイン情報取得
    login_info = get_login_info(request)

    # スタイルシート設定
    stylesheet_set = MStyleSheetSet.objects.filter(delete_flg=False)
    stylesheet = get_stylesheet(request)

    # マスタから値を取得する
    position = MPosition.objects.filter(delete_flg=False)

    form = VillageForm()

    context = {
        'login_info': login_info,
        'stylesheet_set': stylesheet_set,
        'stylesheet': stylesheet,
        'position': position,
        'form': form,
    }

    return render(request, 'pywolf/create_village.html', context)
