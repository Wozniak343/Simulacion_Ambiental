"""
Este archivo maneja todo lo relacionado con guardar y leer datos del CSV.
Funciona como una mini base de datos para los proyectos.
"""
import csv
import os
from typing import List, Optional, Dict
from src.models import Project
import src.logger_base as _log
log = _log.log

# Ruta donde se guarda el archivo CSV
CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "proyectos.csv")
# Columnas que tiene el CSV
CSV_FIELDS = ["id","nombre","tipo","area_ha","duracion_meses","ubicacion","intensidad"]

def init_store():
    """Crea el archivo CSV si no existe."""
    try:
        if not os.path.exists(CSV_PATH):
            # Creo el archivo con los encabezados
            with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
                writer.writeheader()
            log.info("Archivo de datos creado: %s", CSV_PATH)
    except IOError as e:
        log.error("Error al crear archivo de datos: %s", e)
        raise

def create(p: Project) -> None:
    """Guarda un nuevo proyecto en el CSV."""
    init_store()
    
    # Verifico que no exista ya un proyecto con ese ID
    if read_by_id(p.id) is not None:
        log.warning("Intento de crear proyecto con ID existente: %s", p.id)
        raise ValueError(f"Ya existe un proyecto con ID: {p.id}")
    
    try:
        # Abro el archivo en modo append para agregar al final
        with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
            # Escribo los datos del proyecto como un diccionario
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
    """Lee todos los proyectos del CSV y los devuelve como lista."""
    init_store()
    items: List[Project] = []
    
    try:
        # Abro el archivo en modo lectura
        with open(CSV_PATH, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            # Leo cada fila del CSV
            for row in reader:
                try:
                    # Creo un objeto Project con los datos de la fila
                    items.append(Project(
                        id=row["id"],
                        nombre=row["nombre"],
                        tipo=row["tipo"],
                        area_ha=float(row["area_ha"]),  # Convierto a número decimal
                        duracion_meses=int(row["duracion_meses"]),  # Convierto a entero
                        ubicacion=row.get("ubicacion",""),  # Si no existe, uso string vacío
                        intensidad=int(row.get("intensidad",5)),  # Si no existe, uso 5
                    ))
                except (ValueError, KeyError) as e:
                    # Si hay un error en una fila, la ignoro y sigo con la siguiente
                    log.warning("Fila inválida en CSV, omitiendo: %s", e)
                    continue
    except IOError as e:
        log.error("Error al leer proyectos: %s", e)
        return []
    
    log.debug("Leídos %d proyectos del almacenamiento", len(items))
    return items

def read_by_id(pid: str) -> Optional[Project]:
    """Busca un proyecto específico por su ID."""
    # Recorro todos los proyectos hasta encontrar el que coincida
    for p in read_all():
        if p.id == pid:
            return p
    return None  # Si no lo encuentro, devuelvo None

def update(pid: str, cambios: Dict) -> bool:
    """Actualiza los datos de un proyecto existente."""
    init_store()
    rows = []
    encontrado = False
    
    try:
        # Primero leo todos los proyectos
        with open(CSV_PATH, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["id"] == pid:
                    # Encontré el proyecto, actualizo sus campos
                    encontrado = True
                    for k, v in cambios.items():
                        if k in row and k != "id":  # No dejo cambiar el ID
                            row[k] = str(v)
                rows.append(row)
        
        if not encontrado:
            log.warning("Proyecto no encontrado para actualizar: %s", pid)
            return False
        
        # Reescribo el archivo con todos los proyectos actualizados
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
    """Elimina un proyecto del CSV."""
    init_store()
    rows = []
    eliminado = False
    
    try:
        # Leo todos los proyectos
        with open(CSV_PATH, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["id"] == pid:
                    # Encontré el que quiero eliminar, no lo agrego a la lista
                    eliminado = True
                    continue
                rows.append(row)
        
        # Reescribo el archivo sin el proyecto eliminado
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