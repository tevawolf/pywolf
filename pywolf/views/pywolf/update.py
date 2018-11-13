from ...models.pywolf.transactions import VillageProgress
from ...models.pywolf.transactions import VillageParticipant
from ...models.pywolf.transactions import VillageParticipantExeAbility
from ...models.pywolf.transactions import VillageParticipantExeAbilitySpiritResult
from ...models.pywolf.masters import MPosition

import random


def update(request, village_no, day_no):
    """更新処理"""

    village_status = 1

    # 占い処理
    participant = VillageParticipant.objects.filter(village_no=village_no, cancel_flg=False, status=0)
    for part in participant:
        ability = VillageParticipantExeAbility.objects.get(village_participant=participant, day_no=day_no)
        if MPosition.objects.get(pk=part.position_id).fortune_enable_flg:
            fortune_obj = ability.fortune
            # ひとまずは【襲撃可能な役職を人狼と判定】もっとベストな解決はあるか・・・？
            if MPosition.objects.get(pk=fortune_obj.position_id).assault_enable_flg:
                ability.fortune_result = True
                ability.save()

    # 突然死処理

    # 処刑処理
    votes = {}  # 初期化
    for part in participant:
        votes[part.pl_id] = 0

    for part in participant:  # 票集計
        vote = VillageParticipantExeAbility.objects.get(village_participant=part, day_no=day_no)
        votes[vote.vote] += 1

    # 最多票者を取得し、処刑。複数入ればランダム
    panish = max(votes.items(), key=lambda x: x[1])
    if len(panish) == 1:
        death = VillageParticipant.objects.get(pl=panish.keys[0])
    else:
        death = VillageParticipant.objects.get(pl=random.choice(panish).keys[0])
    death.status = 1
    death.save()

    # 決着判定処理１
    village_num = 0
    wolf_num = 0
    participant = VillageParticipant.objects.filter(village_no=village_no, cancel_flg=False, status=0)
    for part in participant:
        if MPosition.objects.get(id=part.position_id).camp_class == 1:
            village_num += 1
        else:
            wolf_num += 1

    win_class = 0
    if wolf_num == 0:  # 村人勝利
        win_class = 1
    elif village_num <= wolf_num:  # 人狼勝利
        win_class = 2

    if win_class != 0:
        participant = VillageParticipant.objects.filter(village_no=village_no, cancel_flg=False)
        for part in participant:
            if MPosition.objects.get(id=part.position_id).camp_class == win_class:
                part.win_lose_class = 1
            else:
                part.win_lose_class = 2
            part.save()
        # エピローグ処理
        village_status = 2

    # 襲撃処理と護衛処理
    # BBS方式にするかクローン方式にするか・・・・
    for part in participant:
        ability = VillageParticipantExeAbility.objects.get(village_participant=participant, day_no=day_no)
        if MPosition.objects.get(pk=part.position_id).assault_enable_flg:
            assault_obj = ability.assault
            # ひとまずは【襲撃可能な役職を人狼と判定】もっとベストな解決はあるか・・・？
            if MPosition.objects.get(pk=fortune_obj.position_id).assault_enable_flg:
                ability.fortune_result = True
                ability.save()

    # 決着判定処理２


    # 霊能処理は死んだ人を判定するから、最後に
    participant = VillageParticipant.objects.filter(village_no=village_no, cancel_flg=False, status=0)
    for part in participant:
        if MPosition.objects.get(pk=part.position_id).spirit_enable_flg:
            deads = VillageParticipant.objects.filter(village_no=village_no, cancel_flg=False, status__in=[1, 2, 9])  # 死んだ人
            for d in deads:
                # ひとまずは【襲撃可能な役職を人狼と判定】もっとベストな解決はあるか・・・？
                if MPosition.objects.get(pk=d.position_id).assault_enable_flg:
                    ability = VillageParticipantExeAbilitySpiritResult()
                    ability.village_participant = part
                    ability.day_no = day_no
                    ability.spirit = d.pl_id
                    ability.spirit_result = True
                    ability.save()

    # 村進行情報作成
    progress = VillageProgress()
    progress.village_no = village_no
    progress.day_no = day_no + 1
    progress.village_status = village_status
    progress.save()

