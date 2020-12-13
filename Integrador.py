from tkinter import *
from tkinter import messagebox as m_box
from tkinter import filedialog
import os
import yfinance as yf
import pandas as pd
from tkcalendar import *
from datetime import timedelta, date, datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle
from matplotlib.gridspec import GridSpec
import binascii
import re


#Genero el cuadro para que el usuario pueda pedir la información que desea
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

#Texto para elegir el gráfico
labelGrafico = Label(miFrame, text = "Seleccione un tipo de gráfico")
labelGrafico.grid(row = 4, column = 2, pady = 5, padx = 5)

#Variable gáfico
variableGrafico = StringVar(root)
variableGrafico.set("Velas")

#Opciones de gráfico
graficoOptionMenu = OptionMenu(miFrame, variableGrafico, "Velas", "Open", "High", "Low", "Close", "OHLC")
graficoOptionMenu.grid(row = 4, column = 3, pady = 5, padx = 5)

# Texto de derivada discreta
labelDerivadaDiscreta = Label(miFrame, text = "Graficar la derivada discreta")
labelDerivadaDiscreta.grid(row = 1, column = 2, pady = 5, padx = 5, sticky = "w")

#Creo los check box para elegir si quiere graficar las derivadas discretas
varDerivadaDiscretaTicker1 = IntVar()
Checkbutton(miFrame, text = "", variable = varDerivadaDiscretaTicker1).grid(row = 2, column = 2, pady = 5, padx = 5)

varDerivadaDiscretaTicker2 = IntVar()
Checkbutton(miFrame, text = "", variable = varDerivadaDiscretaTicker2).grid(row = 3, column = 2, pady = 5, padx = 5)

#Texto de color de las velas ascendentes
labelColorAscendente = Label(miFrame, text = "Ingrese el color de la vela ascendente en formato RGB")
labelColorAscendente.grid(row = 1, column = 3, padx = 5, pady = 5, sticky = "w")

#Creo los input para los colores ascendentes
#Pongo por default el color verde
defaultAscendente = StringVar(miFrame, value = "#4DFF00")
entryColorAscendenteTicker1 = Entry(miFrame, textvariable = defaultAscendente)
entryColorAscendenteTicker1.grid(row = 2, column = 3, padx = 5, pady = 5)

entryColorAscendenteTicker2 = Entry(miFrame, textvariable = defaultAscendente)
entryColorAscendenteTicker2.grid(row = 3, column = 3, padx = 5, pady = 5)

#Texto de color de las velas descendentes
labelColorDescendente = Label(miFrame, text = "Ingrese el color de la vela descendente en formato RGB")
labelColorDescendente.grid(row = 1, column = 4, padx = 5, pady = 5, sticky = "w")

#Creo los input para los colores ascendentes
#Pongo por default el color rojo
defaultDescendente = StringVar(miFrame, value = "#FF0000")
entryColorDescendenteTicker1 = Entry(miFrame, textvariable = defaultDescendente)
entryColorDescendenteTicker1.grid(row = 2, column = 4, padx = 5, pady = 5)

entryColorDescendenteTicker2 = Entry(miFrame, textvariable = defaultDescendente)
entryColorDescendenteTicker2.grid(row = 3, column = 4, padx = 5, pady = 5)

#Creo el texto y el calendario para la fecha de inicio
labelCalInicio = Label(miFrame, text = "Seleccione la fecha de inicio")
labelCalInicio.grid(row = 7, column = 1, padx = 5)

diaHoy = date.today()
calInicio = Calendar(miFrame, selectmode="day", year = diaHoy.year,  month = diaHoy.month, day = diaHoy.day, date_pattern = 'y-mm-dd')
calInicio.grid(row = 8, column = 1, pady = 5, padx = 5)

#Creo el texto y el calendario para la fecha de finalización
labelCalFin = Label(miFrame, text = "Seleccione la fecha de fin")
labelCalFin.grid(row = 7, column = 3, padx = 5)

calFin = Calendar(miFrame, selectmode="day", year = diaHoy.year,  month = diaHoy.month, day = diaHoy.day, date_pattern = 'y-mm-dd')
calFin.grid(row = 8, column = 3, pady = 5, padx = 5)

#Texto para elegir el path
labelBotonBuscar = Label(miFrame, text = "Seleccione donde desea guardar el archivo")
labelBotonBuscar.grid(row = 9, column = 0, pady = 5, padx = 5, sticky = "nw")

