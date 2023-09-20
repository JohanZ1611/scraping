# import

from selenium import webdriver
import time
import pandas as pd
import os

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time

url1 = 'https://www.linkedin.com/jobs/search/?currentJobId=3704889841&keywords=desarrollador%20web'

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

# Esperar 20 segundos antes de cerrar el navegador (puedes ajustar este tiempo según tus necesidades)
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

#Recorro mediante scroll y ejecuto la accoin de ver mas para captrar la mayor cantidad posible de datos

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

#Extraigo los datos de las ofertas y las almaceno en una lista

nombre_compania = []

try:
    companias = driver.find_elements(By.CLASS_NAME, 'base-search-card__subtitle')
    for compania in companias:
        nombre_compania.append(compania.text)
except IndexError:
    print('Fallo extraccion nombre de compañias')

nombre_empleos = []

try:
    empleos = driver.find_elements(By.CLASS_NAME, 'base-search-card__title')
    for empleo in empleos:
        nombre_empleos.append(empleo.text)
except IndexError:
    print('Fallo extraccion nombre de empleos')

# Extraemos el enlace de la oferta de empleo
# linklist = []

# link_oferta = driver.find_element(By.CLASS_NAME, 'base-card__full-link').get_attribute('href')

# for l in link_oferta:
#     linklist.append(l)

# print(linklist)


# genero el archio csv

compania_final = pd.DataFrame(nombre_compania,columns=[' Compañia'])
empleo_final = pd.DataFrame(nombre_empleos,columns=['Nombre del Empleo'])

Archivo = empleo_final.join(compania_final)

Archivo.to_csv('empleos.csv', index=False)


# Cerrar el navegador
driver.quit()
