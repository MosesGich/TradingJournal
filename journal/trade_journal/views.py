from django.shortcuts import render, redirect
from .forms import RegistrationForm

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
            return redirect("home")
    else:
            form = RegistrationForm()
        
    return render(request, "journal/register.html", {
        "form": form
    })