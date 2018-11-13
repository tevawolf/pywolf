from django.shortcuts import render
from ...forms.pywolf.create_village_form import VillageForm
from ...models.pywolf.transactions import Village
from ...models.pywolf.transactions import VillageVoiceSetting
from ...models.pywolf.transactions import VillageProgress
from ...models.pywolf.transactions import VillageParticipant
from ...models.pywolf.transactions import VillageParticipantVoice
from ...models.pywolf.transactions import PLAccount
from ...models.pywolf.masters import MStyleSheetSet
from ...models.pywolf.masters import MVoiceSetting
from ...models.pywolf.masters import MVoiceType
from ...models.pywolf.masters import MPosition
from ...models.pywolf.masters import VOICE_TYPE_ID

from ...common.common import get_stylesheet
from ...common.common import get_login_info

from datetime import date
from datetime import datetime
from datetime import timedelta


def exe_create_village(request):
    """村の作成　情報登録"""

    # スタイルシート設定
    stylesheet = get_stylesheet(request)

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
        progress.village_status = 0
        progress.next_update_datetime = datetime(new_village.start_scheduled_date.year,
                                                 new_village.start_scheduled_date.month,
                                                 new_village.start_scheduled_date.day,
                                                 new_village.update_time.hour,
                                                 new_village.update_time.minute,
                                                 new_village.update_time.second) + \
                                        timedelta(hours=new_village.update_interval)
        progress.update_processing_lock = False
        progress.save()


        # 最初のシステム発言作成

        # システム参加者
        sys_user = VillageParticipant()
        sys_user.village_no = new_village
        sys_user.character_name = 'システム'
        sys_user.pl = PLAccount.objects.get(system_user_flg=True)
        sys_user.chip = new_village.dummy_character
        sys_user.wish_position = MPosition.objects.get(pk=1)
        sys_user.save()

        type_system = MVoiceType.objects.get(pk=VOICE_TYPE_ID['system'])

        sys_voice = VillageParticipantVoice()
        sys_voice.village_no = new_village
        sys_voice.day_no = 0
        sys_voice.village_participant = sys_user
        sys_voice.voice_number = 0
        sys_voice.use_point = 0
        sys_voice.voice_datetime = datetime.now()
        sys_voice.good_pl = ''
        sys_voice.voice_type = type_system
        sys_voice.voice = new_village.system_message.msysmessage_set.get(sequence_number=0).message
        sys_voice.system_voice_flg = True
        sys_voice.voice_order = 0
        sys_voice.save()
        # 「1人目、○○○○○」
        sys_voice1 = VillageParticipantVoice()
        sys_voice1.village_no = new_village
        sys_voice1.day_no = 0
        sys_voice1.village_participant = sys_user
        sys_voice1.voice_number = 1
        sys_voice1.use_point = 0
        sys_voice1.voice_datetime = datetime.now()
        sys_voice1.good_pl = ''
        sys_voice1.voice_type = type_system
        sys_voice1.voice = '1人目、{}'.format(new_village.dummy_character.character_name)
        sys_voice1.system_voice_flg = True
        sys_voice1.voice_order = 1
        sys_voice1.save()

        # 最初のダミー発言作成

        # ダミー参加者
        dummy_user = VillageParticipant()
        dummy_user.village_no = new_village
        dummy_user.character_name = new_village.dummy_character.character_name
        dummy_user.pl = PLAccount.objects.get(dummy_user_flg=True)
        dummy_user.chip = new_village.dummy_character
        dummy_user.wish_position = MPosition.objects.get(pk=1)
        dummy_user.save()

        dummy_voice = VillageParticipantVoice()
        dummy_voice.village_no = new_village
        dummy_voice.day_no = 0
        dummy_voice.village_participant = dummy_user
        dummy_voice.voice_number = 0
        dummy_voice.use_point = 0
        dummy_voice.voice_datetime = datetime.now()
        dummy_voice.good_pl = ''
        dummy_voice.voice_type = MVoiceType.objects.get(pk=VOICE_TYPE_ID['normal'])
        dummy_voice.voice = new_village.dummy_character.dummy_voice_pro
        dummy_voice.system_voice_flg = True
        dummy_voice.voice_order = 2
        dummy_voice.save()

        context = {
            'village': new_village,
            'stylesheet': stylesheet,
        }
        return render(request, 'pywolf/complete_create_village.html', context)

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
        return render(request, 'pywolf/create_village.html', context)
