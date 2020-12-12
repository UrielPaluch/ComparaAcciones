import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle
from matplotlib.gridspec import GridSpec


def wget(url):
    r = requests.get(url, allow_redirects=True)
    with open(url[url.rfind('/') + 1::], 'wb') as f:
        f.write(r.content)

def chart_candlestick (openp, close, high, low, date, i):

    price_coordinates = [high, low]
    date_coordinates = [date, date]
    plt.plot(date_coordinates, price_coordinates, color="black")

    #plt.scatter(date, high, color="green")
    #plt.scatter(date, low, color="#ff0004")
    #plt.scatter(date, openp, color="#4bed15")
    #plt.scatter(date, close, color="#ad0a0d")

    candlestick = bull_or_bear(openp, close)
    if (candlestick == "bull"):
        color = "#5DFD5B"
    if (candlestick == "bear"):
        color = "#FF7051"
    if (candlestick == "indesicion"):
        color = "#DEDEDE"

    plt.gca().add_patch(Rectangle((i-0.5,openp),1,(close-openp),linewidth=0.5,edgecolor='black',facecolor=color))

def chart_candlestick_amzn (openp, close, high, low, date, i):

    price_coordinates = [high, low]
    date_coordinates = [date, date]
    plt.plot(date_coordinates, price_coordinates, color="black")

    #plt.scatter(date, high, color="green")
    #plt.scatter(date, low, color="#ff0004")
    #plt.scatter(date, openp, color="#4bed15")
    #plt.scatter(date, close, color="#ad0a0d")

    candlestick = bull_or_bear(openp, close)
    if (candlestick == "bull"):
        color = "#3855C2"
    if (candlestick == "bear"):
        color = "#C238AF"
    if (candlestick == "indesicion"):
        color = "#DEDEDE"

    plt.gca().add_patch(Rectangle((i-0.5,openp),1,(close-openp),linewidth=0.5,edgecolor='black',facecolor=color))

def bull_or_bear(openp, close):
    if(openp > close):
        return("bear")
    if(openp < close):
        return("bull")
    if(close == openp):
        return("indesicion")

def match (google_high, google_low, amzn_high, amzn_low, i):
    if (google_low > amzn_high):
        return("No match")
    if (amzn_low > google_high):
        return("No match")
    if(google_high > amzn_high > google_low > amzn_low):
        match_square(amzn_high, google_low, i)
    if (amzn_high > google_high > amzn_low > google_low):
        match_square(google_high, amzn_low, i)
    if(amzn_high > google_high and google_low > amzn_low):
        match_square(google_high, google_low, i)
    if (google_high > amzn_high and amzn_low > google_low):
        match_square(amzn_high, google_low, i)

def match_square (mini, maxi, i):
    plt.gca().add_patch(Rectangle((i-0.5,mini),1,(maxi-mini),linewidth=0.5,edgecolor='black',facecolor='#ECFF00'))

def derivada_discreta(open_price, close_price, date):
    #Voy a hacer la derivada discreta entre el precio de cierre y el precio de apertura para ver si hay un gap
    lista_gap = []
    lista_aux = []
    lista_date = []

    for i in range (0, len(date), 1):
        lista_aux.append(open_price[i])
        lista_date.append(date[i])
        lista_aux.append(close_price[i])
        lista_date.append(date[i])

    for i in range(0, len(open_price)-1, 1):
        lista_gap.append(close_price[i] - open_price[i+1])
    
    plt.plot(lista_date, lista_aux)
        

wget("https://raw.githubusercontent.com/LedesmaFran/python/master/GOOGLE.csv")

archivo_google = pd.read_csv("GOOGLE.csv")

data_google = archivo_google.to_dict("list")

google_high = data_google["High"]

google_low = data_google["Low"]

google_date = data_google["Date"]

google_open = data_google["Open"]

google_close = data_google["Close"]

google_volume = data_google["Volume"]

wget("https://raw.githubusercontent.com/LedesmaFran/python/master/AMZN.csv")

archivo_amzn = pd.read_csv("AMZN.csv")

data_amzn = archivo_amzn.to_dict("list")

amzn_high = data_amzn["High"]

amzn_low = data_amzn["Low"]

amzn_date = data_amzn["Date"]

amzn_open = data_amzn["Open"]

amzn_close = data_amzn["Close"]

for i in range(0, len(google_close), 1):
    chart_candlestick(google_open[i], google_close[i], google_high[i], google_low[i], google_date[i], i)

for i in range(0, len(amzn_close), 1):
    chart_candlestick_amzn(amzn_open[i], amzn_close[i], amzn_high[i], amzn_low[i], amzn_date[i], i)

for i in range(0, len(amzn_close), 1):
    match(google_high[i], google_low[i], amzn_high[i], amzn_low[i], i)

'''derivada_discreta(amzn_open, amzn_close, amzn_date)'''

#Google bull #5DFD5B verde
#Google bear #FF7051 rojo

#Amzn bull #3855C2 azul
#Amzn bear #C238AF violeta

#Match #ECFF00 amarillo

plt.xticks(rotation=45)

plt.title("Google vs Amazon")
plt.xlabel("Tiempo")
plt.ylabel("Precio")
plt.legend()
plt.show()