from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.shortcuts import get_object_or_404, reverse
from django.views.generic import UpdateView, TemplateView, ListView, FormView

from .forms import OtpSendForm, OtpVerifyForm, UserProfileForm, UserSettingForm, UserSetForm
from .mixins import OnlyMyDataMixin
from .models import UserCard
from .service import create_otp, send_otp_email
from cards.models import Card
from cards.service import get_user_cards, get_user_repeated_cards

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


class UserStatisticView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users/statistic_main.html'
    form_class = UserSetForm
    context_object_name = 'user'

    def get_success_url(self):
        return reverse('users:statistics', kwargs={'pk': self.request.user.pk})


class MyNewWordsView(LoginRequiredMixin, ListView):
    model = Card
    template_name = 'users/new_words.html'
    context_object_name = 'cards'

    def get_queryset(self):
        cards = get_user_cards(self.request.user)
        return cards


def my_repeated_word(request):
    cards = get_user_repeated_cards(request.user)
    return render(request, 'users/repeated_words.html', {'cards': cards})


def reset_progress(request, user_card_id):
    user_card = get_object_or_404(UserCard, pk=user_card_id)
    user_card.frequency = 100
    user_card.save()
    return my_repeated_word(request)


def delete_user_card(request, user_card_id):
    user_card = get_object_or_404(UserCard, pk=user_card_id)
    user_card.delete()
    return my_repeated_word(request)
