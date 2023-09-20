# import

from selenium import webdriver
import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import time

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

# Imprimir la lista de enlaces
print(linklist)

# Extraer el detalle de cada oferta 

# Lista para almacenar los detalles y los roles
detalles = []
roles = []

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
        # Encuentra el elemento que contiene las etiquetas 'p'
        detalle_oferta = driver.find_element(By.CLASS_NAME, 'show-more-less-html__markup')
        
        # Encuentra todas las etiquetas 'p' dentro del elemento
        p_elements = detalle_oferta.find_elements(By.TAG_NAME, 'p')
        
        if len(p_elements) >= 2:
            detalle = p_elements[0].text.strip()  # Elimina espacios en blanco al inicio y al final
            rol = p_elements[1].text.strip()
            
            # Verifica que el texto no sea nulo o vacío antes de agregarlo a las listas
            if detalle and rol:
                detalles.append(detalle)
                roles.append(rol)
            else:
                detalles.append('No disponible')
                roles.append('No disponible')
        else:
            detalles.append('No disponible')
            roles.append('No disponible')
        
    except Exception as e:
        print(f'Error al extraer detalle o rol: {str(e)}')


    time.sleep(5)    
    
    # Cierra el controlador actual (pestaña)
    driver.quit()

# genero el archio csv

empleo_final = pd.DataFrame(nombre_empleos,columns=['Nombre del Empleo'])
compania_final = pd.DataFrame(nombre_compania,columns=[' Compañia'])
linklist_final = pd.DataFrame(linklist,columns=['Link de la Oferta'])
detalles_final = pd.DataFrame(detalles,columns=['Detalle de la Oferta'])
roles_final = pd.DataFrame(roles,columns=['Rol de la Oferta'])

Archivo = pd.concat([empleo_final,compania_final, linklist_final, detalles_final, roles_final], axis=1)

Archivo.to_csv('empleos.csv', index=False)


# Cerrar el navegador
driver.quit()
