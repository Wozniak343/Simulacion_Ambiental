from typing import Optional, Dict, List
from src.models import Project, Impacto
from src import store
from src import simulation
import src.logger_base as _log
from src.constants import (
    TIPOS_PROYECTO, INTENSIDAD_MIN, INTENSIDAD_MAX, AREA_MIN, DURACION_MIN,
    MSG_ERROR_TIPO_INVALIDO, MSG_ERROR_INTENSIDAD, MSG_ERROR_AREA,
    MSG_ERROR_DURACION, MSG_ERROR_ID_VACIO, MSG_ERROR_NOMBRE_VACIO
)

log = _log.log

def init():
    store.init_store()

def _validar_proyecto(data: Dict) -> Optional[str]:
    """Valida los datos de un proyecto. Retorna mensaje de error o None si es válido."""
    # Validar ID y nombre
    if not data.get("id", "").strip():
        return MSG_ERROR_ID_VACIO
    if not data.get("nombre", "").strip():
        return MSG_ERROR_NOMBRE_VACIO
    
    # Validar tipo
    if data.get("tipo") not in TIPOS_PROYECTO:
        return MSG_ERROR_TIPO_INVALIDO
    
    # Validar área
    try:
        area = float(data.get("area_ha", 0))
        if area < AREA_MIN:
            return MSG_ERROR_AREA
    except (ValueError, TypeError):
        return f"El área debe ser un número válido"
    
    # Validar duración
    try:
        duracion = int(data.get("duracion_meses", 0))
        if duracion < DURACION_MIN:
            return MSG_ERROR_DURACION
    except (ValueError, TypeError):
        return f"La duración debe ser un número entero válido"
    
    # Validar intensidad
    try:
        intensidad = int(data.get("intensidad", 5))
        if not (INTENSIDAD_MIN <= intensidad <= INTENSIDAD_MAX):
            return MSG_ERROR_INTENSIDAD
    except (ValueError, TypeError):
        return f"La intensidad debe ser un número entero válido"
    
    return None

def crear_proyecto(data: Dict) -> Optional[Project]:
    # Validar datos primero
    error = _validar_proyecto(data)
    if error:
        log.error(f'Validación fallida al crear proyecto: {error}')
        raise ValueError(error)
    
    try:
        p = Project(**data)
        store.create(p)
        log.info(f'Proyecto {p.id} creado exitosamente')
        return p
    except TypeError as e:
        log.error(f'Error de tipo en datos para crear proyecto: {e}')
        raise ValueError(f"Error en los datos del proyecto: {e}")

def listar_proyectos() -> List[Project]:
    return store.read_all()

def obtener_proyecto(pid: str) -> Optional[Project]:
    return store.read_by_id(pid)

def actualizar_proyecto(pid: str, cambios: Dict) -> bool:
    resultado = store.update(pid, cambios)
    if resultado:
        log.info(f'Proyecto {pid} actualizado exitosamente')
    else:
        log.warning(f'No se pudo actualizar el proyecto {pid}')
    return resultado

def eliminar_proyecto(pid: str) -> bool:
    resultado = store.delete(pid)
    if resultado:
        log.info(f'Proyecto {pid} eliminado exitosamente')
    else:
        log.warning(f'No se pudo eliminar el proyecto {pid}')
    return resultado

def simular_proyecto(pid: str) -> Optional[Impacto]:
    p = obtener_proyecto(pid)
    if not p:
        log.error(f'No existe el proyecto {pid} para simular')
        return None
    impacto = simulation.simular(p)
    if impacto:
        log.info(f'Simulación completada para proyecto {pid}. Riesgo total: {impacto.riesgo_total:.1f}%')
    return impacto