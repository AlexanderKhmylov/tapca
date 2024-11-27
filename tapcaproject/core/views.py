from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404

from cards.models import Card


def index(request):
    return render(request, 'base.html', {})


def page_not_found(request, exception):
    """View shows 404 error page"""
    return render(request, 'core/404.html', status=404)


def internal_server_error(request, exception=None):
    """View shows 500 error page"""
    return render(request, 'core/500.html', status=500)


def csrf_failure(request, reason=''):
    """Views shows 403csrf error page"""
    return render(request, 'core/403.html', status=403)


def custom_permission_denied(request, exception=None, reason=''):
    """Views shows 403 error page"""
    return render(request, 'core/403.html', status=403)


def error_500(request):
    x = 5/0
    return render(request, 'base.html', {})

def error_404(request):
    card = get_object_or_404(Card, id=1999999)
    return render(request, 'base.html', {})

@permission_required("polls.add_choice", raise_exception=True)
def error_403(request):
    return render(request, 'base.html')
