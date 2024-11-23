from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('', include('core.urls', namespace='core')),
    path('cards/', include('cards.urls', namespace='cards')),
    path('admin/', admin.site.urls),
]

urlpatterns += debug_toolbar_urls()
