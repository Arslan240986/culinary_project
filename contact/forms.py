from django import forms
from django.contrib.auth.models import User

from .models import UserProfile, ContactSubscribe


# class UserCulinaryBookForm(forms.ModelForm):
#     class Meta:
#         model = UserCulinaryBook
#         fields = ('dishes', )


GENDERS = [
    ('М', 'Мужчина'),
    ('Ж', 'Женщина'),
]


class ProfileEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gender'] = forms.ChoiceField(label='Пол:', choices=GENDERS, widget=forms.RadioSelect())
        self.fields['get_news_from'] = forms.BooleanField(label_suffix='', label="Получать уведомления", required=False)
        self.fields['get_notification_about_comments'] = forms.BooleanField(label_suffix='',
                                                         label="Получать уведомления о комментах", required=False)
        self.fields['get_notification_friend_request'] = forms.BooleanField(label_suffix='',
                                                         label="Получать уведомления на добавление в дружбу", required=False)

    class Meta:
        model = UserProfile
        exclude = ['user', 'slug', 'friends', 'dishes']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Фамилия'}),
            'birth_date': forms.DateInput(attrs={'class': 'date_input'}),
            'email': forms.DateInput(attrs={'placeholder': 'Введите ваш маил'}),
            'country_of_birth': forms.DateInput(attrs={'placeholder': 'Введите Страну проживания'}),
            'profession': forms.Textarea(attrs={'rows': 2}),
            'interest': forms.Textarea(attrs={'rows': 2}),
            'about': forms.Textarea(attrs={'rows': 2}),
        }


class ContactSubscribeForm(forms.ModelForm):
    """Форма подписки по email """
    class Meta:
        model = ContactSubscribe
        fields = ('email',)
        widgets = {
            'email': forms.TextInput(attrs={
                'class': 'form__input',
                'placeholder': 'Адрес электронной почты',
            }),
        }
        labels = {
            'email': ''
        }

    def clean_email(self):
        mails = ContactSubscribe.objects.all()
        email = self.cleaned_data.get('email')
        if email in [i.email for i in mails]:
            raise forms.ValidationError('neeeeet')
        return email
