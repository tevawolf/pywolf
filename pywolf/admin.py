from django.contrib import admin

from .models.pywolf.transactions import PLAccount
from .models.pywolf.transactions import Village
from .models.pywolf.transactions import VillageVoiceSetting
from .models.pywolf.transactions import VillageOrganization
from .models.pywolf.transactions import VillageProgress
from .models.pywolf.transactions import VillageParticipant
from .models.pywolf.transactions import VillageParticipantVoice
from .models.pywolf.transactions import VillageParticipantVoiceStatus
from .models.pywolf.transactions import VillageParticipantExeAbility

from .models.pywolf.masters import MPosition
from .models.pywolf.masters import MVoiceType
from .models.pywolf.masters import MPositionVoiceSetting
from .models.pywolf.masters import MVoiceSettingSet
from .models.pywolf.masters import MVoiceSetting
from .models.pywolf.masters import MChipSet
from .models.pywolf.masters import MChip
from .models.pywolf.masters import MSysMessageSet
from .models.pywolf.masters import MSysMessage
from .models.pywolf.masters import MOrganizationSet
from .models.pywolf.masters import MOrganization

admin.site.register(PLAccount)


#村
class VillageVoiceSettingInline(admin.TabularInline):
    model = VillageVoiceSetting
    extra = 1


class VillageOrganizationSettingInline(admin.TabularInline):
    model = VillageOrganization
    extra = 1


class VillageAdmin(admin.ModelAdmin):
    list_display = ('village_no', 'village_name', 'description')
    inlines = [VillageVoiceSettingInline, VillageOrganizationSettingInline]


admin.site.register(Village, VillageAdmin)
#admin.site.register(VillageVoiceSetting)
#admin.site.register(VillageOrganization)

admin.site.register(VillageProgress)


class VillageParticipantAdmin(admin.ModelAdmin):
    list_display = ('pl', 'chip', 'description', 'character_name')


admin.site.register(VillageParticipant, VillageParticipantAdmin)


class VillageParticipantVoiceAdmin(admin.ModelAdmin):
    list_display = ('village_participant', 'day_no', 'voice_type', 'voice_number')
    list_filter = ['village_participant',  'day_no', 'voice_type']
    search_fields = ['voice']


admin.site.register(VillageParticipantVoice, VillageParticipantVoiceAdmin)
admin.site.register(VillageParticipantVoiceStatus)
admin.site.register(VillageParticipantExeAbility)


class MPositionAdmin(admin.ModelAdmin):
    list_display = ('position_name', 'camp_class', 'commentary')


admin.site.register(MPosition, MPositionAdmin)


class MVoiceTypeAdmin(admin.ModelAdmin):
    list_display = ('voice_type_name', 'commentary')


admin.site.register(MVoiceType, MVoiceTypeAdmin)


class MPositionVoiceSettingAdmin(admin.ModelAdmin):
    list_display = ('position', 'voice_type', 'speech_hear_mode')
    list_filter = ['position']


admin.site.register(MPositionVoiceSetting, MPositionVoiceSettingAdmin)


# 発言設定セット
class VoiceSettingInline(admin.TabularInline):
    model = MVoiceSetting
    extra = 1


class VoiceSettingAdmin(admin.ModelAdmin):
    list_display = ('voice_type_set_name', 'commentary')
    inlines = [VoiceSettingInline]


admin.site.register(MVoiceSettingSet, VoiceSettingAdmin)
#admin.site.register(MVoiceSetting)


# チップセット
class ChipInline(admin.TabularInline):
    model = MChip
    extra = 1


class ChipsetAdmin(admin.ModelAdmin):
    list_display = ('chip_set_name', 'author_name')
    inlines = [ChipInline]


admin.site.register(MChipSet, ChipsetAdmin)
#admin.site.register(MChip)


# メッセージセット
class MessageInline(admin.TabularInline):
    model = MSysMessage
    extra = 1


class MessagesetAdmin(admin.ModelAdmin):
    list_display = ('system_message_set_name', 'commentary')
    inlines = [MessageInline]


admin.site.register(MSysMessageSet, MessagesetAdmin)
#admin.site.register(MSysMessage)


# 編成セット
class OrganizationInline(admin.TabularInline):
    model = MOrganization
    extra = 1


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('organization_set_name', 'participant_number')
    inlines = [OrganizationInline]


admin.site.register(MOrganizationSet, OrganizationAdmin)
#admin.site.register(MOrganization)
