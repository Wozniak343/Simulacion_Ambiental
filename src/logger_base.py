"""
Configuración del sistema de logging.
Guarda todos los logs en un archivo y también los muestra en consola.
"""
import logging as log
import os

# Calculo la ruta donde se guardará el archivo de logs
log_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'capa_datos.log')

# Configuro el logger para que guarde en archivo y muestre en consola
log.basicConfig(
    level=log.DEBUG,  # Nivel mínimo de logs a guardar
    format='%(asctime)s: %(levelname)s [%(filename)s:%(lineno)s] %(message)s',
    datefmt='%I:%M:%S %p',  # Formato de hora: 12:30:45 PM
    handlers=[
        log.FileHandler(log_path, encoding='utf-8'),  # Guarda en archivo
        log.StreamHandler()  # Muestra en consola
    ]
)

# Esto es solo para testear si ejecuto este archivo directamente
if __name__ == '__main__':
    log.debug('Mensaje a nivel DEBUG')
    log.info('Mensaje a nivel de INFO')
    log.warning('Mensaje a nivel de WARNING')
    log.error('Mensaje a nivel de ERROR')
    log.critical('Mensaje a nivel de CRITICAL')