import json
from crud_service import (
    init, crear_proyecto, listar_proyectos, obtener_proyecto,
    actualizar_proyecto, eliminar_proyecto, simular_proyecto
)
import logger_base as _log
from constants import TIPOS_PROYECTO

log = _log.log

MENU = f"""
[WIP] Simulador de Impacto Ambiental (CLI)
1) Crear proyecto
2) Listar proyectos
3) Ver proyecto
4) Actualizar proyecto
5) Eliminar proyecto
6) Simular impacto
0) Salir
"""

def pedir(msg, cast=str, default=None):
    v = input(f"{msg} ({'Enter='+str(default) if default is not None else 'obligatorio'}): ").strip()
    if not v and default is not None:
        return default
    return cast(v)

def main():
    log.info('Iniciando aplicación CLI del Simulador de Impacto Ambiental')
    init()
    
    while True:
        print(MENU)
        op = input("Opción: ").strip()
        
        if op == "1":
            log.info('Usuario seleccionó: Crear proyecto')
            try:
                tipos_str = "|".join(TIPOS_PROYECTO)
                data = {
                    "id": pedir("id"),
                    "nombre": pedir("nombre"),
                    "tipo": pedir(f"tipo [{tipos_str}]"),
                    "area_ha": pedir("area_ha", float),
                    "duracion_meses": pedir("duracion_meses", int),
                    "ubicacion": pedir("ubicacion", str, ""),
                    "intensidad": pedir("intensidad (1-10)", int, 5),
                }
                log.debug(f'Datos del proyecto a crear: {data}')
                crear_proyecto(data)
                print(f"✓ Proyecto {data['id']} creado exitosamente")
                log.info(f'Proyecto {data["id"]} creado exitosamente')
            except ValueError as e:
                log.error(f'Error de validación al crear proyecto: {e}')
                print(f"Error de validación: {e}")
            except Exception as e:
                log.error(f'Error inesperado al crear proyecto: {e}')
                print(f"Error inesperado: {e}")
                
        elif op == "2":
            log.info('Usuario seleccionó: Listar proyectos')
            proyectos = listar_proyectos()
            log.debug(f'Se encontraron {len(proyectos)} proyectos')
            if not proyectos:
                log.info('No hay proyectos para mostrar')
                print("No hay proyectos registrados")
            for p in proyectos:
                print(vars(p))
                
        elif op == "3":
            log.info('Usuario seleccionó: Ver proyecto')
            pid = pedir("id")
            log.debug(f'Buscando proyecto con ID: {pid}')
            p = obtener_proyecto(pid)
            if p:
                log.debug(f'Proyecto encontrado: {p.id} - {p.nombre}')
                print(vars(p))
            else:
                log.warning(f'Proyecto no encontrado: {pid}')
                print("No existe")
                
        elif op == "4":
            log.info('Usuario seleccionó: Actualizar proyecto')
            pid = pedir("id")
            campo = pedir("campo a cambiar (nombre,tipo,area_ha,duracion_meses,ubicacion,intensidad)")
            valor = pedir("nuevo valor")
            
            # intento de casteo rápido
            try:
                if campo in ("area_ha",): 
                    valor = float(valor)
                if campo in ("duracion_meses","intensidad"): 
                    valor = int(valor)
                
                log.debug(f'Actualizando proyecto {pid}, campo {campo} = {valor}')
                resultado = actualizar_proyecto(pid, {campo: valor})
                
                if resultado:
                    log.info(f'Proyecto {pid} actualizado exitosamente - Campo: {campo}')
                    print("OK")
                else:
                    log.warning(f'Fallo al actualizar proyecto {pid} - No encontrado')
                    print("Fallo")
                    
            except ValueError as e:
                log.error(f'Error de conversión de tipo al actualizar proyecto {pid}: {e}')
                print("Error: Valor numérico inválido")
            except Exception as e:
                log.error(f'Error inesperado al actualizar proyecto {pid}: {e}')
                print("Error inesperado al actualizar")
                
        elif op == "5":
            log.info('Usuario seleccionó: Eliminar proyecto')
            pid = pedir("id")
            log.debug(f'Intentando eliminar proyecto: {pid}')
            
            if eliminar_proyecto(pid):
                log.info(f'Proyecto {pid} eliminado exitosamente')
                print("Eliminado")
            else:
                log.warning(f'Proyecto {pid} no encontrado para eliminar')
                print("No encontrado")
                
        elif op == "6":
            log.info('Usuario seleccionó: Simular impacto')
            pid = pedir("id")
            log.debug(f'Iniciando simulación para proyecto: {pid}')
            
            imp = simular_proyecto(pid)
            if imp:
                log.info(f'Simulación completada para proyecto {pid}. Riesgo total: {imp.riesgo_total:.1f}%')
                resultado = {
                    "proyecto_id": imp.proyecto_id,
                    "scores": {
                        "aire": imp.calidad_aire,
                        "agua": imp.calidad_agua,
                        "biodiversidad": imp.biodiversidad,
                        "uso_suelo": imp.uso_suelo
                    },
                    "riesgo_total": imp.riesgo_total,
                    "recomendaciones": imp.recomendaciones
                }
                print(json.dumps(resultado, indent=2, ensure_ascii=False))
            else:
                log.warning(f'Proyecto {pid} no encontrado para simulación')
                print("Proyecto no encontrado")
                
        elif op == "0":
            log.info('Usuario seleccionó salir. Finalizando aplicación CLI')
            print("¡Hasta luego!")
            break
            
        else:
            log.warning(f'Opción inválida ingresada: {op}')
            print("Opción inválida")

if __name__ == "__main__":
    try:
        main()
        log.info('Aplicación CLI finalizada correctamente')
    except KeyboardInterrupt:
        log.info('Aplicación CLI interrumpida por el usuario (Ctrl+C)')
        print("\nAplicación interrumpida")
    except Exception as e:
        log.critical(f'Error crítico en aplicación CLI: {e}')
        print(f"Error crítico: {e}")