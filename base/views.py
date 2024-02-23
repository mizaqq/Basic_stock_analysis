from django.shortcuts import render,redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from .models import Company,Prices
from datetime import date, timedelta
import matplotlib.pyplot as plt
import io
import urllib,base64
import pandas as pd
import matplotlib


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try: 
            user=User.objects.get(username=username)
        except:
            messages.error(request,'User does not exist')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Username OR password is incorrect')
    context={'page':page}
    return render(request, 'base/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username= user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,'An error occured during registration')
    context={'form':form}
    return render(request,'base/login_register.html',context)
    
def home(request):
    q= request.GET.get('q') if request.GET.get('q') != None else 'IBM'
    comp = Company.objects.get(name = q)
    prices = Prices.objects.filter(symbol = comp.pk)
    
    if (prices.order_by('-date')[0].date != date.today()- timedelta(days=1)) and date.today().weekday()!=0 and date.today().weekday()!=1:
        Prices.update_values(Company.objects.first().pk)
        prices = Prices.objects.filter(symbol = comp.pk)
        
    companies= Company.objects.all()[0:5]
    
    context= {'companies':companies,'company':comp,'prices':prices[:5]}
    return render(request, 'base/home.html',context)

def getNewCompany(request):
    if request.method == "POST":
        name = request.POST.get('name')
        symbol = request.POST.get('symbol').upper()
        try:
            comp = Company(name=name, symbol = symbol)
            comp.save()
        except:
            messages.error(request,"Company already in db")
        Prices.update_values(Company.objects.get(symbol = symbol).pk)
        prices=Prices.objects.filter(symbol=Company.objects.get(symbol = symbol)).order_by('-date')[:5]
        if prices.exists():
            for i in prices:
                messages.info(request,f'{i.date} Close price: {i.close}')
        else:
            comp.delete()
            messages.error(request,"Company invalid or doesnt exist")
    context= {}
    return render(request,'base/newcompany.html',context)

def companyRoom(request):
    q= request.GET.get('q') if request.GET.get('q') != None else 'IBM'
    comp = Company.objects.get(name = q)
    prices = Prices.objects.filter(symbol = comp.pk)
    comp.updateCompany(symbol=comp.symbol)
    comp.save()
    if (prices.order_by('-date')[0].date != date.today()- timedelta(days=1)) and date.today().weekday()!=0 and date.today().weekday()!=1:
        Prices.update_values(Company.objects.first().pk)
        prices = Prices.objects.filter(symbol = comp.pk)
    df=pd.DataFrame.from_records(
        Prices.objects.filter(symbol = comp.pk).values('date','close')                                 
        )
    matplotlib.use('agg')
    plt.plot(df['date'],df['close'])
    fig=plt.gcf()
    buf=io.BytesIO()
    fig.savefig(buf,format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri=urllib.parse.quote(string)
    buf.close()
    plt.clf()
    
    returnOnSales = comp.netprofit/comp.grossprofit
    earnPerShare = comp.netprofit/comp.volume
    bookValue = (comp.assets-comp.liabilities)/comp.volume
    priceBookValue = float(df['close'].iloc[0])/bookValue
    percLiab= (comp.liabilities/comp.assets)*100
    
    
    context={
        'company':comp.name,
        'prices':df[:5].to_html(),
        'fig':uri,
        'returnOnSales':returnOnSales,
        'earnPerShare':earnPerShare,
        'bookValue':bookValue,
        'priceBookValue':priceBookValue,
        'percLiab':percLiab,    

        }
    return render(request,'base/company.html',context)