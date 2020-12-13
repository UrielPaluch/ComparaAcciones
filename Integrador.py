from tkinter import *
import yfinance as yf
import pandas as pd
from tkcalendar import *
from datetime import timedelta, date, datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle
from matplotlib.gridspec import GridSpec

#               Genero el cuadro para que el usuario pueda pedir la información que desea
#Creo la raiz
root = Tk()

#Cambia el título
root.title("Compara acciones")

#Creo el frame
miFrame = Frame(root, width = 1200, height = 600)
miFrame.pack()

#Creo el título del frame
labelBienvenida = Label(miFrame, text = "Comparación de las acciones de dos empresas")
labelBienvenida.grid(row = 0, column = 0, pady = 10, sticky = "nw")
labelBienvenida.grid_propagate(0)

#Creo el título para ingresar los tickers
labelInstruccionesTickers = Label(miFrame, text = "Ingrese los tickers que desea comparar")
labelInstruccionesTickers.grid(row = 1, column = 0, pady = 10)

#Título del ticker1
labelTicker1 = Label(miFrame, text = "Ticker 1")
labelTicker1.grid(row = 2, column = 0, pady = 5, padx = 5, sticky = "w")

#Cuadro de texto para ingresar el ticker1
entryTicker1 = Entry(miFrame)
entryTicker1.grid(row = 2, column = 1, pady = 5, padx = 5)

#Título del ticker2
labelTicker2 = Label(miFrame, text = "Ticker 2")
labelTicker2.grid(row = 3, column = 0, pady = 5, padx = 5, sticky = "w")

#Cuadro de texto para ingresar el ticker2
entryTicker2 = Entry(miFrame)
entryTicker2.grid(row = 3, column = 1, pady = 5, padx = 5)

#Texto para elegir el intervalo
labelIntervalo = Label(miFrame, text = "Seleccione un intervalo")
labelIntervalo.grid(row = 4, column = 0, pady = 5, padx = 5, sticky = "w")

#Botón para elegir el intervalo
variableIntervalo = StringVar(root)
variableIntervalo.set("1d")

#Opciones de intervalos
intervaloOptionMenu = OptionMenu(miFrame, variableIntervalo, "1m", "2m", "5m", "15m", "30m", "60m", "90m", "1d", "5d", "1wk", "1mo", "3mo")
intervaloOptionMenu.grid(row = 4, column = 1, pady = 5, padx = 5)

# Texto de derivada discreta
labelDerivadaDiscreta = Label(miFrame, text = "Graficar la derivada discreta")
labelDerivadaDiscreta.grid(row = 1, column = 2, pady = 5, padx = 5, sticky = "w")


#Creo los check box para elegir si quiere graficar las derivadas discretas
varDerivadaDiscretaTicker1 = IntVar()
Checkbutton(miFrame, text = "", variable = varDerivadaDiscretaTicker1).grid(row = 2, column = 2, pady = 5, padx = 5)

varDerivadaDiscretaTicker2 = IntVar()
Checkbutton(miFrame, text = "", variable = varDerivadaDiscretaTicker2).grid(row = 3, column = 2, pady = 5, padx = 5)


#Creo el texto y el calendario para la fecha de inicio
labelCalInicio = Label(miFrame, text = "Seleccione la fecha de inicio")
labelCalInicio.grid(row = 6, column = 0, padx = 5)

diaHoy = date.today()
calInicio = Calendar(miFrame, selectmode="day", year = diaHoy.year,  month = diaHoy.month, day = diaHoy.day, date_pattern = 'y-mm-dd')
calInicio.grid(row = 7, column = 0, pady = 5, padx = 5)


#Creo el texto y el calendario para la fecha de finalización
labelCalFin = Label(miFrame, text = "Seleccione la fecha de fin")
labelCalFin.grid(row = 6, column = 1, padx = 5)

calFin = Calendar(miFrame, selectmode="day", year = diaHoy.year,  month = diaHoy.month, day = diaHoy.day, date_pattern = 'y-mm-dd')
calFin.grid(row = 7, column = 1, pady = 5, padx = 5)



