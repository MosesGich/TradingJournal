from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import RegistrationForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def home(request):
    return render(request, "journal/home.html")

#view handling adding of trades
def add_trade(request):
    pass
def reg(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
            form = RegistrationForm()
        
    return render(request, "journal/register.html", {
        "form": form,
    })
def login_view(request):
     if request.method == "POST":
          username = request.POST["username"]
          password = request.POST["password"]
          user =authenticate(request, username=username, password=password)
          if user is not None:
               login(request,user)
               return HttpResponseRedirect(reverse("home"))
          else:
               return render(request, "journal/login.html", {
                   "message" : "Invalid credentials"
               })
     return render(request, "journal/login.html")