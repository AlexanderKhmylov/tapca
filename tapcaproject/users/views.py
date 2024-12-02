from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.shortcuts import get_object_or_404, reverse
from django.views.generic import UpdateView

from .forms import OtpSendForm, OtpVerifyForm, UserProfileForm, UserSettingForm
from .mixins import OnlyMyDataMixin
from .service import create_otp, send_otp_email

User = get_user_model()


def send_otp(request):
    if request.method == 'POST':
        form = OtpSendForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = get_object_or_404(User, email=email)
            code = create_otp(user)
            send_otp_email(user, code)
            url = f"{reverse('users:verify_otp')}?email={email}"
            return redirect(url)
    else:
        form = OtpSendForm()
    return render(
        request, 'users/send_otp.html', {'form': form})


def verify_otp(request):
    if request.method == 'POST':
        form = OtpVerifyForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = get_object_or_404(User, email=email)
            login(request, user)
            return redirect('cards:cards_main')
    else:
        email = request.GET.get('email')
        form = OtpVerifyForm(initial={'email': email})

    return render(
        request, 'users/verify_otp.html', {'form': form})


class UserProfileUpdateView(LoginRequiredMixin, OnlyMyDataMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    context_object_name = 'user'
    template_name = 'users/user_profile_setting.html'

    def get_success_url(self):
        return reverse('cards:cards_main')


class UserSettingUpdateView(LoginRequiredMixin, OnlyMyDataMixin, UpdateView):
    model = User
    form_class = UserSettingForm
    context_object_name = 'user'
    template_name = 'users/user_profile_setting.html'

    def get_success_url(self):
        return reverse('cards:cards_main')
