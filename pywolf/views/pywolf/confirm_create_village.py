from django.shortcuts import render

from ...common.common import get_login_info
from ...models.pywolf.masters import MStyleSheetSet
from ...common.common import get_stylesheet

from ...forms.pywolf.create_village_form import VillageForm


def confirm_create_village(request):
    """村の作成　入力内容確認"""

    # ログイン情報取得
    login_info = get_login_info(request)

    # スタイルシート設定
    stylesheet_set = MStyleSheetSet.objects.filter(delete_flg=False)
    stylesheet = get_stylesheet(request)

    form = VillageForm(request.POST)
    is_valid = form.is_valid()

    context = {
        'login_info': login_info,
        'stylesheet_set': stylesheet_set,
        'stylesheet': stylesheet,
        'form': form,
    }

    if not is_valid:
        return render(request, 'pywolf/create_village.html', context)
    else:
        return render(request, 'pywolf/confirm_create_village.html', context)
