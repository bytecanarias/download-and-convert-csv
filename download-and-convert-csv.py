import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

# URL de la página de inicio de sesión
login_url = 'https://ejemplo.es/login' # url según web ejemplo.es/original.asp o ejemplo.es/login

# Crear una sesión
session = requests.Session()

# Obtener el contenido de la página de inicio de sesión para encontrar el formulario
response = session.get(login_url)
soup = BeautifulSoup(response.content, 'html.parser')

# Aquí debes inspeccionar el formulario de inicio de sesión para obtener los nombres de los campos de entrada
# Por ejemplo, supongamos que los campos son 'name=username' y 'name=password'

login_payload = {
    'username': 'your_user',  # Reemplaza con tu nombre de usuario revisar código HTML para ver nombre del campo
    'password': 'your_pass',  # Reemplaza con tu contraseña código HTML para ver nombre del campo
    # Añade cualquier otro campo oculto que sea necesario, como tokens CSRF
}

# La URL a la que se envían los datos del formulario de inicio de sesión
post_login_url = 'https://ejemplo.es/original.asp?accessdenied=%2Foriginal2%2Easp'  # Esto es un ejemplo, debes verificar la URL correcta

# Enviar el formulario de inicio de sesión
login_response = session.post(post_login_url, data=login_payload)

# Verificar si el inicio de sesión fue exitoso
# if login_response.url == 'https://ejemplo.es/original2.asp':  # La URL de redirección después del inicio de sesión exitoso
#    print('Inicio de sesión exitoso!')
#else:
#    print('Fallo en el inicio de sesión')

# Url de la lista de precios
excel_url = 'https://ejemplo.es/EXCELCOMPLETO.asp'

# Hacer una solicitud GET a la URL de descarga
excel_response = session.get(excel_url)

# Guardar el contendio del archivo
output_file = 'tarifas.html' # Se puede poner el nombre y extensión que se quiera

# Verificar si la solicitud fue exitosa
if excel_response.status_code == 200:
    with open(output_file, 'wb') as file:
        file.write(excel_response.content)
#    print(f'Archivo guardado como {output_file}')
#else:
#    print('Error al descargar el archivo')

# CONVERTIR EL ARCHIVO XLS o HTML A CSV

# Ruta al archivo XLS o HTML
html_path = 'tarifas.html'

# Lista vacía para almacenar los datos
data = []

# Leer el archivo HTML
with open(html_path, encoding='iso-8859-1') as file: # iso-8859-1 en minúsculas para los malditos acentos
    soup = BeautifulSoup(file, 'html.parser')


# Obtener los encabezados de la tabla
list_header = []
header = soup.find_all("table")[0].find("tr")
for items in header.find_all("td"):
    list_header.append(items.get_text())

# Obtener los datos de la tabla
HTML_data = soup.find_all("table")[0].find_all("tr")[1:]
for element in HTML_data:
    sub_data = []
    for sub_element in element.find_all("td"):
        sub_data.append(sub_element.get_text().strip())
    data.append(sub_data)

# Crear un DataFrame de Pandas
dataFrame = pd.DataFrame(data=data, columns=list_header)

# Guardar el DataFrame como archivo CSV
output_csv_path='tarifas.csv'
dataFrame.to_csv(output_csv_path, index=False, sep=';', quoting=csv.QUOTE_MINIMAL)

# print(f'Archivo CSV generado: {output_csv_path}')
