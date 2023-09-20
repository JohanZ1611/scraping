# import

from selenium import webdriver
import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import time

# SOLO ES CAMBIAR LA URL POR LA QUE DESEES O QUE TE GENERE GOOGLE TRAS A VER REALIZADO UNA BUSQUEDA DE EMPLEO EN LINKEDIN Y EL TE HACE EL PROCESO DE EXTRACION DE OFERTAS


url1 = 'https://www.linkedin.com/jobs/search/?currentJobId=3712610052&distance=25&f_C=91650798%2C28119221%2C18802834&f_E=2&f_WT=2&geoId=100876405&keywords=desarrollador%20web&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true'

# Ruta al ejecutable de Microsoft Edge WebDriver
edge_driver_path = r'C:\\Users\\Default\\Desktop\\msedgedriver.exe'

# Configurar las opciones de Microsoft Edge
edge_options = Options()
# Puedes agregar más opciones si es necesario
edge_options.add_argument('--disable-extensions')

# Configurar el servicio de Microsoft Edge con la ruta al ejecutable de Microsoft Edge WebDriver
service = Service(executable_path=edge_driver_path)

# Inicializar el controlador de Microsoft Edge con las opciones y el servicio
driver = webdriver.Edge(service=service, options=edge_options)

driver.get(url1)

# Esperar 10 segundos antes de cerrar el navegador (puedes ajustar este tiempo según tus necesidades)
time.sleep(10)

# Buscar elementos por clase
elements = driver.find_elements(
    By.CLASS_NAME, 'results-context-header__job-count')

# Verificar si se encontraron elementos
if elements:
    # Imprimir el texto del primer elemento encontrado
    print(elements[0].text)
else:
    print("No se encontraron elementos con la clase especificada")

empleos_disponibles = int(pd.to_numeric(elements[0].text))

# Recorro mediante scroll y ejecuto la accoin de ver mas para captrar la mayor cantidad posible de datos

contador = 2

while contador <= 20:
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    contador = contador + 1

    try:
        seguir = driver.find_element(
            By.XPATH, '//button[@aria-label="Ver más empleos"]')
        driver.execute_script("arguments[0].click();", seguir)
        time.sleep(3)
    except:
        pass
        time.sleep(4)

# Extraigo los datos de las ofertas y las almaceno en una lista

nombre_compania = []
nombre_empleos = []
nombre_localizaciones = []
tiempo_publicado = []

try:
    companias = driver.find_elements(
        By.CLASS_NAME, 'base-search-card__subtitle')
    for compania in companias:
        nombre_compania.append(compania.text)

    empleos = driver.find_elements(By.CLASS_NAME, 'base-search-card__title')
    for empleo in empleos:
        nombre_empleos.append(empleo.text)

    localizacion = driver.find_elements(By.CLASS_NAME, 'job-search-card__location')
    for loc in localizacion:
        nombre_localizaciones.append(loc.text)

    tiempo = driver.find_elements(By.CLASS_NAME, 'job-search-card__listdate')
    for tim in tiempo:
        tiempo_publicado.append(tim.text)
except IndexError:
    print('Fallo extraccion nombre de compañias')

# Extraer los enlaces de las ofertas de empleo
link_ofertas = driver.find_elements(By.CLASS_NAME, 'base-card__full-link')

# Crear una lista para almacenar los enlaces
linklist = []

# Iterar sobre los elementos y obtener los enlaces
for link_oferta in link_ofertas:
    link = link_oferta.get_attribute('href')
    linklist.append(link)


# Extraer el detalle de cada oferta

# Lista para almacenar los detalles y los roles
detalles = []

# Itera sobre los enlaces
for link in linklist:
    # Inicializa un nuevo controlador de Microsoft Edge para cada enlace
    edge_driver_path = r'C:\\Users\\Default\\Desktop\\msedgedriver.exe'

    # Configurar las opciones de Microsoft Edge
    edge_options = Options()
    # Puedes agregar más opciones si es necesario
    edge_options.add_argument('--disable-extensions')

    # Configurar el servicio de Microsoft Edge con la ruta al ejecutable de Microsoft Edge WebDriver
    service = Service(executable_path=edge_driver_path)

    # Inicializar el controlador de Microsoft Edge con las opciones y el servicio
    driver = webdriver.Edge(service=service, options=edge_options)

    # Abre una nueva ventana o pestaña y navega a la URL
    driver.get(link)

    try:
        # Encuentra el elemento que contiene el detalle
        detalle_oferta = driver.find_element(
            By.CLASS_NAME, 'show-more-less-html__markup')

        # Extrae el texto del elemento 'detalle_oferta'
        detalle = detalle_oferta.text.strip()

        # Dividir el detalle en párrafos y seleccionar el primer párrafo
        parrafos = detalle.split('\n')
        primer_parrafo = parrafos[0]

        # Verifica que el texto no sea nulo o vacío antes de agregarlo a la lista
        if primer_parrafo:
            detalles.append(primer_parrafo)
        else:
            detalles.append('No disponible')

    except Exception as e:
        print(f'Error al extraer detalle: {str(e)}')

    time.sleep(5)

    # Cierra el controlador actual (pestaña)
    driver.quit()



# # genero el archio csv

empleo_final = pd.DataFrame(nombre_empleos,columns=['Nombre del Empleo'])
compania_final = pd.DataFrame(nombre_compania,columns=[' Compañia'])
localizacion_final = pd.DataFrame(nombre_localizaciones,columns=['Localizacion'])
tiempo_final = pd.DataFrame(tiempo_publicado,columns=['Tiempo de Publicacion'])
detalles_final = pd.DataFrame(detalles,columns=['Detalle de la Oferta'])

Archivo = pd.concat([empleo_final,compania_final, localizacion_final, tiempo_final,detalles_final], axis=1)

Archivo.to_csv('empleos.csv', index=False)


# Cerrar el navegador
driver.quit()
