from ..models.pywolf.masters import MStyleSheetSet
from ..models.pywolf.masters import MStyleSheet
from ..models.pywolf.masters import MVoiceType

from ..models.pywolf.transactions import Village
from ..models.pywolf.transactions import VillageParticipantVoice

from datetime import datetime


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


def save_voice(village_no, pl, day_no, voice_type_key, voice_str, system_voice_flg=False):
    """発言作成登録"""

    village = Village.objects.get(pk=village_no)

    voice = VillageParticipantVoice()
    voice.village_no = village
    voice.village_participant = village.villageparticipant_set.get(pl=pl, cancel_flg=False)
    voice.day_no = day_no
    voice.voice_type = MVoiceType.objects.get(pk=voice_type_key)

    if village.villageparticipantvoice_set.exists():
        lastvoice = village.villageparticipantvoice_set.filter(voice_type_id=voice_type_key).order_by('-voice_number')
        print(lastvoice)
        if lastvoice:
            voice.voice_number = lastvoice[0].voice_number + 1
        else:
            voice.voice_number = 0

        lastvoice_order = \
            village.villageparticipantvoice_set.order_by('-voice_order')[0]
        voice.voice_order = lastvoice_order.voice_order + 1
    else:
        voice.voice_number = 0
        voice.voice_order = 0

    # 発言pt算出

    voice.use_point = 0
    voice.voice = voice_str
    voice.voice_datetime = datetime.now()
    voice.system_voice_flg=system_voice_flg

    voice.save()

    return voice.user_point
