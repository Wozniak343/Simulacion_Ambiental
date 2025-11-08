import logging as log

log.basicConfig(
    level=log.DEBUG,
    format='%(asctime)s: %(levelname)s [%(filename)s:%(lineno)s] %(message)s',
    datefmt='%I:%M:%S %p',
    handlers=[
        log.FileHandler('capa_datos.log', encoding='utf-8'),
        log.StreamHandler()
    ]
)

if __name__ == '__main__':
    log.debug('Mensaje a nivel DEBUG')
    log.info('Mensaje a nivel de INFO')
    log.warning('Mensaje a nivel de WARNING')
    log.error('Mensaje a nivel de ERROR')
    log.critical('Mensaje a nivel de CRITICAL')