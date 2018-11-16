from enum import IntEnum


def forDjango(cls):
    cls.do_not_call_in_templates = True
    return cls


@forDjango
class StartClass(IntEnum):
    """開始方法"""
    AUTO = 1,
    MANUAL = 2,
    LIMIT = 3,


@forDjango
class UpdateInterval(IntEnum):
    """更新頻度"""
    hour24 = 24,
    hour48 = 48,
    hour72 = 72,


@forDjango
class VoiceNumberClass(IntEnum):
    """発言制度"""
    COUNT = 1,
    POINT = 2,


@forDjango
class VillageStatus(IntEnum):
    """村ステータス"""
    PROLOGUE = 0,
    PROGRESS = 1,
    EPILOGUE = 2,
    END = 3,
    ABOLITION = 4,


@forDjango
class VillageParticipantStatus(IntEnum):
    """参加者ステータス"""
    SURVIVE = 0,
    PUNISH_DEATH = 1,
    ASSAULT_DEATH = 2,
    SUDDEN_DEATH = 9,
    LEAVE_VILLAGE = 10,


@forDjango
class WinLoseClass(IntEnum):
    """勝敗"""
    UNSETTLED = 0,
    WIN = 1,
    LOSE = 2,
    SUDDEN_DEATH = 9,


@forDjango
class CampClass(IntEnum):
    """陣営"""
    VILLAGE = 1,
    WOLF = 2,


@forDjango
class VoiceTypeId(IntEnum):
    """発言種別"""
    NORMAL = 1,
    WOLF = 2,
    SELF = 3,
    SYSTEM = 4,
    GRAVE = 5,
    SYS_HIDDEN = 6,


@forDjango
class SpeechHearMode(IntEnum):
    IMPOSSIBLE = 0,
    NOT_SPEECH_HEAR_OTHER = 1,
    SPEECH_HEAR_SELF = 2,
    SPEECH_HEAR = 3,
