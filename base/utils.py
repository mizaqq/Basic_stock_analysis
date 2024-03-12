import matplotlib.pyplot as plt
import io
import urllib,base64
import pandas as pd
import matplotlib
from .models import Prices
from datetime import date, timedelta

def make_plot(df,days: int = 0, intervals:int = 5):
    if(days!=0):
        df=df[:days]
    matplotlib.use('agg')
    plt.plot(df['date'],df['close'])
    begin=df['date'].iloc[-1]
    end=df['date'][0]
    total_duration=begin-end
    interval_duration = total_duration / intervals
    date_list = []
    for i in range(intervals + 1):
        date_list.append(begin - i * interval_duration)
        
    plt.xticks(date_list[::-1])
    plt.grid()
    fig=plt.gcf()
    buf=io.BytesIO()
    fig.savefig(buf,format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri=urllib.parse.quote(string)
    buf.close()
    plt.clf()
    return uri
def update_price(comp):
    prices = Prices.objects.filter(symbol = comp.pk)
    if(prices.order_by('-date')[0].date != date.today()-timedelta(1) 
       and prices.order_by('-date')[0].updated.date()!=date.today()
       and ((date.today().weekday != 5 and date.today().weekday() != 6) 
            or prices.order_by('-date')[0].updated.date()<date.today()-timedelta(6))
       ):
        Prices.update_values(comp.pk)
        