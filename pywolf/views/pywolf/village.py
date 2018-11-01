from django.shortcuts import render
from django.shortcuts import get_object_or_404

from ...models.pywolf.transactions import Village
from ...models.pywolf.transactions import VillageOrganizationSet
from ...models.pywolf.transactions import  VillageOrganization
from ...models.pywolf.transactions import VillageParticipantExeAbility
from ...models.pywolf.masters import MVoiceType
from ...models.pywolf.masters import VOICE_TYPE_ID
from ...models.pywolf.masters import MPositionVoiceSetting
from ...models.pywolf.masters import MChip
from ...models.pywolf.masters import MPosition


def village(request, village_no, day_no):
    """村メイン画面表示"""

    # 各種情報取得
    # get_object_or_404ではエラーメッセージをカスタマイズできない？？
    village = get_object_or_404(Village, pk=village_no)  # 村情報
    parts = village.villageparticipant_set.filter(village_no=village_no, system_user_flg=False, cancel_flg=False).order_by('id')  # 参加者（投票・能力行使先）
    voices = village.villageparticipantvoice_set.filter(day_no=day_no).order_by('voice_order')  # 発言
    progress = village.villageprogress_set.latest()  # 村進行情報(現在の）
    chips = MChip.objects.filter(chip_set_id=village.chip_set_id)  # 村チップセット情報
    voice_type = MVoiceType.objects.all()  # 発言種別情報

    # プロローグの場合、村役職情報
    positions = []
    if progress.village_status == 0:
        # 村の最大人数で、村編成セットから設定役職を重複なしで取得する
        orgset = get_object_or_404(VillageOrganizationSet, village_no_id=village_no)
        organizations = VillageOrganization.objects.filter(organization_id=orgset.id)
        for org in organizations:
            positions.append(MPosition.objects.get(id=org.position_id))

    # ログインユーザーの村参加情報取得
    login_user = request.session.get('login_user', False)
    login_id = request.session.get('login_id', False)
    login_message = request.session.get('login_message', '')  # ログインエラーメッセージ
    if login_message:
        del request.session['login_message']

    vote = ''
    fortune = {}
    fortune_result = {}
    guard = {}
    guard_result = {}
    assault = {}
    assault_result = {}
    voice_settings = False

    if login_id:
        # ログインプレイヤーの村参加情報を取得
        try:
            participant = village.villageparticipant_set.get(village_no=village_no, pl=login_id, cancel_flg=False)

            # 役職別発言設定を取得
            voice_settings = MPositionVoiceSetting.objects.filter(position=participant.position).order_by('voice_type_id')
            for val in voice_settings:
                val.voice_type_name = MVoiceType.objects.get(pk=val.voice_type_id).voice_type_name
            # 能力行使先を取得
            try:
                # 投票
                today_ability = VillageParticipantExeAbility.objects.get(village_participant=participant, day_no=day_no)
                if today_ability.vote:
                    vote = village.villageparticipant_set.get(village_no=village_no, pl=today_ability.vote, cancel_flg=False).character_name

                all_ability = VillageParticipantExeAbility.objects.filter(village_participant=participant)
                for i, ability in enumerate(all_ability):
                    # 襲撃
                    if ability.assault:
                        assault[i] = village.villageparticipant_set.get(village_no=village_no, pl=ability.assault, cancel_flg=False).character_name
                    # 占い
                    if ability.fortune:
                        fortune[i] = village.villageparticipant_set.get(village_no=village_no, pl=ability.fortune, cancel_flg=False).character_name
                        fortune_result[i] = village.villageparticipant_set.get(village_no=village_no, pl=ability.fortune, cancel_flg=False).position.position_name
                    # 護衛
                    if ability.guard:
                        guard[i] = village.villageparticipant_set.get(village_no=village_no, pl=ability.guard, cancel_flg=False).character_name
            except:
                pass
        except:
            participant = False
    else:
        participant = False

    return render(request, "pywolf/village.html",
                  {'village': village,                       # 村情報
                   'day_no': day_no,                         # 日数
                   'voices': voices,                         # 発言
                   'login_user': login_user,                # ログインユーザ名
                   'login_message': login_message,          # ログインエラーメッセージ
                   'participant': participant,              # ログインユーザ参加者情報
                   'voice_settings': voice_settings,        # 役職別発言設定
                   'voice_type': voice_type,                # 発言種別
                   'VOICE_TYPE_ID': VOICE_TYPE_ID,          # 発言種別IDディクショナリ
                   'parts': parts,                           # 村参加者（投票・能力行使先）
                   'vote': vote,                             # 投票セット情報
                   'assault': assault,                       # 襲撃セット情報
                   'fortune': fortune,                       # 占いセット情報
                   'fortune_result': fortune_result,                       # 占い結果情報
                   'guard': guard,                           # 護衛セット情報
                   'progress': progress,                    # 村進行情報
                   'chips': chips,                          # チップセット
                   'positions': positions,                  # 村役職リスト
                   'css': 'pywolf/standard.css',            # スタイルシート
                   'css_win': 'pywolf/voice_window.css',  # スタイルシート(窓)
                   'css_textarea': 'pywolf/voice_textarea.css',  # スタイルシート(発言窓)
                   }
                  )
