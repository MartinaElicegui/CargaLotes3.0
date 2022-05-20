import sys
from SISFEfunciones import *
from easygui import *

def main(): 
    cantidadApremios = validarArchivo() 
    driver = generarDriver()
    informacion = leerArchivos()
    loguearProfesional(driver)
    navegar(driver)
    totalApremios = calcularRepeticiones(informacion,driver)
    posicion = 0
    while (True):
        cargarDatosProfesional(informacion,driver)
        verificarDatosCargados(informacion, driver)
        posicion = posicion + cargarDatosDemandados(informacion,driver,totalApremios,posicion)
        if (posicion>cantidadApremios):
            msgbox("Cree el lote y presione aceptar para terminar.")
            break
if __name__ == "__main__":
    sys.exit(main())