#               Calculos de los tickers pedidos por el usuario
#Creo el texto para la empresa que más creció
labelCrecioMasPasado = Label(miFrame, text = "")
labelCrecioMasPasado.grid(row = 8, column = 0, pady = 5, padx = 5, sticky = "nw")

#Creo el texto para la empresa que menos creció
labelCrecioMasAnterior = Label(miFrame, text = "")
labelCrecioMasAnterior.grid(row = 9, column = 0, pady = 5, padx = 5, sticky = "nw")


#Creo función para conseguir los datos de los tickers en Yahoo Finance
def consigo_datos(ticker, start_date, end_date, intervalo):

    #Creo el elemento ticker
    ticker = yf.Ticker(ticker)

    #Llamo los datos
    datos = ticker.history(start = start_date, end = end_date, interval = intervalo)

   #Verifico que el ticker exista y sino que devuelva los datos del ticker
    if datos.empty:
        rootError = Tk()
        rootError.title("Error")
        rootError.resizable(False, False)
        rootError.geometry("300x300")

        frameError = Frame(rootError, width = 300, height = 300)
        frameError.pack()

        labelError = Label(frameError, text = "Error en " + str(ticker) + ", ingrese otro")
        labelError.pack()
        rootError.mainloop()
    
    else:
        return(datos)



#Creo la función para buscar los tickers pedidos
def llamo_ticker(ticker1_entry, ticker2_entry, start_date, end_date, intervalo):
    tickers = [ticker1_entry, ticker2_entry]
    datos = pd.DataFrame()

    for ticker in tickers:

        #Traigo los datos del ticker
        datos = consigo_datos(ticker, start_date, end_date, intervalo)

        grafico(datos)

        #Se llama distinto la columna date según el timeframe
        if variableIntervalo.get() == "1d" or variableIntervalo.get() == "5d" or variableIntervalo.get() == "1wk" or variableIntervalo.get() == "1mo" or variableIntervalo.get() == "3mo":
            date = datos["Date"]
        else:
            date = datos["Datetime"]

        
        #Verifico en que ticker estoy

        if ticker == tickers[0]:

            #Verifico que el check box del ticker 1 esté seleccionado y calculo su derivada discreta
            if varDerivadaDiscretaTicker1.get() == 1:
                datos.reset_index(inplace = True)
                derivada_discreta(datos["Open"], datos["Close"], date)
        
        if ticker == tickers[1]:

            #Verifico que el check box del ticker 2 esté seleccionado y calculo su derivada discreta
            if varDerivadaDiscretaTicker2.get() == 1:
                datos.reset_index(inplace = True)
                derivada_discreta(datos["Open"], datos["Close"], date)
    
    #Llamo a la función para ver cuál creció más 
    mayor_crecimiento(ticker1_entry, ticker2_entry)

    #Llamo a la función para ver donde se intersectan 
    match_aux(ticker1_entry, ticker2_entry, start_date, end_date, intervalo)

    

    #Genero los títulos del gráfico comparativo
    plt.title(ticker1_entry + " vs " + ticker2_entry)
    plt.xticks(rotation=15)
    plt.xlabel("Tiempo")
    plt.ylabel("Precio")
    plt.xticks(visible = False)
    plt.legend()
    plt.show()


#Función para encontrar cuanto crecio cada ticker en un intervalo
def cuanto_crecio(dataframe):
    dataframe.reset_index(inplace = True)
    lista = dataframe.to_dict("list")
    #Creo un for para que me guarde el último dato, llegado el caso de que por algún motivo no se haya operado el ticker yfinance me devuelve dos datos
    for i in range(0, len(lista["Close"]), 1):
        crecimiento = dataframe["Close"][i] / dataframe["Open"][i] - 1
    return(crecimiento)


def mayor_crecimiento(ticker1, ticker2):

