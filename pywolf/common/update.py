from ..models.pywolf.transactions import VillageProgress
from ..models.pywolf.transactions import VillageParticipant
from ..models.pywolf.transactions import VillageParticipantExeAbilitySpiritResult
from ..models.pywolf.transactions import VillageVoiceSetting
from ..models.pywolf.transactions import VillageParticipantVoiceStatus
from ..models.pywolf.transactions import VillageParticipantExeAbility
from ..models.pywolf.transactions import Village
from ..models.pywolf.masters import MPosition

from pywolf.enums import CampClass
from pywolf.enums import WinLoseClass
from pywolf.enums import VillageStatus
from pywolf.enums import VillageParticipantStatus

import random
import datetime


def update(village_no, day_no):
    """更新処理"""
    village_status = VillageStatus.PROGRESS
    progress = VillageProgress.objects.latest()

    # ロック（すでに更新処理が始まってる）の場合は強制終了
    if progress.update_processing_lock:
        return
    else:
        progress.update_processing_lock = True
        progress.save()

    # 終了判定
    if progress.village_status == VillageStatus.EPILOGUE:  # エピからの更新で終了処理
        end = VillageProgress()
        end.village_no = Village.objects.get(village_no=village_no)
        end.day_no = day_no + 1
        end.village_status = VillageStatus.END
        end.next_update_datetime = None
        end.update_processing_lock = False
        end.save()
        # ロック解除して終了
        progress.update_processing_lock = False
        progress.save()
        return

    # 占い処理
    participant = VillageParticipant.objects.filter(village_no=village_no, cancel_flg=False, status=VillageParticipantStatus.SURVIVE)
    for part in participant:
        ability = part.villageparticipantexeability_set.get(day_no=day_no)
        if MPosition.objects.get(pk=part.position_id).fortune_enable_flg:
            fortune_obj = VillageParticipant.objects.get(village_no=village_no, pl=ability.fortune, cancel_flg=False)
            # ひとまずは【襲撃可能な役職を人狼と判定】もっとベストな解決はあるか・・・？
            if MPosition.objects.get(pk=fortune_obj.position_id).assault_enable_flg:
                ability.fortune_result = True
                ability.save()

    # 突然死処理
    participant = VillageParticipant.objects.filter(village_no=village_no, cancel_flg=False, status=0)
    for part in participant:
        voice = part.villageparticipantvoice_set.filter(day_no=day_no)
        if not voice:
            part.status = VillageParticipantStatus.SUDDEN_DEATH
            part.save()

    # 決着判定処理１回目
    if settled(village_no):
        # エピローグ処理
        create_village_info(village_no, day_no, VillageStatus.EPILOGUE)
        # ロック解除して終了
        progress.update_processing_lock = False
        progress.save()
        return

    # 処刑処理
    votes = {}  # 初期化
    for part in participant:
        votes[part.pl_id] = 0
    # 突然死で地上参加者が減ってかもしれないため、再取得（悲しいね・・・）
    participant = VillageParticipant.objects.filter(village_no=village_no, cancel_flg=False, status=VillageParticipantStatus.SURVIVE)
    for part in participant:
        # 票集計
        vote = part.villageparticipantexeability_set.get(day_no=day_no)
        votes[vote.vote] += 1

    # 最多票者を取得し、処刑。複数入ればランダム
    punish = max(votes.items(), key=lambda x: x[1])
    if len(punish) == 1:
        death = VillageParticipant.objects.get(pl=punish.keys[0])
    else:
        death = VillageParticipant.objects.get(pl=random.choice(punish).keys[0])
    death.status = VillageParticipantStatus.PUNISH_DEATH
    death.save()

    # 決着判定処理２回目
    if settled(village_no):
        # エピローグ処理
        create_village_info(village_no, day_no, VillageStatus.EPILOGUE)
        # ロック解除して終了
        progress.update_processing_lock = False
        progress.save()
        return

    # 襲撃処理と護衛処理
    assault_objs = set()
    for part in participant:
        ability = part.villageparticipantexeability_set.get(day_no=day_no)
        # ひとまずは【襲撃可能な役職を人狼と判定】もっとベストな解決はあるか・・・？
        if MPosition.objects.get(pk=part.position_id).assault_enable_flg:
            assault_objs.add(ability.assault)
    # 襲撃先が全員一致ならそのまま、バラバラならランダム
    if len(assault_objs) == 1:
        assault_target = VillageParticipant.objects.get(pl=assault_objs[0])
    else:
        assault_target = VillageParticipant.objects.get(pl=random.choice(assault_objs))

    # 護衛判定
    guard_success = False
    for part in participant:
        ability = part.villageparticipantexeability_set.get(day_no=day_no)
        if MPosition.objects.get(pk=part.position_id).guard_enable_flg:
            if assault_target == ability.guard:
                # 護衛成功
                ability.guard_result = True
                ability.save()
                guard_success = True

    if not guard_success:
        assault_target.status = VillageParticipantStatus.ASSAULT_DEATH
        assault_target.save()

    # 決着判定処理３回目
    if settled(village_no):
        # エピローグ処理
        create_village_info(village_no, day_no, VillageStatus.EPILOGUE)
        # ロック解除して終了
        progress.update_processing_lock = False
        progress.save()
        return

    # 霊能処理は死んだ人を判定するから、最後に
    participant = VillageParticipant.objects.filter(village_no=village_no, cancel_flg=False, status=VillageParticipantStatus.SURVIVE)
    for part in participant:
        if MPosition.objects.get(pk=part.position_id).spirit_enable_flg:
            deads = VillageParticipant.objects.filter(village_no=village_no,
                                                      cancel_flg=False,
                                                      status__in=[VillageParticipantStatus.PUNISH_DEATH,
                                                                  VillageParticipantStatus.ASSAULT_DEATH,
                                                                  VillageParticipantStatus.SUDDEN_DEATH
                                                                  ])  # 死んだ人
            for d in deads:
                # ひとまずは【襲撃可能な役職を人狼と判定】もっとベストな解決はあるか・・・？
                if MPosition.objects.get(pk=d.position_id).assault_enable_flg:
                    ability = VillageParticipantExeAbilitySpiritResult()
                    ability.village_participant = part
                    ability.day_no = day_no
                    ability.spirit = d.pl_id
                    ability.spirit_result = True
                    ability.save()

    # 翌日の村情報を作成
    create_village_info(village_no, day_no, village_status)
    # ロック解除して終了
    progress.update_processing_lock = False
    progress.save()


