from datetime import datetime

def convert_2_datetime(date_list):
 return [datetime.strptime(date, "%Y-%m-%d") for date in date_list]

import matplotlib.pyplot as plt # type: ignore

import os

def extractora(archivos):

    # Creo un diccionario para cada accion con las claves de la fecha, open, high, low y close
   
    dic = {
        'Date': [],
        'Open': [],
        'High': [],
        'Low': [],
        'Close': []
    }

    with open(archivos, 'rt') as archivo:      
        for i, linea in enumerate(archivo, 1):
            linea = linea.rstrip('\n')
            if i == 1:
                claves = linea.split(',')
                for clave in claves:
                    dic[clave] = []
            else:
                datos_linea = linea.split(',')
                dic['Date'].append(datos_linea[0])
                dic['Open'].append(datos_linea[1])  
                dic['High'].append(datos_linea[2])
                dic['Low'].append(datos_linea[3])
                dic['Close'].append(datos_linea[4])

    return dic


def dic_acciones(carpeta):

    acciones = {}

    # Uso la funcion extractora donde cree un diccionario de cada accion y uno todos en esta funcion

    for archivo in os.listdir(carpeta):
        archivos = os.path.join(carpeta, archivo) 
        accion = os.path.splitext(archivo)[0]
        acciones[accion] = extractora(archivos) 

    return acciones

def graficadora(dic_acciones):

    for accion, datos in dic_acciones.items():

        # El for recorre cada accion y crea un grafico con todos los valores de cada una
   
        fechas = [datetime.strptime(fecha, '%Y-%m-%d') for fecha in datos['Date']]
        open_values = list(map(float, datos['Open']))
        high_values = list(map(float, datos['High']))
        low_values = list(map(float, datos['Low']))
        close_values = list(map(float, datos['Close']))
    
        plt.plot(fechas, open_values, label='Open')
        plt.plot(fechas, high_values, label='High')
        plt.plot(fechas, low_values, label='Low')
        plt.plot(fechas, close_values, label='Close')
        
        plt.title(accion)
        plt.xlabel("Fecha")
        plt.ylabel("Valor")
        plt.grid(visible=True, alpha=0.2)
        
        plt.show()

    return None

def graficarxclave(dic_acciones):

    claves = ['Open', 'High', 'Low', 'Close'] 

    for clave in claves:
        
        # Creo que grafico para cada una de las claves con todas las acciones

        for accion, datos in dic_acciones.items():
            fechas = [datetime.strptime(fecha, '%Y-%m-%d') for fecha in datos['Date']]
            valores = list(map(float, datos[clave]))

            plt.plot(fechas, valores, label=accion)

        plt.title(clave)
        plt.xlabel("Fecha")
        plt.ylabel(clave)
        plt.legend(title="Acciones")
        plt.grid(visible=True, alpha=0.2)

        plt.show()
    
    return None

def volatilidad(dic_acciones, archivotexto="volatilidad.txt"):
   
    resultados = []

    for accion, datos in dic_acciones.items():
      
        high = list(map(float, datos['High']))
        low = list(map(float, datos['Low']))
        openv = list(map(float, datos['Open']))

        # Volatilidad diaria (High - Low) / Open
        volatilidad_diaria = [(high[i] - low[i]) / openv[i] for i in range(len(openv))]

        # Volatilidad promedio general
        promedio = sum(volatilidad_diaria) / len(volatilidad_diaria)

        # Desviación

        # - Numerador
        suma_cuadrados = sum((v - promedio) ** 2 for v in volatilidad_diaria)

        # - Dividir x dias
        sinraiz = suma_cuadrados / len(volatilidad_diaria)        
        
        # - Raiz
        desviacion = sinraiz ** 0.5
        
        # - Redondear a 4 decimales
        
        promedio = round(promedio, 4)
        desviacion = round(desviacion, 4)

        resultados.append(f"La acción {accion} tiene una volatilidad con promedio {promedio} y desviación {desviacion}.")

    # Escribir resultados en un archivo de texto
    with open(archivotexto, "w") as archivo:
        archivo.write("Estudio de volatilidad de stocks:\n")
        archivo.write("\n".join(resultados))

    print(f"Resultados guardados en {archivotexto}")

    return archivotexto

#Especifico donde se encuentran los archivos con las acciones 

carpeta = "C:/Users/karin/OneDrive/Escritorio/TP3/Acciones"

# Llamar funciones

diccionariocompleto = dic_acciones(carpeta)
graficadora(diccionariocompleto)
graficarxclave(diccionariocompleto)
volatilidad(diccionariocompleto) 