from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from .models import Company,Prices
from datetime import date, timedelta
from .utils import make_plot,update_price
import pandas as pd
from django.http import JsonResponse
from rest_framework.authtoken.models import Token

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
            messages.error(request,list(form.errors.values()))
    context={'form':form}
    return render(request,'base/login_register.html',context)
    
def home(request):
    q= request.GET.get('q') if request.GET.get('q') != None else 'IBM'
    comp = Company.objects.get(name = q)
    update_price(comp)
    prices = Prices.objects.filter(symbol = comp.pk)
        
    companies= Company.objects.all()[0:5]
    
    context= {'companies':companies,'company':comp,'prices':prices[:5]}
    return render(request, 'base/home.html',context)

def getNewCompany(request):
    if request.method == "POST":
        name = request.POST.get('name')
        symbol = request.POST.get('symbol').upper()
        if Company.objects.filter(symbol=symbol).exists() == False:
            comp = Company(name=name, symbol = symbol)
            comp.save()
        else:
            comp= Company.objects.get(symbol=symbol)
        update_price(Company.objects.get(symbol = symbol))
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
    try:
        comp = Company.objects.get(name = q)
    except:
        messages.error(request,"Company not existing, add it")
        return redirect('newcompany')
    if(comp.updated.date() != date.today()):
        comp.updateCompany(symbol=comp.symbol)
        comp.save()
    update_price(comp)
    
    df=pd.DataFrame.from_records(
        Prices.objects.filter(symbol = comp.pk).values('date','close')                                 
        )
    uri = make_plot(df)
    uri3 = make_plot(df,55,3)
    
    if comp.grossprofit!=None:
        returnOnSales = comp.netprofit/comp.grossprofit
    else:
        returnOnSales = 0
        
    if comp.volume!=None:
        earnPerShare = comp.netprofit/comp.volume
        bookValue = (comp.assets-comp.liabilities)/comp.volume
        priceBookValue = float(df['close'].iloc[0])/bookValue
    else:
        earnPerShare=0
        bookValue=0 

    if comp.assets!=None:   
        percLiab= (comp.liabilities/comp.assets)*100
    else:
        percLiab=0
    
    context={
        'company':comp.name,
        'prices':df[:5],
        'fig':uri,
        'fig3':uri3,
        'returnOnSales':returnOnSales,
        'earnPerShare':earnPerShare,
        'bookValue':bookValue,
        'priceBookValue':priceBookValue,
        'percLiab':percLiab,    

        }
    return render(request,'base/company.html',context)


def userPage(request):
    if request.user.is_authenticated: 
        user = request.user
        try: 
            token=user.auth_token
        except:
            Token.objects.create(user=user)
            token=user.auth_token
    else:
        redirect(loginPage)
    context={'username':user.username,'token':token}
    return render(request,'base/user.html',context)



def reset_token(request):
    if request.user.is_authenticated: 
        user = request.user
        t = Token.objects.filter(user=user)
        new_token = t[0].generate_key()
        t.update(key=new_token)
    else:
        redirect(loginPage)
            
    return JsonResponse({'new_token': new_token})


    
