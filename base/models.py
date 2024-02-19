from django.db import models
from django.contrib.auth.models import User
import requests
from polygon import RESTClient
import pandas as pd
from datetime import datetime,date
# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=200)
    symbol = models.CharField(max_length=20,unique=True)
    volume = models.BigIntegerField(null = True)
    
    def __str__(self):
        return self.name


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
        client = RESTClient(api_key="JfpEqKFDa_3455NuDEF6DhE8Q2_E7gxR")
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