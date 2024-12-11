from django.urls import path

from .views import index, error_500, error_404, error_403

app_name = 'core'

urlpatterns = [
    path('', index, name='index'),
    path('404/', error_404, name='error_404'),
    path('500/', error_500, name='error_500'),
    path('403/', error_403, name='error_403'),
]
