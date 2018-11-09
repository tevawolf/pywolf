from django.shortcuts import render
from ...forms.pywolf.create_village_form import VillageForm
from ...models.pywolf.transactions import Village
from ...models.pywolf.transactions import VillageVoiceSetting
from ...models.pywolf.transactions import VillageProgress
from ...models.pywolf.transactions import PLAccount
from ...models.pywolf.masters import MStyleSheetSet
from ...models.pywolf.masters import MVoiceSetting

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
        progress.save()

        # 最初のシステム・ダミー発言作成
        # チップセットマスタにダミー発言を持たせないと

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
