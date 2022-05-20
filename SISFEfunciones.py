from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from pathlib import *
from selenium import webdriver
from random import randint
from time import sleep
from easygui import *
import csv
import os
import codecs

# Crea una instancia del driver y la devuelve
def generarDriver():
    rutaDriver = os.path.join(os.getcwd(),"chromedriver")
    driver = webdriver.Chrome(rutaDriver, chrome_options=Options()) 
    Options().add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/59.0.3071.115 Safari/537.36")
    return driver

# Lee los archivos, clasifica la información y mete todo en la lista que devuelve
def leerArchivos():
    demandados = []
    domicilios = []
    montos = []
    pdfs = []

    ruta = os.path.join(os.getcwd(),"Cabecera")
    demandas = codecs.open(ruta + os.sep + "RegistrosAprocesar.csv","r", encoding = 'ISO-8859-1')

    totalApremios = sum(1 for row in demandas)
    demandas.seek(0)

    contadorDemandas = 0

    while (True):
        contadorDemandas += 1
        lineaD = demandas.readline()
        ingresoDemanda = lineaD.split(',')

        if lineaD == "":
            break
        
        if (contadorDemandas == 0 or contadorDemandas//5 == 1):
            mail = ingresoDemanda[0]
            localidad = (ingresoDemanda[1]).upper()
            competencia = (ingresoDemanda[2]).upper()
            organismo = ingresoDemanda[3]
            tipoCausa = (ingresoDemanda[4]).upper()
            causa = (ingresoDemanda[5]).upper()
            actor = (ingresoDemanda[6]).upper()
            domicilio = (ingresoDemanda[7]).upper()

        demandados.append(ingresoDemanda[9]+ingresoDemanda[10])
        domicilios.append(ingresoDemanda[11])
        montos.append(ingresoDemanda[12])
        pdfs.append((ingresoDemanda[13]+","+ingresoDemanda[14]).rstrip())

    return [demandados, domicilios, montos, pdfs, mail, localidad, competencia, organismo, tipoCausa, causa, actor, domicilio]

# Loguea al profesional en el SISFE
def loguearProfesional(driver):
    driver.get('https://sisfe.justiciasantafe.gov.ar/login-matriculado')
    driver.maximize_window()
    botonIngresar = esperarCargaElemento("botonIngresar", driver)
    informacion = codecs.open("datos.csv","r", encoding='ISO-8859-1')
    count = 0
    while True:
        count += 1
        linea = informacion.readline()

        if (len(linea) == 0):
            break
        else:
            datosIngreso = linea.split(',')
            circunscripcion = datosIngreso[0]
            matricula = datosIngreso[2]
            contraseña = datosIngreso[3]

            elementoCircunscripcion = driver.find_element_by_id("circunscripcion")
            elementoCircunscripcion.send_keys(circunscripcion)
            elementoColegio = driver.find_element_by_id("colegio")
            objetoColegio = Select(elementoColegio)
            objetoColegio.select_by_visible_text("Abogados")
            textAreaMatricula = driver.find_element_by_id("matricula")
            textAreaMatricula.send_keys(matricula)
            textAreaContraseña = driver.find_element_by_id("password")
            textAreaContraseña.send_keys(contraseña)
            # input("Complete el captcha y presione enter para continuar")
            msgbox("Complete el captcha. Cuando termine, presione OK para continuar.")
            
            botonIngresar.click()

# Espera que carguen los elementos para que no se produzcan errores
def esperarCargaElemento(elemento, driver):
    if elemento=="botonIngresar":
        botonIngresar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button[@id="ingresar"]'))
            )
        return botonIngresar
    if elemento =="botonInicioMasivoDemanda":
        botonInicioMasivoDemanda = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[@id="iniciarLoteDemanda"]'))
        )
        return botonInicioMasivoDemanda
    if elemento == "botonNuevoLoteDemanda":
        botonNuevoLoteDemanda = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[@id="nuevoLoteDemanda"]'))
        )
        return botonNuevoLoteDemanda
    if elemento == "email":
        email = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//input[@id="correoElectronico"]'))
        )
        return email
    if elemento == "droplistLocalidad":
        droplistLocalidad = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//select[@id="localidad"]'))
        )
        return droplistLocalidad
    if elemento == "droplistCompetencia":
        droplistCompetencia = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//select[@id="competencia"]'))
        )
        return droplistCompetencia
    if elemento == "droplistOrganismo":
        droplistOrganismo = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//select[@id="organismo"]'))
        )
        return droplistOrganismo
    if elemento == "droplistTipoCausa":
        droplistTipoCausa = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//select[@id="tipoCausa"]'))
        )
        return droplistTipoCausa
    if elemento == "droplistCausa":
        droplistCausa = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//select[@id="causa"]'))
        )
        return droplistCausa
    if elemento == "textFieldActor":
        textFieldActor = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="actor"]'))
        )
        return textFieldActor
    if elemento == "textFieldDomicilio":
        textFieldDomicilio = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="domicilio"]'))
        )
        return textFieldDomicilio
    if elemento == "botonNuevoExpediente":
        botonNuevoExpediente = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@id='agregar']"))
        )
        return botonNuevoExpediente

