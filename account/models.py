from django.db import models
from django.contrib.auth.hashers import make_password

class Akademisyen(models.Model):
    kullanici_adi = models.CharField(max_length=100)
    mail = models.EmailField(unique=True)
    sifre = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        # Şifreyi hashle
        self.sifre = make_password(self.sifre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.kullanici_adi


class QRCodeData(models.Model):
    data = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.data
    

class QRData(models.Model):
    qr_data = models.CharField(max_length=255)
    csrf_token = models.CharField(max_length=255)
    okul_numarasi = models.CharField(max_length=50)  # Kullanıcının okul numarası bilgisi
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.qr_data