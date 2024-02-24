import matplotlib.pyplot as plt
import io
import urllib,base64
import pandas as pd
import matplotlib

def make_plot(df):
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
    return uri