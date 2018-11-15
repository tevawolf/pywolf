from django import forms
from django.core.exceptions import ObjectDoesNotExist

from ...models.pywolf.transactions import Village
from ...models.pywolf.masters import MChip
from ...models.pywolf.masters import MPosition
from ...models.pywolf.masters import MOrganizationPositionNumber


class EntryForm(forms.Form):
    """入村時　入力フォーム"""
    chips = forms.models.ChoiceField(
            label='キャラクター選択', required=True, choices=(), )
    description = forms.CharField(label='肩書き', strip=True, required=True, max_length=30)
    character_name = forms.CharField(label='名前', strip=True, required=True, max_length=30)
    wish_position = forms.ChoiceField(label='希望役職', required=True, choices=())
    voice = forms.CharField(label='発言', widget=forms.Textarea())
    into_password = forms.CharField(label='入村パスワード', widget=forms.PasswordInput())

    def __init__(self, village_no, *args, **kwargs):
        super(EntryForm, self).__init__(*args, **kwargs)

        # HTML属性付与
        self.fields['chips'].widget.attrs = {'id': "entry_character_chip", 'onchange': 'selectCharacterChip();'}
        self.fields['description'].widget.attrs = {'id': "entry_description", }
        self.fields['character_name'].widget.attrs = {'id': "entry_character_name", }
        self.fields['wish_position'].widget.attrs = {'id': "entry_wish_position", }
        self.fields['voice'].widget.attrs = {'id': "entry_voice",
                                             'style': 'width:350px; height:150px; background: linear-gradient(135deg, #FFFFFF 60%, #DDDDDD 100%); border: solid 1.5px #222222;',
                                             'class': 'voice',
                                             }
        self.fields['into_password'].widget.attrs = {'id': "entry_into_password", }

        village = Village.objects.get(village_no=village_no)

        # キャラクター選択 候補設定
        chips = [('', '(選択してください)'),]
        cs = MChip.objects.filter(chip_set_id=village.chip_set, delete_flg=False)
        parts = village.villageparticipant_set.all()
        for c in cs:
            same = False
            for part in parts:
                if part.chip_id == c.id:
                    same = True
            if not same:
                chips.append((c.id, c.description + c.character_name))
        self.fields['chips'].choices = tuple(chips)

        # 希望役職 選択候補設定
        positions = [('', '(選択してください)'),]
        try:
            orgset = village.villageorganizationsetting_set.get()
            # 村編成設定から設定役職を取得する
            organizations = orgset.villageorganization_set.get()
        except ObjectDoesNotExist:
            # 編成マスタ情報から編成に含まれる役職を取得する
            organizations = MOrganizationPositionNumber.objects.filter(organization_id=village.organization_setting)
        for org in organizations:
            position = MPosition.objects.get(pk=org.position_id_id)
            positions.append((position.id, position.position_name))
        self.fields['wish_position'].choices = tuple(positions)

        print(positions)

    def clean(self):
        super(EntryForm, self).clean()
