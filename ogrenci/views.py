from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from account.models import QRData

def login_request(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            
            # Kullanıcı girişi yapıldıktan sonra QRData modeline okul numarasını kaydedin
            #okul_numarasi = username
            #qr_data = QRData.objects.create(qr_data=okul_numarasi, csrf_token="", okul_numarasi=okul_numarasi)
            
            return redirect('ogrenci')
        else:
            return render(request, "account/login.html", {"error": "Okul numarası veya Şifre yanlış"})

    return render(request, "account/login.html")

def register_request(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        password = request.POST["password"]
        repassword = request.POST["repassword"]

        if password == repassword:
            if User.objects.filter(username=username).exists():
                return render(request, "account/register.html", {"error":"Okul numarası zaten var"})

            else:
                if User.objects.filter(email=email).exists():
                    return render(request, "account/register.html", {"error":"email zaten var"})
                else:
                    user = User.objects.create_user(username=username, email=email, first_name=firstname, last_name=lastname, password=password)
                    user.save()
                    return redirect('login')
        else:
            return render(request, "account/register.html", {"error":"Şifre eşleşmiyor"})

    return render(request, "account/register.html")

def logout_request(request):
    logout(request)
    return redirect("home")
