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
labelBienvenida.grid(row = 0, column = 0, pady = 10, sticky = "nw")
labelBienvenida.grid_propagate(0)

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

labelCrecioMasPasado = Label(miFrame, text = "")
labelCrecioMasPasado.grid(row = 7, column = 0, pady = 5, padx = 5, sticky = "nw")

labelCrecioMasAnterior = Label(miFrame, text = "")
labelCrecioMasAnterior.grid(row = 8, column = 0, pady = 5, padx = 5, sticky = "nw")

def llamo_ticker(ticker1_entry, ticker2_entry, start_date, end_date, intervalo):
    tickers = [ticker1_entry, ticker2_entry]

    for ticker in tickers:

        datos = consigo_datos(ticker, start_date, end_date, intervalo)
    
        print(datos)
    
    mayor_crecimiento(ticker1_entry, ticker2_entry, intervalo)

def consigo_datos(ticker, start_date, end_date, intervalo):

    #Creo el elemento ticker
    ticker = yf.Ticker(ticker)

    #Llamo los datos
    datos = ticker.history(start = start_date, end = end_date, interval = intervalo)

    if datos.empty:
        return(print('Ticker no válido'))
        

    else:
        return(datos)

def mayor_crecimiento(ticker1, ticker2, intervalo):

    #Como me pide que acción creció mas no necesito traer todos los datos
    #Para optimizar el programa voy a traer con un intervalo mensual la información del primer día y del último día

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

    if cuanto_crecio_mesPasado_ticker1 > cuanto_crecio_mesPasado_ticker2:
        labelCrecioMasPasado.configure(text ="El ticker que mas creció el mes pasado (" + str(ultimoDiaPasado.strftime('%B')) + ") fue " + ticker1 + " con un crecimiento del " + str(cuanto_crecio_mesPasado_ticker1 * 100) + "%")
    if cuanto_crecio_mesPasado_ticker1 < cuanto_crecio_mesPasado_ticker2:
        labelCrecioMasPasado.configure(text = "El ticker que mas creció el mes pasado (" + str(ultimoDiaPasado.strftime('%B')) + ") fue " + ticker2 + " con un crecimiento del " + str(cuanto_crecio_mesPasado_ticker2 * 100) + "%")
    if cuanto_crecio_mesPasado_ticker1 == cuanto_crecio_mesPasado_ticker2:
        labelCrecioMasPasado.configure(text = "Ambos tickers crecieron lo mismo el mes pasado (" + str(ultimoDiaPasado.strftime('%B')) + ") con un crecimiento del " + str(cuanto_crecio_mesPasado_ticker2 * 100) + "%")
    
    cuanto_crecio_mesAnterior_ticker1 = cuanto_crecio(datosAnteriorTicker1)
    cuanto_crecio_mesAnterior_ticker2 = cuanto_crecio(datosAnteriorTicker2)
    
    if cuanto_crecio_mesAnterior_ticker1 > cuanto_crecio_mesAnterior_ticker2:
        labelCrecioMasAnterior.configure(text = "El ticker que mas creció el mes anterior (" + str(ultimoDiaAnterior.strftime('%B')) + ") fue " + ticker1 + " con un crecimiento del " + str(cuanto_crecio_mesAnterior_ticker1 * 100) + "%")
    if cuanto_crecio_mesAnterior_ticker1 < cuanto_crecio_mesAnterior_ticker2:
        labelCrecioMasAnterior.configure(text = "El ticker que mas creció el mes anterior (" + str(ultimoDiaAnterior.strftime('%B')) + ") fue " + ticker2 + " con un crecimiento del " + str(cuanto_crecio_mesAnterior_ticker2 * 100) + "%")
    if cuanto_crecio_mesAnterior_ticker1 == cuanto_crecio_mesAnterior_ticker2:
        labelCrecioMasAnterior.configure(text = "Ambos tickers crecieron lo mismo el mes anterior (" + str(ultimoDiaAnterior.strftime('%B')) + ") con un crecimiento del " + str(cuanto_crecio_mesAnterior_ticker2 * 100) + "%")

def cuanto_crecio(dataframe):
    dataframe.reset_index(inplace = True)
    lista = dataframe.to_dict("list")
    #Creo un for para que me guarde el último dato, llegado el caso de que por algún motivo no se haya operado el ticker yfinance me devuelve dos datos
    for i in range(0, len(lista["Close"]), 1):
        crecimiento = dataframe["Close"][i] / dataframe["Open"][i] - 1
    return(crecimiento)

#Cuando tocas el boton llama a chart_candlestick
#Con lambda: lo que hace es no llamarla hasta que se toque el boton
#Con .get() recibo el cuadro de texto que me ingresan
botonEnvio = Button(root, text = "Graficar", pady = 5, command = lambda:llamo_ticker(entryTicker1.get(), entryTicker2.get(), calInicio.get_date(), calFin.get_date(), variableIntervalo.get()))
botonEnvio.pack()

root.mainloop()
    