#Como me pide que acción creció mas no necesito traer todos los datos
#Para optimizar el programa voy a traer con un intervalo diario la información del primer día y del último día
    intervalo = "1d"
    ultimoDiaPasado = date.today().replace(day=1) - timedelta(days=1)
    primerDiaPasado = date(day=1, month= ultimoDiaPasado.month, year= ultimoDiaPasado.year)

    datosPasadoTicker1 = consigo_datos(ticker1, primerDiaPasado, ultimoDiaPasado, intervalo)
    datosPasadoTicker2 = consigo_datos(ticker2, primerDiaPasado, ultimoDiaPasado, intervalo)

    ultimoDiaAnterior = ultimoDiaPasado.replace(day = 1) - timedelta(days = 1)
    primerDiaAnterior = date(day = 1, month = ultimoDiaAnterior.month, year = ultimoDiaAnterior.year)

    datosAnteriorTicker1 = consigo_datos(ticker1, primerDiaAnterior, ultimoDiaAnterior, intervalo)
    datosAnteriorTicker2 = consigo_datos(ticker2, primerDiaAnterior, ultimoDiaAnterior, intervalo)
  
    cuanto_crecio_mesPasado_ticker1 = cuanto_crecio(datosPasadoTicker1)
    cuanto_crecio_mesPasado_ticker2 = cuanto_crecio(datosPasadoTicker2)

    #Calcula cuál fue el que más creció el mes pasado (Octubre)
    if cuanto_crecio_mesPasado_ticker1 > cuanto_crecio_mesPasado_ticker2:
        labelCrecioMasPasado.configure(text ="El ticker que mas creció el mes pasado (" + str(ultimoDiaPasado.strftime('%B')) + ") fue " + ticker1 + " con un crecimiento del " + str(round(cuanto_crecio_mesPasado_ticker1 * 100, 2)) + "%")
    if cuanto_crecio_mesPasado_ticker1 < cuanto_crecio_mesPasado_ticker2:
        labelCrecioMasPasado.configure(text = "El ticker que mas creció el mes pasado (" + str(ultimoDiaPasado.strftime('%B')) + ") fue " + ticker2 + " con un crecimiento del " + str(round(cuanto_crecio_mesPasado_ticker2 * 100, 2)) + "%")
    if cuanto_crecio_mesPasado_ticker1 == cuanto_crecio_mesPasado_ticker2:
        labelCrecioMasPasado.configure(text = "Ambos tickers crecieron lo mismo el mes pasado (" + str(ultimoDiaPasado.strftime('%B')) + ") con un crecimiento del " + str(round(cuanto_crecio_mesPasado_ticker2 * 100, 2)) + "%")
    
    cuanto_crecio_mesAnterior_ticker1 = cuanto_crecio(datosAnteriorTicker1)
    cuanto_crecio_mesAnterior_ticker2 = cuanto_crecio(datosAnteriorTicker2)
    
    #Calcula cuál fue el que más creció el mes anterior (Septiembre)
    if cuanto_crecio_mesAnterior_ticker1 > cuanto_crecio_mesAnterior_ticker2:
        labelCrecioMasAnterior.configure(text = "El ticker que mas creció el mes anterior (" + str(ultimoDiaAnterior.strftime('%B')) + ") fue " + ticker1 + " con un crecimiento del " + str(round(cuanto_crecio_mesAnterior_ticker1 * 100, 2)) + "%")
    if cuanto_crecio_mesAnterior_ticker1 < cuanto_crecio_mesAnterior_ticker2:
        labelCrecioMasAnterior.configure(text = "El ticker que mas creció el mes anterior (" + str(ultimoDiaAnterior.strftime('%B')) + ") fue " + ticker2 + " con un crecimiento del " + str(round(cuanto_crecio_mesAnterior_ticker2 * 100, 2)) + "%")
    if cuanto_crecio_mesAnterior_ticker1 == cuanto_crecio_mesAnterior_ticker2:
        labelCrecioMasAnterior.configure(text = "Ambos tickers crecieron lo mismo el mes anterior (" + str(ultimoDiaAnterior.strftime('%B')) + ") con un crecimiento del " + str(round(cuanto_crecio_mesAnterior_ticker2 * 100, 2)) + "%")



