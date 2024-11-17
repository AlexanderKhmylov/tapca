from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('core.urls', namespace='core')),
    path('cards/', include('cards.urls', namespace='cards')),
    path('admin/', admin.site.urls),
]
