from django.shortcuts import render

from ...models.pywolf.masters import VOICE_TYPE_ID


def confirm(request, village_no, day_no):
    '''発言内容の確認画面に遷移'''

    v = request.POST['voice']
    vt = request.POST['voice_type']
    chip_pass = request.POST['chip_pass']

    # 発言内容、発言種類、発言種類区分のディクショナリを渡す
    return render(request, "pywolf/confirm.html",
                  {'village_no': village_no,
                   'day_no': day_no,
                   'voice': v,
                   'voice_type': vt,
                   'chip_pass': chip_pass,
                   'VOICE_TYPE_ID_NORMAL': str(VOICE_TYPE_ID['normal']),
                   'VOICE_TYPE_ID_WOLF': str(VOICE_TYPE_ID['wolf']),
                   'VOICE_TYPE_ID_SELF': str(VOICE_TYPE_ID['self']),
                   'VOICE_TYPE_ID_GRAVE': str(VOICE_TYPE_ID['grave']),
                   }
                  )