from django import forms
from .models import CulinaryPost, CulinaryPostComment


class CulinaryPostModelForm(forms.ModelForm):
    # content = forms.CharField(widget=forms.Textarea(attrs={'rows':2}), label='Описания')

    class Meta:
        model = CulinaryPost
        fields = ('title', 'content', 'image')


class PostCommentModelForm(forms.ModelForm):
    """Форма отзывов"""

    class Meta:
        model = CulinaryPostComment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'rows': 2})
        }