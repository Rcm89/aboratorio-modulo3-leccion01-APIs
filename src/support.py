import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')
from geopy.geocoders import Nominatim
import requests
# Uso de API's
# -----------------------------------------------------------------------
import requests

# Para incluir una barra de proceso en for loops
# -----------------------------------------------------------------------
from tqdm import tqdm


# Para introducir tiempo entre las llamadas
# -----------------------------------------------------------------------
from time import sleep


# Para trabajar con archivos dotenv y los tokens
# -----------------------------------------------------------------------

import os
import dotenv
dotenv.load_dotenv()

from geopy.geocoders import Nominatim
from tqdm import tqdm
import pandas as pd
from time import sleep

def obtener_df_coordenadas(lista_municipios):
    """
    Obtiene las coordenadas geográficas (latitud y longitud) de una lista de municipios y las devuelve en un DataFrame.

    Parámetros:
    lista_municipios (list): Lista de nombres de municipios.

    Retorna:
    pandas.DataFrame: DataFrame con las columnas 'Municipio', 'Latitud' y 'Longitud'.
    """
    # Inicializar el geolocalizador Nominatim con un user_agent personalizado
    geolocator = Nominatim(user_agent="SetMagic Productions")  # Usamos Nominatim como geolocalizador
    resultados = []  # Lista para almacenar los resultados

    # Iteramos sobre la lista de municipios con una barra de progreso
    for municipio in tqdm(lista_municipios):
        try:
            # Intentamos obtener la ubicación geográfica del municipio
            location = geolocator.geocode(municipio)
            if location:
                # Si se encuentra la ubicación, añadimos los datos a la lista de resultados
                resultados.append((municipio, location.latitude, location.longitude))
            else:
                # Si no se encuentra la ubicación, añadimos None para latitud y longitud
                resultados.append((municipio, None, None))

            # Pausa de 1 segundo para respetar los términos de uso del servicio y evitar sobrecargas
            sleep(1)

        except Exception as e:
            # Capturamos cualquier error y lo mostramos por pantalla
            print(f"Error al obtener las coordenadas para {municipio}: {e}")
            # Añadimos el municipio con coordenadas None en caso de error
            resultados.append((municipio, None, None))

    # Crear un DataFrame con los resultados obtenidos
    df_resultados = pd.DataFrame(resultados, columns=["Municipio", "Latitud", "Longitud"])

    return df_resultados

def buscar_lugares(municipio, latitud, longitud, categoria, radio=5000):
    """
    Busca lugares de interés en una ubicación específica utilizando la API de Foursquare.

    Parámetros:
    municipio (str): Nombre del municipio.
    latitud (float): Latitud de la ubicación.
    longitud (float): Longitud de la ubicación.
    categoria (str): Código de categoría para los lugares a buscar.
    radio (int, opcional): Radio de búsqueda en metros. Por defecto es 5000.

    Retorna:
    list: Lista de lugares encontrados si la solicitud es exitosa.
    None: Si la solicitud falla.
    """
    # URL de la API de Foursquare para buscar lugares
    url = f"https://api.foursquare.com/v3/places/search"
    
    # Encabezados de la solicitud, incluyendo la clave de autorización
    headers = {
        "accept": "application/json",
        "Authorization": os.getenv("token")  # La clave de la API debe ser proporcionada
    }
    
    # Parámetros de la solicitud, incluyendo coordenadas, radio y categoría
    params = {
        "ll": f"{latitud},{longitud}",  # Coordenadas de la ubicación
        "radius": radio,                 # Radio de búsqueda en metros
        "categories": categoria,         # Categoría de lugares a buscar
        "limit": 10                      # Número máximo de resultados a devolver
    }
    
    try:
        # Realizamos la solicitud GET a la API con los encabezados y parámetros especificados
        response = requests.request("GET", url, params=params, headers=headers)
        
        # Verificamos si la solicitud fue exitosa (código 200)
        if response.status_code == 200:
            # Retornamos la lista de resultados obtenidos
            return response.json()["results"]
        else:
            # Si hubo un error en la solicitud, podemos imprimir el código de estado
            print(f"Error en la solicitud: {response.status_code}")
            return None
    except Exception as e:
        # Capturamos cualquier excepción que pueda ocurrir durante la solicitud
        print(f"Error al buscar lugares para {municipio}: {e}")
        return None
    
    

