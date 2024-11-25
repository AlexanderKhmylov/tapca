from django import forms
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .service import verify_otp_code

User = get_user_model()


class OtpSendForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email не найден")
        return email


class OtpVerifyForm(forms.Form):
    email = forms.EmailField(widget=forms.HiddenInput())
    otp = forms.CharField(max_length=10, required=True, label='Код')

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        otp = cleaned_data.get('otp')
        user = get_object_or_404(User, email=email)
        if not verify_otp_code(user, otp):
            raise forms.ValidationError(
                ('Вы ввели неправильный код'
                 ' или истек его срок действия.'
                 ' Запросите код повторно!'))
