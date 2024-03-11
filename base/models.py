from django.db import models
from django.contrib.auth.models import User
import requests
from polygon import RESTClient
import pandas as pd
from datetime import datetime,date
from django.contrib.auth.models import AbstractUser
from django.db import models
from utils.model_abstracts import Model
import os
class Company(models.Model):
    name = models.CharField(max_length=200)
    symbol = models.CharField(max_length=20,unique=True)
    volume = models.BigIntegerField(null = True)
    netprofit = models.BigIntegerField(null = True)
    assets = models.BigIntegerField(null = True)
    liabilities = models.BigIntegerField(null = True)
    grossprofit = models.BigIntegerField(null = True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    
    def updateCompany(self,symbol):
        base_url = 'https://financialmodelingprep.com/api/v3/financial-statement-full-as-reported/'
        api_key=os.environ.get("API_KEY_FINANCIAL")
        params = {
            'period': 'annual',
            'apikey': api_key,
        }
        try:
            response = requests.get(f'{base_url}{symbol}', params=params)
            data = response.json()
            self.netprofit=int(data[0]['netincomeloss'])
            self.assets=int(data[0]['assets'])
            self.liabilities=int(data[0]['liabilitiescurrent'])
            self.grossprofit=int(data[0]['grossprofit'])
        except:
            pass
        base_url = 'https://api.polygon.io/v3/reference/tickers/' +symbol
        api_key=os.environ.get("API_KEY_POLYGON")
        params = {
            'apiKey': api_key,
        }
        try:   
            response = requests.get(base_url,params=params)
            data = response.json()
            self.volume=int(data['results']['share_class_shares_outstanding'])
        except:
            pass

class Prices(models.Model):
    symbol = models.ForeignKey(Company, on_delete = models.CASCADE)
    date = models.DateField()
    open = models.DecimalField(max_digits=15, decimal_places=4)
    close = models.DecimalField(max_digits=15, decimal_places=4)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add= True)
    
    class Meta:
        ordering = ['-date']
    def __str__(self):
        return str(self.symbol)

    @classmethod
    def update_values(cls,company_id):
        company = Company.objects.get(pk=company_id)   
        api_key = os.environ.get("API_KEY_POLYGON")
        try:   
            client = RESTClient(api_key=api_key)
            price_o=[]
            price_c=[]
            dates=[]
            for a in client.list_aggs(ticker=company.symbol, multiplier=1, timespan="day", from_="2023-01-01", to=date.today(), limit=50000):
                price_o.append(a.open)
                price_c.append(a.close)
                dates.append(a.timestamp)

            pre_df={'dates':[datetime.fromtimestamp(ts/1000).date() for ts in dates],'open':price_o,'close':price_c}
            df=pd.DataFrame(pre_df)

            for index,row in df.iterrows():
                x,y = cls.objects.get_or_create(
                    symbol = company, date= row['dates'], defaults={'open':row['open'], 'close': row['close']}
                )
        #fix for limited api connections
        except:
            pass
            