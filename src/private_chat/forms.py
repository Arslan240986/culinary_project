from django import forms


class ComposeForm(forms.Form):
    message = forms.CharField(
            widget=forms.Textarea(
                attrs={'cols': 1}
                ),
            label = ''
            )
