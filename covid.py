# Agustin Avila
# noviembre 2020

# TODO:Funcionalidad mínima (requisito):
# TODO:
# TODO:La aplicación debe recibir del usuario el nombre del país deseado y permitir graficar casos detectados y fallecimientos totales para ese país en función del tiempo.
# TODO:El usuario debe poder ingresar 2 países y se permite graficar para dichos países la cantidad de casos y fallecimientos en dos gráficos con labels. El usuario debe poder ingresar el intervalo de tiempo a graficar. Calcular las intersecciónes entre gráficos si las hubiera y marcarlas con un punto de algún tipo.
# TODO:El usuario debe poder ingresar n países y se permite graficar para dichos países la cantidad de casos en una escala logaritmica. El programa debe pedirle al usuario el intervalo de tiempo deseado.
# TODO:Gráfico a entregar (requisito):
# TODO:
# TODO:Gráficar sobre la misma imagen la cantidad de casos en una escala logaritmica de Argentina y todos sus países limítrofes (Chile, Bolivia, Paraguay, Brasil y Uruguay) durante los meses de invierno (21 de junio a 21 de septiembre). Debe quedar claro la curva que corresponde a cada país.
# Funcionalidad opcional: Pueden realizar todos, algunos, o ninguno de los siguientes ítems. También pueden agregar otra funcionalidad que se les ocurra a ustedes en tanto cumpla con la funcionalidad mínima.
# TODO:
# TODO:El programa debe permitir almacenar en un archivo excel los países ordenados de mayor cantidad de casos totales acumulados (al día de hoy) a menor cantidad de casos indicando en las distintas columnas el nombre del país, la cantidad de casos y los fallecimientos.
# TODO:
# TODO:Almacenar en un archivo excel los países ordenados de mayor cantidad de casos totales acumulados a menor cantidad de casos indicando en las distintas columnas el nombre del país, la cantidad de casos y los fallecimientos colocando en distintas hojas del archivo excel (distintas pestañas) la evolución de este ranking, es decir armar una hoja distinta para cada día transcurrido. Defina los días a utilizar acorde a cuanta información se disponga, podría ser una entrada del usuario.
# TODO:
# TODO:Para cada gráfico generado el usuario deberá poder ingresar un nombre de archivo y el programa genera un archivo .PNG del gráfico con el nombre indicado.
# TODO:
# TODO:Crear una aplicación de consola que se ejecute continuamente recibiendo comandos del usuario, el usuario debe indicar el modo de operación que desea y el programa le pide los datos requeridos. Luego de finalizar la tarea el programa regresa al inicio y le pide al usuario el próximo comando. Incluír un comando de ayuda para que el programa indique al usuario cómo utilizarlo. Incluír un comando de salida que provoca la finalización del programa.

# %% importa librerias y declara algunas constantes
import sys
import numpy as np              #Ni se si lo necesito pero porsi
from scipy import signal,misc   #Procesamiento de señales
import matplotlib.pyplot as plt #Para graficar
import pandas as pd             #Para cargar datos
import requests
import datetime

# try:
    # from ngram import NGram
# except ImportError:
    #raise ImportError('No se encuentra el paquete NGram, si lo instala podra corregir errores...("pip install ngram")')
    # from pip._internal import main as pip
    # pip(['install', '--user', 'ngram'])
    # from ngram import NGram

archivo=[]
opciones=[
    {"column":"paises",
    "texto":"Ver lista de paises"
    },
    {"column":"new_cases",
    "texto":"Casos nuevos por dia"
    },
    {"column":"new_deaths",
    "texto":"Muertes nuevas por dia"
    },
    {"column":"total_cases",
    "texto":"Casos totales"
    },
    {"column":"total_deaths",
    "texto":"Muertes totales"
    },
    {"column":"salir",
    "texto":"Finalizar programa"
    }]

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
    url='https://covid.ourworldindata.org/data/ecdc/full_data.csv'
    #url=input("Ingrese la url del archivo:")
    wget(url)
    nombre=url[url.rfind('/') + 1::]
    archivo=pd.read_csv(nombre,parse_dates=["date"]) #Cargado archivo en dataframe
    return archivo

def interseccion(ind,data1,data2):
    m1=np.linalg.det(np.array([[0,data1[ind]],[1, data1[ind+1]]]))
    m2=-1
    m3=np.linalg.det(np.array([[0,data2[ind]],[1, data2[ind+1]]]))
    m4=-1
    m5=np.linalg.det(np.array([[data1[ind], 1],[data1[ind+1], 1]]))
    m6=np.linalg.det(np.array([[data2[ind], 1],[data2[ind+1], 1]]))
    denom=np.linalg.det(np.array([[m2,m5],[m4,m6]]))
    x=np.linalg.det(np.array([[m1,m2],[m3,m4]]))/denom
    y=np.linalg.det(np.array([[m1,m5],[m3,m6]]))/denom
    x=((data1["Date"][ind+1]-data1["Date"][ind])*x)+data1["Date"][ind]
    return x,y

def chequear(pais):
    pais=pais.capitalize()
    if pais in paises:
        print("El pais seleccionado es",pais)
        return pais
    # elif paisesNgram.find(pais,.2):
        # pais=paisesNgram.find(pais,.2)
        # print("El pais seleccionado es",pais)
        # return pais
    else:
        #print("No encontrado ")
        return None

