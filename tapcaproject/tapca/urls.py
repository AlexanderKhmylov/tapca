from django.contrib import admin
from django.urls import path, include
from django.conf import settings


handler404 = 'core.views.page_not_found'
handler500 = 'core.views.internal_server_error'
handler403 = 'core.views.custom_permission_denied'

urlpatterns = [
    path('', include('cards.urls', namespace='cards')),
    path('core/', include('core.urls', namespace='core')),
    path('users/', include('users.urls', namespace='users')),
    path('admin/', admin.site.urls),
]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
