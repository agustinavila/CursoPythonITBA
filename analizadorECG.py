# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'

import sys
import numpy as np              #Ni se si lo necesito pero porsi
from scipy import signal,misc   #Procesamiento de señales
import matplotlib.pyplot as plt #Para graficar
import pandas as pd             #Para cargar datos
import requests
from xlrd import XLRDError      #Maneja excepciones cuando se abre un archivo que no es de excel

archivo=[]
TMAX=2000
# %% definicion de funciones:

def wget(url):
    try:
        r = requests.get(url, allow_redirects=True)
        r.raise_for_status()
        with open(url[url.rfind('/') + 1::], 'wb') as f:
            f.write(r.content)
    except requests.RequestException:
        print("Error en la descarga")

def descargar():
    url="https://raw.githubusercontent.com/IEEESBITBA/Curso-Python/master/Clase_4_datos/electrocardiograma.xlsx"
    url=input("Ingrese la url del archivo:")
    wget(url)
    nombre=url[url.rfind('/') + 1::]
    #archivo=pd.read_excel("electrocardiograma.xlsx",index_col=0) #Cargado archivo en dataframe
    #return archivo

def incorporado(): #usar los datos incorporados
    ecg=misc.electrocardiogram()
    fs=360
    tiempo = np.arange(ecg.size) / fs
    archivo=pd.DataFrame({'señal':list(ecg),'tiempo':list(tiempo)},columns=['señal','tiempo'])
    return archivo


def local():
    while True:
        try:
            nombre=input("Ingrese el nombre del archivo:")
            archivo=pd.read_excel(nombre)
            break
        except IOError:
            print("No se encontro el archivo especificado")
        except XLRDError:
            print("El archivo ingresado no se reconoce como un archivo de excel")
    return archivo

def pulsaciones():
    puls=picos["Tiempo"][len(picos)-1]-picos["Tiempo"][0]
    puls=(len(picos)-1)*60/puls
    print(puls)

def estado_persona():
    val_sexo=["H","M"]
    while True:
        try:
            edad=int(input("Ingrese la edad del paciente: "))
        except ValueError:
            print("Debe ingresar un numero entero")
        else:
            if edad > 0:
                break
            else:
                print("El valor debe ser positivo")
    while True:
        print("Ingrese el sexo de la persona.")
        sexo=input('Ingrese "M" si es mujer o "H" si es hombre:')
        if sexo in val_sexo:
            break
        else:
            print("Ha ingresado un valor erroneo, intente nuevamente")
    #ingreso de datos

function_dict={"descargar":descargar,"incorporado":incorporado,"local":local}   #Para ver el metodo de ingreso de datos


# %% Codigo principal:
#opcion="local"  #para testing, ya trabajo con el archivo local
while True:
    print("Elija si desea descargar el archivo o usar el archivo incorporado")
    opcion=input('Ingrese "descargar" o "incorporado":')
    if opcion in function_dict:
        print("Ha elegido:",opcion)
        break
    else:
        print("Ha ingresado un valor incorrecto, por favor intente nuevamente")

archivo=function_dict[opcion]()
datos=archivo[archivo["tiempo"]<TMAX]
plt.figure(figsize=(12, 4))
plt.plot(datos["tiempo"],datos["señal"])
sig=archivo["señal"]
t=archivo["tiempo"]
ts=t.values[-1]/t.size
fs=1/ts


# %%
#intentando obtener los picos, falta resolver que se hace con eso

plt.figure(figsize=(12, 4))
plt.plot(datos["tiempo"],datos["señal"])
picos=pd.DataFrame(columns=["Tiempo","Amplitud"])
pico,prop=signal.find_peaks(datos["señal"],prominence=(1.3,None))
for i in range(0,len(pico)):
    picos.loc[i]=({'Tiempo':datos["tiempo"][pico[i]],'Amplitud':datos["señal"][pico[i]]})
print(picos)
plt.plot(picos["Tiempo"],picos["Amplitud"],'ro')

# %%
# obtencion de pulsaciones:

ppm=pulsaciones()

# %%
#analisis espectral de la señal
f,espectro=signal.welch(archivo["señal"],fs=1/ts,nperseg=1024)
plt.figure(figsize=(12, 4))
#plt.semilogy(f,espectro)
plt.magnitude_spectrum(datos["señal"],Fs=fs,scale="dB")
nombre_archivo=input("Ingrese un nombre de archivo para guardar el espectro del ECG: ")
#plt.savefig(nombre_archivo)
#guarda el archivo con el nombre dado. 
#faltaria sacar potencia en 60hz


# %%
estado_persona()
