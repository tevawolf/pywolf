from django.shortcuts import render

from ....common.common import get_stylesheet

from ....forms.pywolf.create_user_form import PLAccountForm


def create_user(request):
    """ユーザー作成ページ表示"""

    # スタイルシート設定
    stylesheet = get_stylesheet(request)

    form = PLAccountForm()

    context = {
        'stylesheet': stylesheet,
        'form': form,
    }

    return render(request, 'pywolf/create_user/create_user.html', context)
