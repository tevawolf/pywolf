from django import forms
from ...models.pywolf.transactions import Village
from ...models.pywolf.masters import MChipSet
from ...models.pywolf.masters import MSysMessageSet
from ...models.pywolf.masters import MOrganizationSet
from ...models.pywolf.masters import MVoiceSettingSet


class VillageForm(forms.ModelForm):
    """村の作成　基本情報入力画面用フォーム"""
    class Meta:
        model = Village
        fields = ('village_name', 'description', 'start_class', 'lowest_number', 'max_number',
                  'into_password', 'update_interval', 'start_scheduled_date',
                  'voice_number_class', )
        widgets = {
            'into_password': forms.PasswordInput(),
            'description': forms.Textarea(),
        }

    # 更新時刻
    update_time_hour = forms.models.ChoiceField(label='時', required=True, choices=((h, h) for h in range(0, 24)))
    update_time_minute = forms.models.ChoiceField(label='分', required=True, choices=((m, m) for m in range(0, 60, 15)))

    chip_set = forms.models.ModelChoiceField(label='チップセット', required=True,
                                             queryset=MChipSet.objects.filter(delete_flg=False))

    system_message = forms.models.ModelChoiceField(label='システム文章', required=True,
                                                   queryset=MSysMessageSet.objects.filter(delete_flg=False))

    organization_setting = forms.models.ModelChoiceField(label='編成設定', required=True,
                                                     queryset=MOrganizationSet.objects.filter(delete_flg=False))

    voice_setting_set = forms.models.ModelChoiceField(label='発言設定', required=True,
                                                      queryset=MVoiceSettingSet.objects.filter(delete_flg=False))

    def __init__(self, *args, **kwargs):
        super(VillageForm, self).__init__(*args, **kwargs)
        self.fields['village_name'].label = '村の名前'
        self.fields['description'].label = '村の説明'
        self.fields['start_class'].label = '開始方法'
        self.fields['lowest_number'].label = '最低開始人数'
        self.fields['max_number'].label = '最大開始人数'
        self.fields['into_password'].label = '入村パスワード'
        self.fields['into_password'].required = False
        self.fields['update_interval'].label = '更新間隔'
        self.fields['start_scheduled_date'].label = '開始予定日'
        self.fields['start_scheduled_date'].widget.attrs['class'] = 'form-control'
        self.fields['voice_number_class'].label = '発言量タイプ<br/>(回数制/pt制)'

    def clean_update_time_hour(self):
        return self.cleaned_data['update_time_hour']

    def clean_update_time_minute(self):
        return self.cleaned_data['update_time_minute']

    def clean_chip_set(self):
        return self.cleaned_data['chip_set']

    def clean_system_message(self):
        return self.cleaned_data['system_message']

    def clean_organization_setting(self):
        return self.cleaned_data['organization_setting']

    def clean_voice_setting_set(self):
        return self.cleaned_data['voice_setting_set']

    def clean(self):
        super(VillageForm, self).clean()

    def get_village_name(self):
        return self.cleaned_data['village_name']
