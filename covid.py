# Agustin Avila
# noviembre 2020

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
import requests                 #Para descargar el archivo
import datetime                 #Para manejar fechas

#En un principio use Ngram para corregir errores de tipeo en paises
#Pero por si acaso lo comente.

# try:
    # from ngram import NGram
# except ImportError:
    #raise ImportError('No se encuentra el paquete NGram, si lo instala podra corregir errores...("pip install ngram")')
    # from pip._internal import main as pip
    # pip(['install', '--user', 'ngram'])
    # from ngram import NGram

archivo=[]
#opciones serviria para graficar por ejemplo, casos por dia o opciones fuera de lo basico
opciones=[      #Para sanitizar entradas y hacer graficas customizadas
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

def wget(url):      #Descarga archivo
    try:
        r = requests.get(url, allow_redirects=True)
        r.raise_for_status()
        with open(url[url.rfind('/') + 1::], 'wb') as f:
            f.write(r.content)
    except requests.RequestException:
        print("Error en la descarga")

def descargar():    #Realmente descarga archivo y lo guarda
    url='https://covid.ourworldindata.org/data/ecdc/full_data.csv'
    #url=input("Ingrese la url del archivo:")
    wget(url)
    nombre=url[url.rfind('/') + 1::]
    archivo=pd.read_csv(nombre,parse_dates=["date"]) #Cargado archivo en dataframe
    return archivo

def interseccion(dato11,dato12,dato21,dato22,dia):  #Grafica los puntos de interseccion
    #Esta funcion determina la interseccion utilizando un metodo con determinantes de matrices
    #No sabria explicarlo pero funciona
    #dato11 y dato12 determinan una recta, dato21 y dato22 determinan otra
    m1=np.linalg.det(np.array([[0,dato11],[1, dato12]]))
    m2=-1
    m3=np.linalg.det(np.array([[0,dato21],[1, dato22]]))
    m4=-1
    m5=np.linalg.det(np.array([[dato11, 1],[dato12, 1]]))
    m6=np.linalg.det(np.array([[dato21, 1],[dato22, 1]]))
    denom=np.linalg.det(np.array([[m2,m5],[m4,m6]]))
    x=np.linalg.det(np.array([[m1,m2],[m3,m4]]))/denom
    y=np.linalg.det(np.array([[m1,m5],[m3,m6]]))/denom
    x=dia+datetime.timedelta(hours=int(x*24))   #se devuelve el x en formato fecha a partir del dia inicial
    return x,y

def chequear(pais): #Analiza si el pais ingresado es parte de los paises disponibles
    pais=pais.capitalize()
    if pais in paises:
        print("El pais seleccionado es",pais)
        return pais
#Usando ngram, corregia errores de tipeo
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

def getdate():  #Devuelve fechamin y fechamax
    while True:
        date_entry = input('ingrese fecha en el formato dd-mm-aaaa')
        try:
            dia,mes,anio = map(int, date_entry.split('-'))
            date1 = datetime.datetime(anio,mes,dia)
            break
        except ValueError:
            print("fecha incorrecta, intente nuevamente")
    return date1

def grafica(dato,fechamin,fechamax,extra):
    fig= plt.figure(figsize=(12,4)) #se genera la grafica
    if extra=="log":                #Se cambia la escala a logaritmica si se llama con ese argumento
        plt.yscale("log")
    for pais in paisesElegidos:     #grafica la curva para cada pais
        data=df[df["location"]==pais]
        if extra=="uno":    #grafico a realizar cuando es un solo pais
            plt.plot(data["date"],data["total_cases"],label="Casos totales")
            plt.plot(data['date'],data["total_deaths"],label="Muertes totales")
            plt.title("Casos y muertes totales en",pais)
        else:
            plt.plot(data["date"],data[dato.get("column")],label=pais)
            plt.title(dato.get("texto"))
    if extra=="dos":        #para el caso de dos paises, hay que buscar los puntos de interseccion
        rango=pd.date_range(start=fechamin,end=fechamax)    #genera un rango de fechas para analizar
        for dia in rango:       #para cada fecha, analiza si tiene los valores necesarios:
            try:                #existe el caso de que no hayan datos para una fecha dada
                #para cada pais, se buscan la cantidad de casos del dia y del dia siguiente:
                dato11=int(df[(df["date"]==dia)& (df["location"]==paisesElegidos[0])][dato.get("column")])  
                dato21=int(df[(df["date"]==dia)& (df["location"]==paisesElegidos[1])][dato.get("column")])     
                dato12=int(df[(df["date"]==dia+datetime.timedelta(days=1))& (df["location"]==paisesElegidos[0])][dato.get("column")])     
                dato22=int(df[(df["date"]==dia+datetime.timedelta(days=1))& (df["location"]==paisesElegidos[1])][dato.get("column")])     
                if (dato11-dato21)*(dato12-dato22)<=0:                  #analiza si hay un cruce entre ambos datos
                    x,y=interseccion(dato11,dato12,dato21,dato22,dia)   #si hay, obtiene las coord del punto
                    plt.plot(x,y,'bo')                                  #y finalmente lo grafica
            except:
                pass    #en caso de que no se encuentre alguno de los datos, no hace nada
    plt.xlim(fechamin,fechamax) #limita la grafica entre fechamin y fechamax
    plt.xticks(rotation=60)
    plt.legend()                #Muestra los nombres de los paises
    plt.grid()                  #Agrega grilla
    plt.show()                  #La grafica
    return fig

def ingresarfechas():
    print("ingrese la fecha inicial para graficar")
    fechamin=getdate()
    print("Ingrese la fecha final para graficar")
    fechamax=getdate()
    return fechamin,fechamax

# %% Codigo principal:
archivo=descargar()                     #guarda el archivo y genera el datafram
paises=archivo['location'].unique()     #genera una lista de paises posibles

# paisesNgram=NGram()
# for pais in paises:
    # print(pais)
    # paisesNgram.add(pais)

# %% graficando paises limitrofes:
paisesElegidos=["Argentina","Chile","Brazil","Bolivia","Uruguay","Paraguay"]
fechamin=datetime.datetime(2020,6,21)   #fecha de inicio del invierno
fechamax=datetime.datetime(2020,9,21)   #fecha de fin del invierno
df=archivo.loc[archivo['location'].isin(paisesElegidos)]    #Arreglo con los datos requeridos, no es necesario pero es mas facil que trabajar con el archivo completo
print("Graficando casos de Argentina y sus paises limítrofes:")
fig=grafica(opciones[3],fechamin,fechamax,"log")  
# %% grafica con paises ingresados por el usuario
paisesElegidos=[]   #vacia la lista de paises y le pide al usuario que ingrese los paises nuevos:
print("Si no ingresa ningun pais, el programa termina. Si ingresa un pais, se graficará la cantidad de casos y muertes totales.")
print("Si ingresa dos paises, se graficarán casos y muertes totales, marcando intersecciones si en algun momento los datos se cruzan")
print("Si ingresa mas de dos paises, se graficara casos y muertes totales, utilizando una escala logaritmica")
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
        paisito=chequear(paistemp)              #revisa si el texto ingresado corresponde a un pais
        if paisito:                             #si no corresponde, paisito es none
            if paisito in paisesElegidos:       #chequea redundancia de datos
                print("El pais",paisito,"ya fue seleccionado")
            else:
                paisesElegidos.append(paisito)  #si no estaba en la lista, lo agrega

df=archivo.loc[archivo['location'].isin(paisesElegidos)]    #Arreglo con los datos requeridos, no es necesario pero agiliza el programa

# %% switch: para ver que funcion realiza luego
npaises=len(paisesElegidos) #segun cuantos paises hay es lo que hace:
if npaises==0:
    print("No se seleccionaron paises, terminando.")
elif npaises==1:
    print("Se selecciono un solo pais")
    temp=input('Desea ingresar un rango temporal? Si no lo ingresa, se mostrara los datos desde el inicio hasta el dia de hoy. Ingrese Si/No')
    while True:
        if temp.capitalize()=="Si":     #permite ingresar fechas
            fechamin,fechamax=ingresarfechas()
            break
        elif temp.capitalize()=="No":   #Toma como minimo la primer fecha de los paises seleccionados
            fechamin=df["date"].min()   
            fechamax=df["date"].max()   #y como final el dia de hoy
            break
        else:
            temp=input("Ingreso una opcion incorrecta: Desea ingresar una fecha? Si/No:")
    grafica(opciones[3],fechamin,fechamax,"uno")
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
    grafica(opciones[3],fechamin,fechamax,"dos")    #grafica casos totales
    grafica(opciones[4],fechamin,fechamax,"dos")    #grafica muertes totales
else:
    print("Ha selecionado",npaises,"paises.")
    fechamin,fechamax=ingresarfechas()
    grafica(opciones[3],fechamin,fechamax,"log")    #grafica solo casos totales en escala logaritmica
