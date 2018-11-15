from django import forms

from ...models.pywolf.transactions import PLAccount


class PLAccountForm(forms.ModelForm):
    """ユーザー作成　情報入力画面用フォーム"""
    class Meta:
        model = PLAccount
        fields = ('id_view', 'password', 'commentary', )
        widgets = {
            'password': forms.PasswordInput(),
            'commentary': forms.Textarea(attrs={'cols': 25, 'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super(PLAccountForm, self).__init__(*args, **kwargs)
        self.fields['id_view'].label = 'ID'

    def clean(self):
        super(PLAccountForm, self).clean()
