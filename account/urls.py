from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.index, name="home"),
    path('ogrenci/', views.ogrenci, name='ogrenci'),
    path('giris/', views.akademisyen_giris, name='akademisyen_giris'),
    path('panel/', views.akademisyen_paneli, name='akademisyen_paneli'),
    path('cikis/', views.cikis_yap, name='cikis_yap'),  # Yeni URL eklendi
    path('save_qr_data/', views.save_qr_data, name='save_qr_data'),
    path('detay/', views.yoklama_view, name='yoklama')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)