from django.shortcuts import render
from django.shortcuts import get_object_or_404

from ...models.pywolf.transactions import Village
from ...models.pywolf.transactions import VillageProgress
from ...models.pywolf.transactions import VillageParticipantExeAbility
from ...models.pywolf.masters import VOICE_TYPE_ID
from ...models.pywolf.masters import MPositionVoiceSetting


def village(request, village_no, day_no):
    '''村メイン画面表示'''

    # 各種情報取得
    # get_object_or_404ではエラーメッセージをカスタマイズできない？？
    village = get_object_or_404(Village, pk=village_no)  # 村情報
    parts = village.villageparticipant_set.filter(village_no=village_no, system_user_flg=False).order_by('id')  # 参加者情報
    voices = village.villageparticipantvoice_set.filter(day_no=day_no).order_by('voice_order')  # 発言
    progress = get_object_or_404(VillageProgress, pk=village_no)  # 村進行情報
    # プロローグの場合、村役職情報（まだ未決定のもののみ）
    # 村の最大人数で、村編成セットから設定役職を重複なしで取得する

    # ログインユーザーの村参加情報取得
    login_user = request.session.get('login_user', False)
    login_id = request.session.get('login_id', False)
    login_message = request.session.get('login_message', '')  # ログインエラーメッセージ
    if login_message:
        del request.session['login_message']

    vs = {}
    normal_voice_mode = 0
    wolf_voice_mode = 0
    self_voice_mode = 0
    system_message_mode = 0
    grave_voice_mode = 0
    vote = ''
    if login_id:
        # ログインプレイヤーの村参加情報を取得
        try:
            particant = village.villageparticipant_set.get(village_no=village_no, pl=login_id)

            # 役職別発言設定を取得
            voice_settings = MPositionVoiceSetting.objects.filter(position=particant.position)
            for s in voice_settings:
                # 人狼発言
                if s.voice_type.id == VOICE_TYPE_ID['normal']:
                    normal_voice_mode = s.speech_hear_mode
                # 人狼発言
                elif s.voice_type.id == VOICE_TYPE_ID['wolf']:
                    wolf_voice_mode = s.speech_hear_mode
                # 独り言
                elif s.voice_type.id == VOICE_TYPE_ID['self']:
                    self_voice_mode = s.speech_hear_mode
                # 墓下発言
                elif s.voice_type.id == VOICE_TYPE_ID['grave']:
                    grave_voice_mode = s.speech_hear_mode
            # 能力行使先を取得
            try:
                ability = VillageParticipantExeAbility.objects.get(
                    village_participant=particant, day_no=day_no)
                vote = village.villageparticipant_set.get(village_no=village_no, pl=ability.vote).character_name
            except:
                pass
        except:
            particant = False
    else:
        particant = False

    return render(request, "pywolf/village.html",
                  {'village': village,                       # 村情報
                   'day_no': day_no,                         # 日数
                   'voices': voices,                         # 発言
                   'login_user': login_user,                # ログインユーザ名
                   'login_message': login_message,          # ログインエラーメッセージ
                   'particant': particant,                  # ログインユーザ参加者情報
                   'normal_voice_mode': normal_voice_mode,  # 通常発言モード
                   'wolf_voice_mode': wolf_voice_mode,      # 人狼発言モード
                   'self_voice_mode': self_voice_mode,      # 独り言発言モード
                   'grave_voice_mode': grave_voice_mode,    # 墓下発言モード
                   'VOICE_TYPE_ID': VOICE_TYPE_ID,          # 発言種別IDディクショナリ
                   'parts': parts,                           # 村参加者情報
                   'vote': vote,                             # ログインユーザ能力行使セット情報
                   'progress': progress,                    # 村進行情報
                   }
                  )
