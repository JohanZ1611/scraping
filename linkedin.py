# import

from selenium import webdriver
import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import time

#SOLO ES CAMBIAR LA URL POR LA QUE DESEES O QUE TE GENERE GOOGLE TRAS A VER REALIZADO UNA BUSQUEDA DE EMPLEO EN LINKEDIN Y EL TE HACE EL PROCESO DE EXTRACION DE OFERTAS


url1 = 'https://www.linkedin.com/jobs/search/?currentJobId=3716433278&distance=25&f_C=22306525%2C28119221&f_E=2%2C3&f_TPR=r604800&f_WT=2%2C1&geoId=100876405&keywords=desarrollador%20web&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true'

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
salarios = []
ubicaciones = []

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
        detalle_oferta = driver.find_element(By.CLASS_NAME, 'show-more-less-html__markup')
        
        # Extrae el texto del elemento 'detalle_oferta'
        detalle = detalle_oferta.text.strip()
        
        # Encuentra elementos que contienen 'Salary' y 'Location'
        elements = driver.find_elements(By.XPATH, "//p[contains(text(), 'Salary:') or contains(text(), 'Location:')]")
        
        salario = 'No disponible'
        ubicacion = 'No disponible'
        
        for element in elements:
            text = element.text.strip()
            if text.startswith('Salary:'):
                salario = text[len('Salary:'):].strip()
            elif text.startswith('Location:'):
                ubicacion = text[len('Location:'):].strip()
        
        # Verifica que el texto de detalle no sea nulo o vacío antes de agregarlo a la lista
        if detalle:
            detalles.append(detalle)
        else:
            detalles.append('No disponible')
        
        # Agrega los valores de salario y ubicación a las listas correspondientes
        salarios.append(salario)
        ubicaciones.append(ubicacion)
        
    except Exception as e:
        print(f'Error al extraer detalle: {str(e)}')
    
    time.sleep(8)
    
    # Cierra el controlador actual (pestaña)
    driver.quit()

print(detalles)

# # genero el archio csv

empleo_final = pd.DataFrame(nombre_empleos,columns=['Nombre del Empleo'])
compania_final = pd.DataFrame(nombre_compania,columns=[' Compañia'])
detalles_final = pd.DataFrame(detalles,columns=['Detalle de la Oferta'])
salario_final = pd.DataFrame(salarios,columns=['Salario'])
ubicacion_final = pd.DataFrame(ubicaciones,columns=['Ubicacion'])

Archivo = pd.concat([empleo_final,compania_final, detalles_final,salario_final,ubicacion_final], axis=1)

Archivo.to_csv('empleos.csv', index=False)


# Cerrar el navegador
driver.quit()
