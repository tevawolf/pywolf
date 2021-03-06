from django.shortcuts import render

from pywolf.enums import VoiceTypeId


def confirm_voice(request, village_no, day_no):
    """発言内容の確認画面に遷移"""

    v = request.POST['voice']
    vt = request.POST['voice_type']
    chip_width = request.POST['chip_width']
    chip_height = request.POST['chip_height']
    chip_pass = request.POST['chip_pass']

    # 発言内容、発言種類、発言種類区分のディクショナリを渡す
    return render(request, "pywolf/confirm_voice.html",
                  {'village_no': village_no,
                   'day_no': day_no,
                   'voice': v,
                   'voice_type': vt,
                   'chip_width': chip_width,
                   'chip_height': chip_height,
                   'chip_pass': chip_pass,
                   'VOICE_TYPE_ID_NORMAL': str(VoiceTypeId.NORMAL.value),
                   'VOICE_TYPE_ID_WOLF': str(VoiceTypeId.WOLF.value),
                   'VOICE_TYPE_ID_SELF': str(VoiceTypeId.SELF.value),
                   'VOICE_TYPE_ID_GRAVE': str(VoiceTypeId.GRAVE.value),
                   }
                  )