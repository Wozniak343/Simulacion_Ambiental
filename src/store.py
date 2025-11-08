import csv
import os
from typing import List, Optional, Dict
from src.models import Project
import src.logger_base as _log
log = _log.log

CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "proyectos.csv")
CSV_FIELDS = ["id","nombre","tipo","area_ha","duracion_meses","ubicacion","intensidad"]

def init_store():
    """Inicializa el archivo CSV si no existe."""
    try:
        if not os.path.exists(CSV_PATH):
            with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
                writer.writeheader()
            log.info("Archivo de datos creado: %s", CSV_PATH)
    except IOError as e:
        log.error("Error al crear archivo de datos: %s", e)
        raise

def create(p: Project) -> None:
    """Crea un nuevo proyecto en el almacenamiento."""
    init_store()
    if read_by_id(p.id) is not None:
        log.warning("Intento de crear proyecto con ID existente: %s", p.id)
        raise ValueError(f"Ya existe un proyecto con ID: {p.id}")
    
    try:
        with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
            writer.writerow({
                "id": p.id,
                "nombre": p.nombre,
                "tipo": p.tipo,
                "area_ha": p.area_ha,
                "duracion_meses": p.duracion_meses,
                "ubicacion": p.ubicacion,
                "intensidad": p.intensidad
            })
        log.debug("Proyecto creado: %s", p.id)
    except IOError as e:
        log.error("Error al escribir proyecto %s: %s", p.id, e)
        raise

def read_all() -> List[Project]:
    """Lee todos los proyectos del almacenamiento."""
    init_store()
    items: List[Project] = []
    
    try:
        with open(CSV_PATH, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    items.append(Project(
                        id=row["id"],
                        nombre=row["nombre"],
                        tipo=row["tipo"],
                        area_ha=float(row["area_ha"]),
                        duracion_meses=int(row["duracion_meses"]),
                        ubicacion=row.get("ubicacion",""),
                        intensidad=int(row.get("intensidad",5)),
                    ))
                except (ValueError, KeyError) as e:
                    log.warning("Fila inválida en CSV, omitiendo: %s", e)
                    continue
    except IOError as e:
        log.error("Error al leer proyectos: %s", e)
        return []
    
    log.debug("Leídos %d proyectos del almacenamiento", len(items))
    return items

def read_by_id(pid: str) -> Optional[Project]:
    """Busca un proyecto por su ID."""
    for p in read_all():
        if p.id == pid:
            return p
    return None

def update(pid: str, cambios: Dict) -> bool:
    """Actualiza un proyecto existente."""
    init_store()
    rows = []
    encontrado = False
    
    try:
        with open(CSV_PATH, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["id"] == pid:
                    encontrado = True
                    for k, v in cambios.items():
                        if k in row and k != "id":  # No permitir cambiar el ID
                            row[k] = str(v)
                rows.append(row)
        
        if not encontrado:
            log.warning("Proyecto no encontrado para actualizar: %s", pid)
            return False
        
        with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
            writer.writeheader()
            writer.writerows(rows)
        
        log.debug("Proyecto %s actualizado: %s", pid, cambios)
        return True
        
    except IOError as e:
        log.error("Error al actualizar proyecto %s: %s", pid, e)
        return False

def delete(pid: str) -> bool:
    """Elimina un proyecto por su ID."""
    init_store()
    rows = []
    eliminado = False
    
    try:
        with open(CSV_PATH, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["id"] == pid:
                    eliminado = True
                    continue
                rows.append(row)
        
        with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
            writer.writeheader()
            writer.writerows(rows)
        
        if eliminado:
            log.debug("Proyecto eliminado: %s", pid)
        else:
            log.warning("Proyecto no encontrado para eliminar: %s", pid)
        return eliminado
        
    except IOError as e:
        log.error("Error al eliminar proyecto %s: %s", pid, e)
        return False