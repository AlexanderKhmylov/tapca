from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('core/', include('core.urls', namespace='core')),
    path('', include('cards.urls', namespace='cards')),
    path('admin/', admin.site.urls),
]

urlpatterns += debug_toolbar_urls()
