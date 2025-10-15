from django.db.models import Sum, Count, Case, When, FloatField
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .forms import RegistrationForm, TradeForm, Trade_image_form
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from .models import Trade
from django.db import transaction 

# Create your views here.
def home(request):
    if not request.user.is_authenticated:
         return HttpResponseRedirect(reverse("login"))
    info = Trade.objects.filter(user=request.user).order_by('-id')
    #calculate profit data
    profit_data = info.aggregate(
         net_profit = Sum("profit")
    )
    net_profit = profit_data["net_profit"] if profit_data["net_profit"] is not None else 0

    #calculate the win rate
    total_trades = info.count()
    win_rate = 0.0
    context = {
              "winrate": win_rate,
              "netprofit": net_profit,
              "info": info,
              }

    if total_trades > 0:
         win_count = info.aggregate(
              wins = Count(
                  Case(
                     When(outcome="WIN", then=1 ),
                     output_field= FloatField()
                  ) 
              )
         )
         win_count = win_count["wins"]

         win_rate = (win_count/total_trades) * 100
         context['netprofit'] = net_profit
         context['winrate'] = round(win_rate, 2)

         
    return render(request, "journal/home.html", context)

#view handling adding of trades
@login_required
def add_trade(request):
    if request.method == "POST":
        form = TradeForm(request.POST)
        formset = Trade_image_form(request.POST, request.FILES)
        if form.is_valid and formset.is_valid():
            with transaction.atomic():
                photo_instance = form.save(commit=False)
                photo_instance.user = request.user
                photo_instance.save()

                formset.instance = photo_instance
                formset.save()
                return redirect("home")
    else:
            form = TradeForm()
            formset = Trade_image_form()

    return render(request, "journal/add_trade.html", {
            "form" : form,
            "formset" : formset
        })
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

def logout_view(request):
     logout(request)
     return render(request, "journal/login.html")