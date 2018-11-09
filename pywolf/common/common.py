from ..models.pywolf.masters import MStyleSheetSet
from ..models.pywolf.masters import MStyleSheet


def get_stylesheet(request):
    # スタイルシート設定
    if 'stylesheet' in request.session:
        sset = MStyleSheetSet.objects.get(id=request.session['stylesheet'], delete_flg=False)
    else:
        # セッションに設定がなければ、デフォルトのスタイルシートを指定する
        sset = MStyleSheetSet.objects.get(id=1)

    stylesheet = MStyleSheet.objects.filter(stylesheet_set_id=sset.id)

    return stylesheet


def get_login_info(request):
    """ログインユーザーの村参加情報取得"""
    login_user = request.session.get('login_user', False)
    login_id = request.session.get('login_id', False)
    login_message = request.session.get('login_message', '')  # ログインエラーメッセージ
    if login_message:
        del request.session['login_message']

    return {'login_user': login_user, 'login_id': login_id, 'login_message': login_message}