#Calculos de los tickers pedidos por el usuario
#Creo el texto para la empresa que más creció en el mes pasado
labelCrecioMasPasado = Label(miFrame, text = "")
labelCrecioMasPasado.grid(row = 10, column = 0, pady = 5, padx = 5, sticky = "nw")

#Creo el texto para la empresa que más creció en el mes pasado
labelCrecioMasAnterior = Label(miFrame, text = "")
labelCrecioMasAnterior.grid(row = 11, column = 0, pady = 5, padx = 5, sticky = "nw")

#Creo el texto para la empresa que más creció en el último año
labelCrecioMasAño = Label(miFrame, text = "")
labelCrecioMasAño.grid(row = 12, column = 0, pady = 5, padx = 5, sticky = "nw")

#Función para elegir a donde se va a descargar el archivo
def browsefunc(): 
    global directory 
    directory = filedialog.askdirectory(initialdir='.')

#Creo función para conseguir los datos de los tickers en Yahoo Finance
def consigo_datos(ticker, start_date, end_date, intervalo):

    #Creo el elemento ticker
    ticker = yf.Ticker(ticker)

    #Llamo los datos
    datos = ticker.history(start = start_date, end = end_date, interval = intervalo)

   #Verifico que el ticker exista y sino que devuelva los datos del ticker
    if datos.empty:
        m_box.showerror('Error', "Error en " + str(ticker) + ", ingrese otro")
    else:
        return(datos)

#Creo la función para buscar los tickers pedidos
def llamo_ticker(ticker1_entry, ticker2_entry, start_date, end_date, intervalo):
    tickers = [ticker1_entry, ticker2_entry]
    datos = pd.DataFrame()

    for ticker in tickers:
        #Traigo los datos del ticker
        datos = consigo_datos(ticker, start_date, end_date, intervalo)

        grafico(datos, tickers.index(ticker))

        #Se llama distinto la columna date según el timeframe
        if variableIntervalo.get() == "1d" or variableIntervalo.get() == "5d" or variableIntervalo.get() == "1wk" or variableIntervalo.get() == "1mo" or variableIntervalo.get() == "3mo":
            date = datos["Date"]
        else:
            date = datos["Datetime"]

        #Verifico en que ticker estoy
        if ticker == tickers[0]:
            #Verifico que el check box del ticker 1 esté seleccionado y calculo su derivada discreta
            if varDerivadaDiscretaTicker1.get() == 1 and variableGrafico.get() == "Velas":
                datos.reset_index(inplace = True)
                derivada_discreta(datos["Open"], datos["Close"], date)
        
        if ticker == tickers[1]:
            #Verifico que el check box del ticker 2 esté seleccionado y calculo su derivada discreta
            if varDerivadaDiscretaTicker2.get() == 1 and variableGrafico.get() == "Velas":
                datos.reset_index(inplace = True)
                derivada_discreta(datos["Open"], datos["Close"], date)
    
    #Llamo a la función para ver cuál creció más 
    mayor_crecimiento_mes_pasado(ticker1_entry, ticker2_entry)
    mayor_crecimiento_mes_anterior(ticker1_entry, ticker2_entry)
    mayor_crecimiento_año(ticker1_entry, ticker2_entry)

    #Llamo a la función para ver donde se intersectan 
    match_aux(ticker1_entry, ticker2_entry, start_date, end_date, intervalo)
    
    #Llamo a la función excel para que me genere el archivo
    excel(ticker1_entry, ticker2_entry, date)

    

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