def settled(village_no):
    """決着判定"""

    settled = False

    # 人数確認
    village_num = 0
    wolf_num = 0
    # 処刑もしくは襲撃が行われて地上参加者が減っているため、再取得
    participant = VillageParticipant.objects.filter(village_no=village_no, cancel_flg=False, status=VillageParticipantStatus.SURVIVE)
    for part in participant:
        if MPosition.objects.get(id=part.position_id).camp_class == CampClass.VILLAGE:
            village_num += 1
        else:
            wolf_num += 1

    # 決着・勝敗判定
    win_class = 0
    if wolf_num == 0:  # 村人勝利
        win_class = CampClass.VILLAGE
    elif village_num <= wolf_num:  # 人狼勝利
        win_class = CampClass.WOLF

    # 決着なら勝敗を確定
    if win_class != 0:
        participant = VillageParticipant.objects.filter(village_no=village_no, cancel_flg=False)
        for part in participant:
            if part.status == VillageParticipantStatus.SUDDEN_DEATH:
                # 突然死者は勝敗つけず・・・
                part.win_lose_class = WinLoseClass.SUDDEN_DEATH
            else:
                if MPosition.objects.get(id=part.position_id).camp_class == win_class:
                    part.win_lose_class = WinLoseClass.WIN
                else:
                    part.win_lose_class = WinLoseClass.LOSE
            part.save()
        settled = True

    return settled


def create_village_info(village_no, day_no, village_status):
    """村情報作成"""

    village = Village.objects.get(village_no=village_no)

    # 村進行情報作成
    progress = VillageProgress()
    progress.village_no = village
    progress.day_no = day_no + 1
    progress.village_status = village_status
    progress.next_update_datetime = VillageProgress.objects.latest().next_update_datetime + datetime.timedelta(hours=village.update_interval)
    progress.update_processing_lock = False
    progress.save()

    # 投票･能力行使データ作成
    participant = VillageParticipant.objects.filter(village_no=village_no, cancel_flg=False, status=0)
    for part in participant:
        ability = VillageParticipantExeAbility()
        ability.village_participant = part
        ability.day_no = day_no + 1
        ability.save()

    # 村発言ステータス作成
    voice_setting = VillageVoiceSetting.objects.filter(village_no=village_no)
    participant = VillageParticipant.objects.filter(village_no=village_no, cancel_flg=False)  # 生死問わず取得
    for p in participant:
        for v in voice_setting:
            voice_status = VillageParticipantVoiceStatus()
            voice_status.village_participant = p
            voice_status.day_no = day_no + 1
            voice_status.voice_type = v.voice_type
            voice_status.voice_number_remain = v.voice_number
            voice_status.voice_point_remain = v.voice_point
            voice_status.save()



    # 更新結果のシステムメッセージ作成

    if voice_status.day_no == 1:
        # プロローグ＞１日目のみ希望役職から実際の配役決定


        # １日目のシステム発言・ダミー発言作成
        pass

    # 決着がついた場合、リザルト表示

