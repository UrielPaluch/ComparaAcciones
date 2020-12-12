from tkinter import *
import yfinance as yf
import pandas as pd
from tkcalendar import *
from datetime import timedelta, date


#Creo la raiz
root = Tk()

#Cambia el título
root.title("Compara acciones")

#Creo el frame
miFrame = Frame(root, width = 1200, height = 600)
miFrame.pack()

labelBienvenida = Label(miFrame, text = "Título de la pantalla")
labelBienvenida.grid(row = 0, column = 0, pady = 10)

labelInstruccionesTickers = Label(miFrame, text = "Ingrese los tickers que desea comparar")
labelInstruccionesTickers.grid(row = 1, column = 0, pady = 10)

labelTicker1 = Label(miFrame, text = "Ticker 1")
labelTicker1.grid(row = 2, column = 0, pady = 5, padx = 5, sticky = "w")

entryTicker1 = Entry(miFrame)
entryTicker1.grid(row = 2, column = 1, pady = 5, padx = 5)

labelTicker2 = Label(miFrame, text = "Ticker 2")
labelTicker2.grid(row = 3, column = 0, pady = 5, padx = 5, sticky = "w")

entryTicker2 = Entry(miFrame)
entryTicker2.grid(row = 3, column = 1, pady = 5, padx = 5)

variableIntervalo = StringVar(root)
variableIntervalo.set("1m")

labelIntervalo = Label(miFrame, text = "Seleccione un intervalo")
labelIntervalo.grid(row = 4, column = 0, pady = 5, padx = 5, sticky = "w")

intervaloOptionMenu = OptionMenu(miFrame, variableIntervalo, "1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo")
intervaloOptionMenu.grid(row = 4, column = 1, pady = 5, padx = 5)

labelCalInicio = Label(miFrame, text = "Seleccione la fecha de inicio")
labelCalInicio.grid(row = 5, column = 0, padx = 5)

calInicio = Calendar(miFrame, selectmode="day", year = 2020,  month = 5, day = 22, date_pattern = 'y-mm-dd')
calInicio.grid(row = 6, column = 0, pady = 5, padx = 5)

labelCalFin = Label(miFrame, text = "Seleccione la fecha de fin")
labelCalFin.grid(row = 5, column = 1, padx = 5)

calFin = Calendar(miFrame, selectmode="day", year = 2020,  month = 5, day = 22, date_pattern = 'y-mm-dd')
calFin.grid(row = 6, column = 1, pady = 5, padx = 5)

def llamo_ticker(ticker1_entry, ticker2_entry, start_date, end_date, intervalo):
    tickers = [ticker1_entry, ticker2_entry]

    for ticker in tickers:

        datos = consigo_datos(ticker, start_date, end_date, intervalo)
    
        print(datos)

def consigo_datos(ticker, start_date, end_date, intervalo):

    #Creo el elemento ticker
    ticker = yf.Ticker(ticker)

    #Llamo los datos
    datos = ticker.history(start = start_date, end = end_date, interval = intervalo)

    if datos.empty:
        return( print( 'Ticker no válido') )

    else:
        return(datos)


#Cuando tocas el boton llama a chart_candlestick
#Con lambda: lo que hace es no llamarla hasta que se toque el boton
#Con .get() recibo el cuadro de texto que me ingresan
botonEnvio = Button(root, text = "Graficar", pady = 5, command = lambda:llamo_ticker(entryTicker1.get(), entryTicker2.get(), calInicio.get_date(), calFin.get_date(), variableIntervalo.get()))
botonEnvio.pack()

root.mainloop()
    