def chart_candlestick (openp, close, high, low, date, i):
    date = str(date)
    color="red"
    price_coordinates = [high, low]
    date_coordinates = [date, date]
    plt.plot(date_coordinates, price_coordinates, color="black")

    candlestick = bull_or_bear(openp, close)
    if (candlestick == "bull"):
        color = "#5DFD5B"
    if (candlestick == "bear"):
        color = "#FF7051"
    if (candlestick == "indesicion"):
        color = "#DEDEDE"

    plt.gca().add_patch(Rectangle((i-0.5,openp),1,(close-openp),linewidth=0.5,edgecolor='black',facecolor=color))


def grafico(datos):

    datos.reset_index(inplace = True)

    high = datos["High"]
    #Se llama distinto la columna date según el timeframe
    if variableIntervalo.get() == "1d" or variableIntervalo.get() == "5d" or variableIntervalo.get() == "1wk" or variableIntervalo.get() == "1mo" or variableIntervalo.get() == "3mo":
        date = datos["Date"]
    else:
        date = datos["Datetime"]
    openp = datos["Open"]
    low = datos["Low"]
    close = datos["Close"]

    for i in range(0, len(close), 1):
        chart_candlestick(openp[i], close[i], high[i], low[i], date[i], i)


def bull_or_bear(openp, close):
    if(openp > close):
        return("bear")
    if(openp < close):
        return("bull")
    if(close == openp):
        return("indesicion")


def match_aux(ticker1, ticker2, start_date, end_date, intervalo):
    datos1 = consigo_datos(ticker1, start_date, end_date, intervalo)
    datos2 = consigo_datos(ticker2, start_date, end_date, intervalo)

    lista_datos1 = datos1.to_dict("list")
    ticker1_high = lista_datos1["High"]
    ticker1_low = lista_datos1["Low"]

    lista_datos2 = datos2.to_dict("list")
    ticker2_high = lista_datos2["High"]
    ticker2_low = lista_datos2["Low"]

    for i in range(0, len(ticker1_high), 1):
        match(ticker1_high[i], ticker1_low[i], ticker2_high[i], ticker2_low[i], i)


def match_square (mini, maxi, i):
    plt.gca().add_patch(Rectangle((i-0.5,mini),1,(maxi-mini),linewidth=0.5,edgecolor='black',facecolor='#ECFF00'))


def match (tick1_high, tick1_low, tick2_high, tick2_low, i):
    if (tick1_low > tick2_high) or (tick2_low > tick1_high):
        return("No match")
    
    if (tick1_high > tick2_high > tick1_low > tick2_low):
        match_square(tick2_high, tick1_low, i)
    if (tick2_high > tick1_high > tick2_low > tick1_low):
        match_square(tick1_high, tick2_low, i)
    if (tick2_high > tick1_high and tick1_low > tick2_low):
        match_square(tick1_high, tick1_low, i)
    if (tick1_high > tick2_high and tick2_low > tick1_high):
        match_square(tick2_high, tick2_low, i)


def derivada_discreta(open_price_entry, close_price_entry, date_entry):
    #Voy a hacer la derivada discreta entre el precio de cierre y el precio de apertura para ver si hay un gap

    open_price = list(open_price_entry)
    close_price = list(close_price_entry)
    date = list(date_entry)

    lista_gap = []
    lista_aux = []
    lista_date = []

    for i in range (0, len(date), 1):
        lista_aux.append(open_price[i])
        lista_date.append(str(date[i]))
        lista_aux.append(close_price[i])
        lista_date.append(str(date[i]))

    for i in range(0, len(open_price)-1, 1):
        lista_gap.append(close_price[i] - open_price[i+1])
    
    plt.plot(lista_date, lista_aux)

#Cuando tocas el boton llama a chart_candlestick
#Con lambda: lo que hace es no llamarla hasta que se toque el boton
#Con .get() recibo el cuadro de texto que me ingresan
botonEnvio = Button(root, text = "Graficar", pady = 5, command = lambda:llamo_ticker(entryTicker1.get(), entryTicker2.get(), calInicio.get_date(), calFin.get_date(), variableIntervalo.get()))
botonEnvio.pack()

root.mainloop()