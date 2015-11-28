from django import forms


class PostNormalForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField(
        widget=forms.Textarea
    )
    category = forms.IntegerField()
    registration_code = forms.CharField(
        label='주민등록번호',
        help_text='xxxxxx-yyyyyy 형식으로 입력하세요.',
        widget=forms.TextInput(
            attrs={'class': 'hello_world'}
        )
    )