#Calculo los mayores crecimientos en cada intervalo pedido
def mayor_crecimiento_mes_pasado(ticker1, ticker2):
    max_pasado = ' '
    #Como me pide que acción creció mas no necesito traer todos los datos
    #Para optimizar el programa voy a traer con un intervalo diario la información del primer día y del último día
    intervalo = "1d"

    #Para el mes pasado (ej. si es Noviembre, el de Octubre)
    ultimoDiaPasado = date.today().replace(day=1) - timedelta(days=1)
    primerDiaPasado = date(day=1, month= ultimoDiaPasado.month, year= ultimoDiaPasado.year)

    datosPasadoTicker1 = consigo_datos(ticker1, primerDiaPasado, ultimoDiaPasado, intervalo)
    datosPasadoTicker2 = consigo_datos(ticker2, primerDiaPasado, ultimoDiaPasado, intervalo)

    cuanto_crecio_mesPasado_ticker1 = cuanto_crecio(datosPasadoTicker1)
    cuanto_crecio_mesPasado_ticker2 = cuanto_crecio(datosPasadoTicker2)

    if cuanto_crecio_mesPasado_ticker1 > cuanto_crecio_mesPasado_ticker2:
        max_pasado = ticker1
        labelCrecioMasPasado.configure(text ="El ticker que mas creció el mes pasado (" + str(ultimoDiaPasado.strftime('%B')) + ") fue " + ticker1 + " con un crecimiento del " + str(round(cuanto_crecio_mesPasado_ticker1 * 100, 2)) + "%")
    if cuanto_crecio_mesPasado_ticker1 < cuanto_crecio_mesPasado_ticker2:
        max_pasado = ticker2
        labelCrecioMasPasado.configure(text = "El ticker que mas creció el mes pasado (" + str(ultimoDiaPasado.strftime('%B')) + ") fue " + ticker2 + " con un crecimiento del " + str(round(cuanto_crecio_mesPasado_ticker2 * 100, 2)) + "%")
    if cuanto_crecio_mesPasado_ticker1 == cuanto_crecio_mesPasado_ticker2:
        max_pasado = 'Ambos'
        labelCrecioMasPasado.configure(text = "Ambos tickers crecieron lo mismo el mes pasado (" + str(ultimoDiaPasado.strftime('%B')) + ") con un crecimiento del " + str(round(cuanto_crecio_mesPasado_ticker2 * 100, 2)) + "%")
    return max_pasado

def mayor_crecimiento_mes_anterior(ticker1, ticker2):
    max_anterior = ' '
    intervalo = "1d"
    #Para el mes anterior al pasado (ej. si es Noviembre, el de Septiembre)
    ultimoDiaPasado = date.today().replace(day=1) - timedelta(days=1)
    ultimoDiaAnterior = ultimoDiaPasado.replace(day = 1) - timedelta(days = 1)
    primerDiaAnterior = date(day = 1, month = ultimoDiaAnterior.month, year = ultimoDiaAnterior.year)

    datosAnteriorTicker1 = consigo_datos(ticker1, primerDiaAnterior, ultimoDiaAnterior, intervalo)
    datosAnteriorTicker2 = consigo_datos(ticker2, primerDiaAnterior, ultimoDiaAnterior, intervalo)
  
    #Calcula cuál fue el que más creció el mes anterior (Septiembre)
    cuanto_crecio_mesAnterior_ticker1 = cuanto_crecio(datosAnteriorTicker1)
    cuanto_crecio_mesAnterior_ticker2 = cuanto_crecio(datosAnteriorTicker2)
    
    if cuanto_crecio_mesAnterior_ticker1 > cuanto_crecio_mesAnterior_ticker2:
        max_anterior = ticker1
        labelCrecioMasAnterior.configure(text = "El ticker que mas creció el mes anterior (" + str(ultimoDiaAnterior.strftime('%B')) + ") fue " + ticker1 + " con un crecimiento del " + str(round(cuanto_crecio_mesAnterior_ticker1 * 100, 2)) + "%")
    if cuanto_crecio_mesAnterior_ticker1 < cuanto_crecio_mesAnterior_ticker2:
        max_anterior = ticker2
        labelCrecioMasAnterior.configure(text = "El ticker que mas creció el mes anterior (" + str(ultimoDiaAnterior.strftime('%B')) + ") fue " + ticker2 + " con un crecimiento del " + str(round(cuanto_crecio_mesAnterior_ticker2 * 100, 2)) + "%")
    if cuanto_crecio_mesAnterior_ticker1 == cuanto_crecio_mesAnterior_ticker2:
        max_anterior = 'Ambis'
        labelCrecioMasAnterior.configure(text = "Ambos tickers crecieron lo mismo el mes anterior (" + str(ultimoDiaAnterior.strftime('%B')) + ") con un crecimiento del " + str(round(cuanto_crecio_mesAnterior_ticker2 * 100, 2)) + "%")
    return max_anterior

