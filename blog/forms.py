from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    def clean(self):
        title = self.cleaned_data.get('title', '')
        if '카지노' in title:
            self.add_error('title', '스팸 냄새가 납니다.')

    def clean_title(self):
        title = self.cleaned_data.get('title', '')
        if '카지노' in title:
            raise forms.ValidationError(
                '스팸 냄새가 납니다.',
                code='strange_word'
            )

        if '배팅' in title:
            raise forms.ValidationError(
                '스팸 냄새가 납니다.',
                code='toto_word'
            )
        return title

    class Meta:
        model = Post
        fields = ('category', 'title', 'content', )
        # widgets = {
        #     'title': forms.PasswordInput
        # }


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
