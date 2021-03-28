from django import forms
from .models import CulinaryPost, PostComment


class CulinaryPostModelForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows':2}), label='Описания')

    class Meta:
        model = CulinaryPost
        fields = ('title', 'content', 'image')


class PostCommentModelForm(forms.ModelForm):
    body = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': 'Оставить коментарий',
                                                                   'class': 'mb-2','rows': 2,
                                                                   }))

    class Meta:
        model = PostComment
        fields = ('body',)