# Hace click en un par de botones para llegar a la página objetivo
def navegar(driver):
    sleep(randint(7,9))

    botonInicioMasivoDemanda = esperarCargaElemento("botonInicioMasivoDemanda",driver)
    botonInicioMasivoDemanda.click()

    botonNuevoLoteDemanda = esperarCargaElemento("botonNuevoLoteDemanda",driver)
    botonNuevoLoteDemanda.click()

def verificarDatosCargados(informacion, driver):
    print("Verificando los datos cargados.")

    # textoLocalidad = driver.find_element(By.XPATH, 'select[@id="localidad"]')
    # select = driver.find_element_by_id('localidad')
    select = Select(WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//select[@id='localidad']"))))
    textoLocalidad = select.first_selected_option
    result = textoLocalidad.text
    print("El texto es: ", result)
    print("La información a cargar es: ", informacion[5])
    if (result != informacion[5]):
        print ("No coinciden. Ahora hay que recargar este campo")
        droplistLocalidad = esperarCargaElemento("droplistLocalidad",driver)
        droplistLocalidad.send_keys(informacion[5])
        verificarDatosCargados(informacion, driver)


# Carga los datos del profesional
def cargarDatosProfesional(info,driver):
    sleep(15)
    try:
        textFieldCorreo = esperarCargaElemento("email",driver)
        textFieldCorreo.send_keys(info[4])
        sleep(randint(2,3))
    except:
        print("El correo no se cargó correctamente")

    try:
        droplistLocalidad = esperarCargaElemento("droplistLocalidad",driver)
        droplistLocalidad.send_keys(info[5])
        sleep(randint(2,3))
    except:
        print("El droplist localidad no se cargó correctamente")

    try:
        droplistCompetencia = esperarCargaElemento("droplistCompetencia",driver)
        droplistCompetencia.send_keys(info[6])
        sleep(randint(2,3))
    except:
        print("El droplist competencia no se cargó correctamente")

    try:
        droplistOrganismo = esperarCargaElemento("droplistOrganismo",driver)
        droplistOrganismo.send_keys(info[7])
        sleep(randint(2,3))
    except:
        print("El droplist organismo no se cargó correctamente")

    try:
        droplistTipoCausa = esperarCargaElemento("droplistTipoCausa",driver)
        droplistTipoCausa.send_keys(info[8])
        sleep(randint(4,5))
    except:
        print("El droplist tipo de causa no se cargó correctamente")

    try:
        droplistCausa = esperarCargaElemento("droplistCausa",driver)
        droplistCausa.send_keys(info[9])
        sleep(randint(2,3))
    except:
        print("El droplist causa no se cargó correctamente")

    scroll(driver)

    textFieldActor = esperarCargaElemento("textFieldActor",driver)
    textFieldActor.send_keys(info[10])
    sleep(randint(2,3))

    textFieldDomicilio = esperarCargaElemento("textFieldDomicilio",driver)
    textFieldDomicilio.send_keys(info[11])
    sleep(randint(2,3))

# Scrollea para que se vea cómo se van completando los campos
def scroll(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

def calcularRepeticiones(info, driver):
    ruta = os.path.join(os.getcwd(),"Cabecera")
    demandas = codecs.open(ruta + os.sep + "presentarCirc1.csv","r", encoding ='ISO-8859-1')
    totalApremios = sum(1 for row in demandas)
    demandas.seek(0)
    repeticiones = totalApremios//20
    resto = totalApremios - (repeticiones*20)

    return (repeticiones, resto, totalApremios)


# Carga los datos de los demandados x20, con n repeticiones
def cargarDatosDemandados(info, driver, totalApremios, pos):
    
    #TotalApremios[0]=cantidad de Repeticiones, 1 repeticiòn 20 ciclos
    #TotalApremios[1]=resto 
    #TotalApremios[2]=totalApremios  
    cantidad=0
    sigue = True
    for (i) in range(20):
        try:
            cantidad=cantidad+1
            botonNuevoExpediente = esperarCargaElemento("botonNuevoExpediente", driver)
            botonNuevoExpediente.click()
            
            numero = i
            demandado = info[0][i+pos]
            domicilioDemandado = info[1][i+pos]
            monto = info[2][i+pos]
            pdf = info[3][i+pos]

            posicion = str(cantidad)
            vuelta = str(i)
                        
            textAreaNro = driver.find_element_by_id("nro"+vuelta)
            textAreaNro.send_keys(posicion)

            textAreaDemandado = driver.find_element_by_id("demandado"+vuelta)
            textAreaDemandado.send_keys(demandado)  

            textAreaDomicilio = driver.find_element_by_id("domicilio"+vuelta)
            textAreaDomicilio.send_keys(domicilioDemandado)

            textAreaMonto = driver.find_element_by_id("monto"+vuelta)
            textAreaMonto.send_keys(monto)

            archivoAdjuntar = os.path.join(os.getcwd(),"Demandas"+"/"+pdf)

            adjunto = driver.find_element_by_id("file"+vuelta)
            adjunto.send_keys(archivoAdjuntar)
        except:
            sigue = False
            break
    if (sigue):
        msgbox("Cree el lote. Cuando termine, presione OK para continuar")
        driver.get("https://sisfe.justiciasantafe.gov.ar/nuevo-lote-demanda")
    return(i+1)

# Valida que la cantidad de columnas sea correcta para cada registro.
# El archivo RegistrosAprocesar contendrá todos los registros que pasen esta prueba.
def validarArchivo():
    quitar_registros = []
    with open('Cabecera/presentarCirc4.csv', encoding = 'UTF-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            line_count += 1
            if (len(row) != 15):
                quitar_registros.append(row)
                agregarAerrores(row)
            else:
                agregarAprocesar(row)
        print(f'Se han procesado {line_count} líneas.')
    print(f"Existen {len(quitar_registros)} registros a quitar")
    return (line_count - len(quitar_registros))

def agregarAerrores(fila):
    with open('Cabecera/RegistrosConErrores.csv', 'a', newline='', encoding = 'ISO-8859-1') as err:
        writer = csv.writer(err, delimiter=',')
        writer.writerow(fila)

def agregarAprocesar(fila):
    with open('Cabecera/RegistrosAprocesar.csv', 'a', newline='', encoding = 'ISO-8859-1') as err:
        writer = csv.writer(err, delimiter=',')
        writer.writerow(fila)