def mayor_crecimiento_año(ticker1, ticker2):
    max_año = ' '
    intervalo = "1d"
    #Para todo el año pasado
    ultimoDiaAño = date.today()
    primerDiaAño = date(day = ultimoDiaAño.day, month = ultimoDiaAño.month, year = ultimoDiaAño.year - 1)

    datosAñoTicker1 = consigo_datos(ticker1, primerDiaAño, ultimoDiaAño, intervalo)
    datosAñoTicker2 = consigo_datos(ticker2, primerDiaAño, ultimoDiaAño, intervalo)

    #Calcula cuál fue el que más creció el año pasado 
    cuanto_crecio_añoPasado_ticker1 = cuanto_crecio(datosAñoTicker1)
    cuanto_crecio_añoPasado_ticker2 = cuanto_crecio(datosAñoTicker2)

    if cuanto_crecio_añoPasado_ticker1 > cuanto_crecio_añoPasado_ticker2:
        max_año = ticker1
        labelCrecioMasAño.configure(text = "El ticker que mas creció en el último año fue " + ticker1 + " con un crecimiento del " + str(round(cuanto_crecio_añoPasado_ticker1 * 100,2)) + "%," )
    if cuanto_crecio_añoPasado_ticker1 < cuanto_crecio_añoPasado_ticker2:
        max_año = ticker2
        labelCrecioMasAño.configure(text = "El ticker que mas creció en el último año fue " + ticker2 + " con un crecimiento del " + str(round(cuanto_crecio_añoPasado_ticker2 * 100,2)) + "%")
    if cuanto_crecio_añoPasado_ticker1 == cuanto_crecio_añoPasado_ticker2:
        max_año = 'Ambos'
        labelCrecioMasAño.configure(text = "Ambos tickers crecieron lo mismo en el último año con un crecimiento del " + str(round(cuanto_crecio_añoPasado_ticker2 * 100,2)) + "%")
    return max_año

#Codigos para los gráficos
def chart_candlestick (openp, close, high, low, date, i, ticker):
    date = str(date)
    color=""
    price_coordinates = [high, low]
    date_coordinates = [date, date]
    plt.plot(date_coordinates, price_coordinates, color="black")

    #Pido los colores de los Data Entry del usuario
    #Si no se ponen colores pongo unos por default
    candlestick = bull_or_bear(openp, close)
    if ticker == 1:
        if (candlestick == "bull"):
            color = entryColorAscendenteTicker1.get()
        if (candlestick == "bear"):
            color = entryColorDescendenteTicker1.get()
        if (candlestick == "indesicion"):
            color = "#DEDEDE"
    else:
        if (candlestick == "bull"):
            color = entryColorAscendenteTicker2.get()
        if (candlestick == "bear"):
            color = entryColorDescendenteTicker2.get()
        if (candlestick == "indesicion"):
            color = "#DEDEDE"

    #Chequeo que el color sea correcto
    empieza_con(color)
    isrgbcolor(color)

    plt.gca().add_patch(Rectangle((i-0.5,openp),1,(close-openp),linewidth=0.5,edgecolor='black',facecolor=color))

def grafico(datos, ticker):
    datos.reset_index(inplace = True)
    ticker = ticker + 1
    high = datos["High"]
    #Se llama distinto la columna date según el timeframe
    if variableIntervalo.get() == "1d" or variableIntervalo.get() == "5d" or variableIntervalo.get() == "1wk" or variableIntervalo.get() == "1mo" or variableIntervalo.get() == "3mo":
        date = datos["Date"]
    else:
        date = datos["Datetime"]
    openp = datos["Open"]
    low = datos["Low"]
    close = datos["Close"]

    if variableGrafico.get() == "Velas":
        for i in range(0, len(close), 1):
            chart_candlestick(openp[i], close[i], high[i], low[i], date[i], i, ticker)
    
    if variableGrafico.get() == "Open":
        grafico_open(openp, date)
    
    if variableGrafico.get() == "Close":
        grafico_close(close, date)
    
    if variableGrafico.get() == "Low":
        grafico_low(low, date)
    
    if variableGrafico.get() == "High":
        grafico_high(high, date)
    
    if variableGrafico.get() == "OHLC":
        grafico_ohlc(openp, high, low, close, date)
    
def bull_or_bear(openp, close):
    if(openp > close):
        return("bear")
    if(openp < close):
        return("bull")
    if(close == openp):
        return("indesicion")

#Buscamos intersecciones
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