def getdate():
    while True:
        date_entry = input('ingrese fecha en el formato dd-mm-aaaa')
        try:
            dia,mes,anio = map(int, date_entry.split('-'))
            date1 = datetime.date(anio,mes,dia)
            break
        except ValueError:
            print("fecha incorrecta")
    return date1

def grafica(dato,fechamin,fechamax,extra):
    fig= plt.figure(figsize=(12,4))
    if extra=="log":
        plt.yscale("log")
    for pais in paisesElegidos:
        data=df[df["location"]==pais]
        if extra=="uno":
            plt.plot(data["date"],data["total_cases"],label="Casos totales")
            plt.plot(data['date'],data["total_deaths"],label="Muertes totales")
            plt.title("Casos y muertes totales en",pais)
        else:
            plt.plot(data["date"],data[dato.get("column")],label=pais)
            plt.title(dato.get("texto"))
            
    plt.xlim(fechamin,fechamax)
    plt.xticks(rotation=60)
    plt.legend()
    #plt.title(opciones[nOpcion]["texto"])
    plt.grid()
    plt.show()
    return fig

def ingresarfechas():
    print("ingrese la fecha inicial para graficar")
    fechamin=getdate()
    print("Ingrese la fecha final para graficar")
    fechamax=getdate()
    return fechamin,fechamax

# %% Codigo principal:
#opcion="local"  #para testing, ya trabajo con el archivo local
print("Opciones:")
for i in range(len(opciones)):
    print(i,":",opciones[i]["texto"])

# while True:
#     try:
#         nOpcion=int(input("Ingrese la opcion deseada: "))
#     except ValueError:
#         print("Debe ingresar un numero")
#     else:
#         if nOpcion >= len(opciones) or nOpcion < 0:        
#             print("El valor debe ser ser una de las opciones")
#         else:
#             print("")
#             print("Ha ingresado la opcion",nOpcion)
#             break
    #Aca deberia ir el codigo recursivo

archivo=descargar()
paises=archivo['location'].unique()
# if nOpcion == 0:
#     print("")
#     print("Imprimiendo lista de paises:")
#     for pais in paises:
#         print(pais)

# paisesNgram=NGram()
# for pais in paises:
    # print(pais)
    # paisesNgram.add(pais)

# %% graficando paises limitrofes
paisesElegidos=["Argentina","Chile","Brazil","Bolivia","Uruguay","Paraguay"]
fechamin=datetime.date(2020,6,21)
fechamax=datetime.date(2020,9,21)
df=archivo.loc[archivo['location'].isin(paisesElegidos)]    #Arreglo con los datos requeridos, no es necesario igual
fig=grafica(opciones[3],fechamin,fechamax,"log")
#deberia guardar esa grafica?
# %% grafica con paises ingresados por el usuario
paisesElegidos=[]
while True:
    paistemp=input('Ingrese un pais: (Escriba "No" para finalizar, "info" para ver la lista de paises)')
    if paistemp.capitalize()==("No"):
        print("Ok, continuando:")
        break
    elif paistemp.capitalize()==("Info"):
        print("")
        print("Imprimiendo lista de paises:")
        for pais in paises:
            print(pais)
    else:
        paisito=chequear(paistemp)
        if paisito:
            if paisito in paisesElegidos:
                print("El pais",paisito,"ya fue seleccionado")
            else:
                paisesElegidos.append(paisito)    

df=archivo.loc[archivo['location'].isin(paisesElegidos)]    #Arreglo con los datos requeridos, no es necesario igual

# %% switch: para ver que funcion realiza luego
npaises=len(paisesElegidos)
if npaises==0:
    print("No se seleccionaron paises, terminando.")
elif npaises==1:
    print("Se selecciono un pais nomas")
    temp=input('Desea ingresar un rango temporal? Si no lo ingresa, se mostrara los datos desde el inicio hasta el dia de hoy. Ingrese Si/No')
    while True:
        if temp.capitalize()=="Si":
            fechamin,fechamax=ingresarfechas()
            break
        elif temp.capitalize()=="No":
            fechamin=df["date"].min()
            fechamax=df["date"].max()
            break
        else:
            temp=input("Ingreso una opcion incorrecta: Desea ingresar una fecha? Si/No:")
    grafica(opciones[3]["column"],fechamin,fechamax,"uno")
elif npaises==2:
    print("Se seleccionaron dos paises")
    temp=input('Desea ingresar un rango temporal? Si no lo ingresa, se mostrara los datos desde el inicio hasta el dia de hoy. Ingrese Si/No')
    while True:
        if temp.capitalize()=="Si":
            fechamin,fechamax=ingresarfechas()
            break
        elif temp.capitalize()=="No":
            fechamin=df["date"].min()
            fechamax=df["date"].max()
            break
        else:
            temp=input("Ingreso una opcion incorrecta: Desea ingresar una fecha? Si/No:")
    grafica(opciones[3],fechamin,fechamax,"")
    grafica(opciones[4],fechamin,fechamax,"")
else:
    print("Ha selecionado",npaises,"paises.")
    fechamin,fechamax=ingresarfechas()
    grafica(opciones[3],fechamin,fechamax,"log")


# %%

