import time
import os

from django import forms
from django.forms import CheckboxSelectMultiple
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from dotenv import load_dotenv

from .service import verify_otp_code

load_dotenv()
User = get_user_model()


class OtpSendForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            User.objects.create_user(
                username=str(int(time.time())),
                email=email,
                password=os.getenv('DEFAULT_USER_PASSWORD')
            )
        return email


class OtpVerifyForm(forms.Form):
    email = forms.EmailField(widget=forms.HiddenInput())
    number_1 = forms.IntegerField(required=True, label=False)
    number_2 = forms.IntegerField(required=True, label=False)
    number_3 = forms.IntegerField(required=True, label=False)
    number_4 = forms.IntegerField(required=True, label=False)
    number_5 = forms.IntegerField(required=True, label=False)
    number_6 = forms.IntegerField(required=True, label=False)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        number_1 = cleaned_data.get('number_1')
        number_2 = cleaned_data.get('number_2')
        number_3 = cleaned_data.get('number_3')
        number_4 = cleaned_data.get('number_4')
        number_5 = cleaned_data.get('number_5')
        number_6 = cleaned_data.get('number_6')

        otp = ''.join(map(
            str, (number_1, number_2, number_3, number_4, number_5, number_6))
        )
        user = get_object_or_404(User, email=email)
        if not verify_otp_code(user, otp):
            raise forms.ValidationError(
                ('Вы ввели неправильный код'
                 ' или истек его срок действия.'
                 ' Запросите код повторно!'))


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User

        fields = ('first_name', 'last_name')


class UserSettingForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('tags',)
        widgets = {
            'tags': CheckboxSelectMultiple(),
        }


class UserSetForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'tags')
        widgets = {
            'tags': CheckboxSelectMultiple(),
        }