lista_inters = []
def match (tick1_high, tick1_low, tick2_high, tick2_low, i):
    if (tick1_low > tick2_high) or (tick2_low > tick1_high):
        return("No match")
    
    if (tick1_high > tick2_high > tick1_low > tick2_low):
        match_square(tick2_high, tick1_low, i)
        lista_inters.append(i)
    if (tick2_high > tick1_high > tick2_low > tick1_low):
        match_square(tick1_high, tick2_low, i)
        lista_inters.append(i)
    if (tick2_high > tick1_high and tick1_low > tick2_low):
        match_square(tick1_high, tick1_low, i)
        lista_inters.append(i)
    if (tick1_high > tick2_high and tick2_low > tick1_high):
        match_square(tick2_high, tick2_low, i)
        lista_inters.append(i)

#Grafica la derivada discreta
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

#Opción para elegir colores para las velas
def empieza_con(bgcolor):
    if not bgcolor.startswith('#'):
        raise ValueError(m_box.showerror('Error', 'El color debe empezar con un "#"'))

def isrgbcolor(value):
    _rgbstring = re.compile(r'#[a-fA-F0-9]{6}$')
    if _rgbstring.match(value) == None:
        raise ValueError(m_box.showerror('Error', 'Debe ser un color válido'))

def grafico_open(openp, date):
    plt.plot(date, openp)

def grafico_close(close, date):
    plt.plot(date, close)

def grafico_low (low, date):
    plt.plot(date, low)

def grafico_high(high, date):
    plt.plot(date, high)

def grafico_ohlc(openp, high, low, close, date):
    promedio = []
    #Para concatenar el promedio en una lista
    for i in range(0, len(openp), 1):
        promedio.append((openp[i] + high[i] + low[i] + close[i])/4)

    plt.plot(date, promedio)

#Creamos una función para poder generar el excel
def excel(ticker1, ticker2, date):
    lista_fechas = []

    #Creo un diccionario para que luego sea un df
    dicc = {'Empresas': [], 'Intersecciones': [], 'Cuál creció más': []}

    #Ingreso los tickers
    tickers = [ticker1, ticker2]
    
    #Busco cuál creció más en cada mes y lo agrego
    como_crecen = []
    como_crecen.append('Mes Pasado: ' + mayor_crecimiento_mes_pasado(ticker1, ticker2))
    como_crecen.append('Mes Anterior: ' + mayor_crecimiento_mes_anterior(ticker1, ticker2))
    como_crecen.append('Año: ' + mayor_crecimiento_año(ticker1, ticker2))

    #Agrego las fechas en que hubo intersección
    for i in lista_inters:
        lista_fechas.append(date[i])
    
    #Relleno los espacios en blanco
    largo_max = 0
    lista_largos = [len(tickers), len(como_crecen), len(lista_fechas)]
    for largo in lista_largos:
        if largo > largo_max:
            largo_max = largo
    
    if len(tickers) < largo_max:
        while len(tickers) != largo_max:
            tickers.append('-')
    
    if len(como_crecen) < largo_max:
        while len(como_crecen) != largo_max:
            como_crecen.append('-')
    
    if len(lista_fechas) < largo_max:
        while len(lista_fechas) != largo_max:
            lista_fechas.append('-')

    #Guardo las listas
    dicc['Empresas'] = tickers
    dicc['Cuál creció más'] = como_crecen
    dicc['Intersecciones'] = lista_fechas
    
    #Creo el data frame y después el archivo de excel
    df = pd.DataFrame.from_dict(dicc)
    try:
      df.to_excel(directory + "/Comparando acciones.xlsx")
    except Exception:
      m_box.showwarning('Aviso!', 'Si no selecciona una carpeta, no se van a guardar los datos')
    
#Boton para elegir el path
botonBuscar = Button(miFrame, text = "Buscar", command = lambda:browsefunc())
botonBuscar.grid(row=9, column=1, sticky='nw', padx=5, pady=5)

#Cuando tocas el boton llama a chart_candlestick
#Con lambda: lo que hace es no llamarla hasta que se toque el boton
#Con .get() recibo el cuadro de texto que me ingresan
botonEnvio = Button(root, text = "Graficar", pady = 5, command = lambda:llamo_ticker(entryTicker1.get(), entryTicker2.get(), calInicio.get_date(), calFin.get_date(), variableIntervalo.get()))
botonEnvio.pack()

root.mainloop()