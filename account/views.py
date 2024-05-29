from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from .models import Akademisyen
from django.contrib.auth import logout 
from django.contrib.auth.hashers import check_password, make_password
from django.http import HttpResponse
import qrcode
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import QRData
import json
from itertools import groupby

# Create your views here.

def index(request):
    return render(request, "index.html")

def ogrenci(request):
    return render(request, "ogrenci.html")

def akademisyen_giris(request):
    if request.method == 'POST':
        mail = request.POST['mail']
        girilen_sifre = request.POST['sifre']

        try:
            akademisyen = Akademisyen.objects.get(mail=mail)
            
            # Giriş formundan gelen şifreyi hashleme
            girilen_sifre_hashli = make_password(girilen_sifre)
            
            # Veritabanındaki hashlenmiş şifre ile karşılaştır
            if check_password(girilen_sifre, akademisyen.sifre):
                # Şifreler eşleşiyorsa, giriş başarılı
                return render(request, 'akademisyen_paneli.html', {'akademisyen': akademisyen})
            else:
                # Şifreler eşleşmiyorsa, giriş başarısız
                return render(request, 'login.html', {'hata': 'Mail veya şifre hatalı!'})
        except Akademisyen.DoesNotExist:
            return render(request, 'login.html', {'hata': 'Mail veya şifre hatalı!'})
    return render(request, 'login.html')

@login_required
def akademisyen_paneli(request):
    akademisyen = request.session.get('akademisyen')
    return render(request, 'akademisyen_paneli.html', {'akademisyen': akademisyen})

def cikis_yap(request):
    logout(request)
    return redirect('akademisyen_giris')

def group_qr_data_by_name(qrdata_list):
    # QR verilerini adlarına göre grupla
    sorted_qrdata = sorted(qrdata_list, key=lambda x: x.qr_data)
    grouped_qrdata = {}
    for name, group in groupby(sorted_qrdata, key=lambda x: x.qr_data):
        grouped_qrdata[name] = list(group)
    return grouped_qrdata

@csrf_exempt
def save_qr_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        qr_data = data.get('data')  # QR verisi
        okul_numarasi = data.get('okul_numarasi')  # Kullanıcı girişinden alınan okul numarası
        
        # Kullanıcının oturum açık olup olmadığını kontrol et
        if request.user.is_authenticated:
            # QR verisi ve öğrenci numarası ile QRData modeline yeni bir giriş oluştur
            QRData.objects.create(qr_data=qr_data, okul_numarasi=okul_numarasi)
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'User is not authenticated.'})
    else:
        # Sadece POST istekleri kabul edilir
        return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed.'})


def yoklama_view(request):
    qrdata_list = QRData.objects.all()  # Tüm QRData verilerini al
    grouped_qrdata = group_qr_data_by_name(qrdata_list)
    return render(request, 'yoklama.html', {'grouped_qrdata': grouped_qrdata})
