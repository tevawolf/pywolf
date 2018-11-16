from django.shortcuts import render
from django.db.models import Q

from pywolf.forms.pywolf.create_village_form import VillageForm
from pywolf.models.pywolf.transactions import Village
from pywolf.models.pywolf.transactions import VillageVoiceSetting
from pywolf.models.pywolf.transactions import VillageProgress
from pywolf.models.pywolf.transactions import VillageParticipant
from pywolf.models.pywolf.transactions import VillageParticipantVoice
from pywolf.models.pywolf.transactions import PLAccount
from pywolf.models.pywolf.masters import MStyleSheetSet
from pywolf.models.pywolf.masters import MVoiceSetting
from pywolf.models.pywolf.masters import MVoiceType
from pywolf.models.pywolf.masters import MPosition

from pywolf.common.common import get_stylesheet
from pywolf.common.common import get_login_info
from pywolf.common.common import save_voice

from pywolf.enums import VoiceTypeId
from pywolf.enums import VillageStatus

from datetime import date
from datetime import datetime
from datetime import timedelta


def exe_create_village(request):
    """村の作成　情報登録"""

    # スタイルシート設定
    stylesheet = get_stylesheet(request)

    # 上限オーバーチェック
    LIMIT = 4
    if VillageProgress.objects.latest().exclide(
            Q(village_status=VillageStatus.END) | Q(village_status=VillageStatus.ABOLITION)) > LIMIT:
        context = {
            'village': '',
            'error_message': '村の作成数の上限を超えたため、村の作成ができませんでした。<br/>申し訳ありませんが、ほかの村が終了するのをお待ちください。',
            'stylesheet': stylesheet,
        }
        return render(request, 'pywolf/create_village/complete_create_village.html', context)

    form = VillageForm(request.POST)
    if form.is_valid():
        non_save_village = form.save(commit=False)
        non_save_village.village_master_account = PLAccount.objects.get(id=request.session['login_id'])
        non_save_village.update_time = datetime(date.today().year, date.today().month, date.today().day,
                                                int(form.cleaned_data['update_time_hour']),
                                                int(form.cleaned_data['update_time_minute']), 0).time()
        non_save_village.abolition_date = date.today() + timedelta(days=14)
        non_save_village.chip_set = form.cleaned_data['chip_set']
        # デフォルトのダミー設定
        # オプションで、ダミーキャラと発言を村建てが設定可能にする
        for chip in non_save_village.chip_set.mchip_set.all():
            if chip.dummy_flg:
                non_save_village.dummy_character = chip
        non_save_village.system_message = form.cleaned_data['system_message']
        non_save_village.organization_setting = form.cleaned_data['organization_setting']
        non_save_village.save()

        # 登録したての村情報を取得
        new_village = Village.objects.latest()

        # 発言設定登録
        mvs = MVoiceSetting.objects.filter(pk=form.cleaned_data['voice_setting_set'].id)
        for vs in mvs:
            voice_setting = VillageVoiceSetting()
            voice_setting.village_no = new_village
            voice_setting.voice_type = vs.voice_type
            voice_setting.voice_number = vs.voice_number
            voice_setting.max_str_length = vs.max_str_length
            voice_setting.voice_point = vs.voice_point
            voice_setting.max_voice_point = vs.max_voice_point
            voice_setting.save()

        # 村進行情報作成
        progress = VillageProgress()
        progress.village_no = new_village
        progress.day_no = 0
        progress.village_status = VillageStatus.PROLOGUE
        progress.next_update_datetime = datetime(new_village.start_scheduled_date.year,
                                                 new_village.start_scheduled_date.month,
                                                 new_village.start_scheduled_date.day,
                                                 new_village.update_time.hour,
                                                 new_village.update_time.minute,
                                                 new_village.update_time.second) + \
                                        timedelta(hours=new_village.update_interval)
        progress.update_processing_lock = False
        progress.save()

        # システム参加者
        sys_user = VillageParticipant()
        sys_user.village_no = new_village
        sys_user.character_name = 'システム'
        sys_user.pl = PLAccount.objects.get(system_user_flg=True)
        sys_user.chip = new_village.dummy_character
        sys_user.wish_position = MPosition.objects.get(pk=1)
        sys_user.save()

        type_system = MVoiceType.objects.get(pk=VoiceTypeId.SYSTEM)

        # 最初のシステム発言作成
        save_voice(village_no=new_village, day_no=0, pl=sys_user, voice_type_key=type_system,
                   voice_str=new_village.system_message.msysmessage_set.get(sequence_number=0).message,
                   system_voice_flg=True)

        # 「1人目、○○○○○」
        save_voice(village_no=new_village, day_no=0, pl=sys_user, voice_type_key=type_system,
                   voice_str='1人目、{} {}'.format(new_village.dummy_character.description, new_village.dummy_character.character_name),
                   system_voice_flg=True)

        # 最初のダミー発言作成
        dummy_user = VillageParticipant()
        dummy_user.village_no = new_village
        dummy_user.description = new_village.dummy_character.description
        dummy_user.character_name = new_village.dummy_character.character_name
        dummy_user.pl = PLAccount.objects.get(dummy_user_flg=True)
        dummy_user.chip = new_village.dummy_character
        dummy_user.wish_position = MPosition.objects.get(pk=1)
        dummy_user.save()
        save_voice(village_no=new_village, day_no=0, pl=dummy_user, voice_type_key=MVoiceType.objects.get(pk=VoiceTypeId.NORMAL),
                   voice_str=new_village.dummy_character.dummy_voice_pro,
                   system_voice_flg=True)

        context = {
            'village': new_village,
            'stylesheet': stylesheet,
        }
        return render(request, 'pywolf/create_village/complete_create_village.html', context)

    else:
        # ログイン情報取得
        login_info = get_login_info(request)
        # スタイルシート設定
        stylesheet_set = MStyleSheetSet.objects.filter(delete_flg=False)
        context = {
            'login_info': login_info,
            'stylesheet_set': stylesheet_set,
            'stylesheet': stylesheet,
            'form': form,
        }
        return render(request, 'pywolf/create_village/create_village.html', context)
