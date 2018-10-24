from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models.pywolf.transactions import Village
from .models.pywolf.transactions import VillageParticipant
from .models.pywolf.transactions import VillageParticipantVoice
from .models.pywolf.transactions import VillageParticipantExeAbility
from .models.pywolf.transactions import PLAccount
from .models.pywolf.masters import MVoiceType
from .models.pywolf.masters import VOICE_TYPE_ID
from .models.pywolf.masters import MPositionVoiceSetting

from datetime import datetime
import hashlib


# def index(request):
#     '''トップページ表示'''
#     pl_list = PLAccount.objects.order_by('id')
#     village_list = Village.objects.order_by('village_no')
#     context = {'village_list': village_list, 'pl_list': pl_list}
#     return render(request, 'pywolf/index.html', context)


# def village(request, village_no, day_no):
#     '''村メイン画面表示'''
#
#     # 発言取得
#     # get_object_or_404ではエラーメッセージをカスタマイズできない？？
#     village = get_object_or_404(Village, pk=village_no)
#     parts = village.villageparticipant_set.filter(village_no=village_no).order_by('id')
#     voices = village.villageparticipantvoice_set.filter(day_no=day_no)
#
#     # ログインユーザーの村参加情報取得
#     login_user = request.session.get('login_user', False)
#     login_id = request.session.get('login_id', False)
#     vs = {}
#     normal_voice_flg = 0
#     wolf_voice_flg = 0
#     self_voice_flg = 0
#     vote = ''
#     if login_id:
#         particant = village.villageparticipant_set.get(village_no=village_no, pl=login_id)
#         # 役職別発言設定を取得
#         voice_settings = MPositionVoiceSetting.objects.filter(position=particant.position)
#         for s in voice_settings:
#             # 人狼発言
#             if s.voice_type.id == VOICE_TYPE_ID['normal']:
#                 normal_voice_flg = s.speech_hear_mode
#             # 人狼発言
#             elif s.voice_type.id == VOICE_TYPE_ID['wolf']:
#                 wolf_voice_flg = s.speech_hear_mode
#             # 独り言
#             elif s.voice_type.id == VOICE_TYPE_ID['self']:
#                 self_voice_flg = s.speech_hear_mode
#         # 能力行使先を取得
#         try:
#             ability = VillageParticipantExeAbility.objects.get(
#                 village_participant=particant, day_no=day_no)
#             vote = village.villageparticipant_set.get(village_no=village_no, pl=ability.vote).character_name
#         except:
#             pass
#     else:
#         particant = False
#
#     return render(request, "pywolf/village.html",
#                   {'village': village,
#                    'day_no': day_no,
#                    'voices': voices,
#                    'login_user' : login_user,
#                    'particant' : particant,
#                    'normal_voice_flg' : normal_voice_flg,
#                    'wolf_voice_flg' : wolf_voice_flg,
#                    'self_voice_flg' : self_voice_flg,
#                    'VOICE_TYPE_ID' : VOICE_TYPE_ID,
#                    'parts': parts,
#                    'vote': vote,
#                    }
#                   )



# def voice(request, village_no, day_no):
#     '''発言を投稿して村メイン画面に戻る'''
#
#     voice = VillageParticipantVoice()
#     voice.village_no = Village.objects.get(pk=village_no)
#     voice.village_participant = VillageParticipant.objects.get(pl=request.session['login_id'])
#     voice.day_no = day_no
#     vt = request.POST['voice_type']
#     voice.voice_type = MVoiceType.objects.get(pk=vt)
#     lastvoice = \
#         Village.objects.get(pk=village_no). \
#             villageparticipantvoice_set.order_by('-voice_number')[0]
#     voice.voice_number = lastvoice.voice_number + 1
#     voice.use_point = 0
#     v = request.POST['voice']
#     voice.voice = v
#     voice.good_pl = PLAccount.objects.get(pk=request.session['login_id'])
#     voice.voice_datetime = datetime.now()
#     voice.delete_flg = False
#     voice.save()
#
#     # 村メイン画面に戻る
#     return HttpResponseRedirect(reverse('pywolf:village', args=(village_no, day_no,)))


# def login(request, village_no, day_no):
#     """ログイン"""
#
#     id = request.POST['id']
#     password = request.POST['password']
#
#     id = hashlib.sha256(id.encode('utf-8')).hexdigest()
#     password = hashlib.sha256(password.encode('utf-8')).hexdigest()
#
#     account = PLAccount.objects.get(id=id, password=password)
#
#     if account is not None:
#         request.session['login_user'] = account.id_view
#         request.session['login_id'] = id
#
#     # 村メイン画面に戻る
#     return HttpResponseRedirect(reverse('pywolf:village', args=(village_no, day_no,)))


# def logout(request, village_no, day_no):
#     """ログアウト"""
#
#     request.session.flush()  # （仮実装）
#
#     # 村メイン画面に戻る
#     return HttpResponseRedirect(reverse('pywolf:village', args=(village_no, day_no,)))


# def vote(request, village_no, day_no):
#     vote_id = request.POST['vote']
#     login_id = request.session.get('login_id', False)
#     participant = VillageParticipant.objects.get(village_no=village_no, pl=login_id)
#     ability = VillageParticipantExeAbility.objects.get(village_participant=participant, day_no=day_no)
#
#     ability.vote = hashlib.sha256(vote_id.encode('utf-8')).hexdigest()
#
#     ability.save()
#
#     # 村メイン画面に戻る
#     return HttpResponseRedirect(reverse('pywolf:village', args=(village_no, day_no,)))