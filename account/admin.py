from django.contrib import admin
from .models import Akademisyen
from .models import QRCodeData, QRData

admin.site.register(QRCodeData)
admin.site.register(Akademisyen)
admin.site.register(QRData)
