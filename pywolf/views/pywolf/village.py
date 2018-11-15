from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from ...models.pywolf.transactions import Village
from ...models.pywolf.transactions import VillageProgress
from ...models.pywolf.masters import MVoiceType
from ...models.pywolf.masters import VOICE_TYPE_ID
from ...models.pywolf.masters import MPositionVoiceSetting
from ...models.pywolf.masters import MChip
from ...models.pywolf.masters import MPosition
from ...models.pywolf.masters import MStyleSheetSet
from ...models.pywolf.masters import MOrganizationPositionNumber
from ...common.common import get_stylesheet
from ...common.common import get_login_info
from ...common.update import update
from ...forms.pywolf.entry_form import EntryForm

from datetime import datetime
import pytz


def village(request, village_no, day_no):
    """村メイン画面表示"""

    # 更新するか判定
    prg = VillageProgress.objects.filter(village_no=village_no).latest()
    update_datetime = prg.next_update_datetime

    now = datetime.now()
    timezone = pytz.timezone('Asia/Tokyo')
    now = timezone.localize(now)

    if now > update_datetime:
        if prg.village_status != 3 and prg.village_status != 4:  # 終了か廃村していなければ
            # 更新実行して、そのままログ取得＆表示へ
            update(village_no, day_no)

    # 各種情報取得
    # get_object_or_404ではエラーメッセージをカスタマイズできない？？
    village = get_object_or_404(Village, pk=village_no)  # 村情報
    progress = village.villageprogress_set.latest()  # 村進行情報(現在の）
    parts = village.villageparticipant_set.filter(pl__system_user_flg=False, pl__dummy_user_flg=False, cancel_flg=False, delete_flg=False).order_by('id')  # 参加者（投票・能力行使先）
    voices = village.villageparticipantvoice_set.filter(day_no=day_no, delete_flg=False).order_by('voice_order')  # 発言
    days = village.villageprogress_set.all()  # 村進行情報(すべて）
    chips = MChip.objects.filter(chip_set_id=village.chip_set_id, dummy_flg=False, delete_flg=False)

    # プロローグの場合、村役職情報（希望役職選択に使う）
    # positions = []
    # if progress.village_status == 0:
    #     try:
    #         orgset = village.villageorganizationsetting_set.get()
    #         # 村編成設定から設定役職を取得する
    #         organizations = orgset.villageorganization_set.get()
    #     except ObjectDoesNotExist:
    #         # 編成マスタ情報から編成に含まれる役職を取得する
    #         organizations = MOrganizationPositionNumber.objects.filter(organization_id=village.organization_setting)
    #     for org in organizations:
    #         positions.append(MPosition.objects.get(pk=org.position_id_id))

    # ログインユーザーの村参加情報取得
    login_info = get_login_info(request)

    vote = ''
    fortune = {}
    fortune_set = None
    guard = {}
    assault = {}
    assault_set = None
    voice_settings = False

    if login_info['login_id']:
        # ログインプレイヤーの村参加情報を取得
        try:
            login_participant = village.villageparticipant_set.get(pl=login_info['login_id'], cancel_flg=False, delete_flg=False)

            # ログインプレイヤーの役職の発言設定を取得
            voice_settings = MPositionVoiceSetting.objects.filter(position=login_participant.position).order_by('voice_type_id')
            for val in voice_settings:
                val.voice_type_name = MVoiceType.objects.get(pk=val.voice_type_id).voice_type_name
            try:
                # 投票セット済みなら、投票した相手の情報を取得
                today_ability = login_participant.villageparticipantexeability_set.get(day_no=day_no)
                if today_ability.vote:
                    vote = village.villageparticipant_set.get(pl=today_ability.vote, cancel_flg=False)

                # すべての日の能力行使情報を取得
                all_ability = login_participant.villageparticipantexeability_set.all()
                for i, ability in enumerate(all_ability):
                    # 襲撃
                    if ability.assault:
                        if i == day_no:
                            assault_set = village.villageparticipant_set.get(village_no=village_no, pl=ability.assault, cancel_flg=False)

                        assault[i] = village.villageparticipant_set.get(village_no=village_no, pl=ability.assault, cancel_flg=False)
                        if assault[i].status == 2:
                            assault[i].result = '殺害'
                        else:
                            assault[i].result = '失敗'
                    # 占い
                    if ability.fortune:
                        if i == day_no:
                            fortune_set = village.villageparticipant_set.get(village_no=village_no, pl=ability.fortune, cancel_flg=False)

                        fortune[i] = village.villageparticipant_set.get(village_no=village_no, pl=ability.fortune, cancel_flg=False)
                        fortune[i].result = village.villageparticipant_set.get(village_no=village_no, pl=ability.fortune, cancel_flg=False).position.position_name
                    # 護衛
                    if ability.guard:
                        guard[i] = village.villageparticipant_set.get(village_no=village_no, pl=ability.guard, cancel_flg=False).character_name
            except:
                pass
        except:
            login_participant = False
    else:
        login_participant = False

    # （この村の情報ではない）マスタ情報
    voice_type = MVoiceType.objects.filter(delete_flg=False)  # 発言種別情報

    # スタイル設定
    stylesheet_set = MStyleSheetSet.objects.filter(delete_flg=False)
    stylesheet = get_stylesheet(request)

    # 入村パスワードエラーメッセージ
    if request.session.get('entry_message', False):
        into_password_error_message = request.session['entry_message']
        del request.session['entry_message']
    else:
        into_password_error_message = ''

    # プロローグで、ログインしておりかつ参加していなければ、入村フォーム
    e_form = False
    if progress.village_status == 0 and login_info['login_id'] and not login_participant:
        # e_form = EntryForm(village_no)
        e_form = EntryForm(village_no)

    return render(request, "pywolf/village.html",
                  {'village': village,                       # 村情報
                   'day_no': day_no,                         # 日数（表示用）
                   'days': days,                            # 進行情報(すべての日）
                   'progress': progress,                    # 村進行情報(現在）
                   'voices': voices,                         # 発言
                   'login_info': login_info,                # ログイン情報
                   'participant': login_participant,         # ログインユーザ参加者情報
                   'voice_settings': voice_settings,        # 役職別発言設定
                   'voice_type': voice_type,                # 発言種別
                   'VOICE_TYPE_ID': VOICE_TYPE_ID,          # 発言種別IDディクショナリ
                   'parts': parts,                           # 村参加者（投票・能力行使先）
                   'vote': vote,                             # 投票セット情報
                   'assault_result': assault,               # 襲撃結果情報
                   'assault_set': assault_set,               # 襲撃セット情報
                   'fortune_result': fortune,               # 占い結果情報
                   'fortune_set': fortune_set,              # 占いセット情報
                   'guard': guard,                           # 護衛セット情報
                   'chips': chips,                          # チップセット
                   # 'positions': positions,                  # 村役職リスト
                   'stylesheet_set': stylesheet_set,       # スタイルシートセット
                   'stylesheet': stylesheet,                # スタイルシート
                   'into_password_error_message': into_password_error_message,  # 入村パスワードエラーメッセージ
                   'e_form': e_form,                          # 入村フォーム
                   }
                  )