def buscar_lugares(municipio, latitud, longitud, categoria, radio=5000):
    """
    Busca lugares de interés en una ubicación específica utilizando la API de Foursquare.

    Parámetros:
    municipio (str): Nombre del municipio.
    latitud (float): Latitud de la ubicación.
    longitud (float): Longitud de la ubicación.
    categoria (str): Código de categoría para los lugares a buscar.
    radio (int, opcional): Radio de búsqueda en metros. Por defecto es 5000.

    Retorna:
    list: Lista de lugares encontrados si la solicitud es exitosa.
    None: Si la solicitud falla.
    """
    # URL de la API de Foursquare para buscar lugares
    url = f"https://api.foursquare.com/v3/places/search"
    
    # Encabezados de la solicitud, incluyendo la clave de autorización
    headers = {
        "accept": "application/json",
        "Authorization": os.getenv("token")  # La clave de la API debe ser proporcionada
    }
    
    # Parámetros de la solicitud, incluyendo coordenadas, radio y categoría
    params = {
        "ll": f"{latitud},{longitud}",  # Coordenadas de la ubicación
        "radius": radio,                 # Radio de búsqueda en metros
        "categories": categoria,         # Categoría de lugares a buscar
        "limit": 10                      # Número máximo de resultados a devolver
    }
    
    try:
        # Realizamos la solicitud GET a la API con los encabezados y parámetros especificados
        response = requests.request("GET", url, params=params, headers=headers)
        
        # Verificamos si la solicitud fue exitosa (código 200)
        if response.status_code == 200:
            # Retornamos la lista de resultados obtenidos
            return response.json()["results"]
        else:
            # Si hubo un error en la solicitud, podemos imprimir el código de estado
            print(f"Error en la solicitud: {response.status_code}")
            return None
    except Exception as e:
        # Capturamos cualquier excepción que pueda ocurrir durante la solicitud
        print(f"Error al buscar lugares para {municipio}: {e}")
        return None
    

def obtener_servicios_municipios(df_municipios, categorias):
    """
    Obtiene servicios de interés en una lista de municipios utilizando la API de Foursquare.

    Parámetros:
    df_municipios (pandas.DataFrame): DataFrame con columnas 'Municipio', 'Latitud' y 'Longitud'.
    categorias (list): Lista de códigos de categorías a buscar.
    
    Retorna:
    pandas.DataFrame: DataFrame con información de los servicios encontrados.
    """
    servicios = []  # Lista para almacenar los servicios encontrados

    # Iteramos sobre cada municipio en el DataFrame con una barra de progreso
    for i in tqdm(range(len(df_municipios))):
        municipio = df_municipios.iloc[i]['Municipio']
        latitud = df_municipios.iloc[i]['Latitud']
        longitud = df_municipios.iloc[i]['Longitud']
       
        # Iteramos sobre cada categoría de interés
        for categoria in categorias:
            # Llamamos a la función buscar_lugares para obtener lugares de la categoría en el municipio
            lugares = buscar_lugares(municipio, latitud, longitud, categoria)
            if lugares:
                # Si se encontraron lugares, extraemos la información relevante
                for lugar in lugares:
                    servicios.append({
                        'municipio': municipio,
                        'nombre_lugar': lugar['name'],
                        'categoria': lugar['categories'][0]['name'] if lugar.get('categories') else 'N/A',
                        'direccion': lugar['location'].get('address', 'N/A'),
                        'latitud': lugar['geocodes']['main']['latitude'],
                        'longitud': lugar['geocodes']['main']['longitude']
                    })
    # Convertimos la lista de servicios en un DataFrame y lo retornamos
    return pd.DataFrame(servicios)
