from django.contrib import admin

from .models import TapcaUser, OTP


admin.site.register(TapcaUser)
admin.site.register(OTP)
