from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls

handler404 = 'core.views.page_not_found'
handler500 = 'core.views.internal_server_error'
handler403 = 'core.views.custom_permission_denied'

urlpatterns = [
    path('core/', include('core.urls', namespace='core')),
    path('', include('cards.urls', namespace='cards')),
    path('users/', include('users.urls', namespace='users')),

    path('admin/', admin.site.urls),
]

urlpatterns += debug_toolbar_urls()
