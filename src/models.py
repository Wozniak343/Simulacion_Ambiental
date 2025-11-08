"""
Modelos de datos para el Simulador de Impacto Ambiental.

Este módulo define las estructuras de datos principales utilizadas en el sistema.
"""
from dataclasses import dataclass, field
from typing import Dict

@dataclass
class Project:
    """
    Representa un proyecto a evaluar ambientalmente.
    
    Attributes:
        id: Identificador único del proyecto
        nombre: Nombre descriptivo del proyecto
        tipo: Tipo de proyecto (construccion, mineria, agricultura)
        area_ha: Área del proyecto en hectáreas
        duracion_meses: Duración estimada del proyecto en meses
        ubicacion: Ubicación geográfica del proyecto
        intensidad: Nivel de intensidad del impacto (1-10)
    """
    id: str
    nombre: str
    tipo: str
    area_ha: float
    duracion_meses: int
    ubicacion: str = ""
    intensidad: int = 5
    
@dataclass
class Impacto:
    """
    Representa el resultado de una simulación de impacto ambiental.
    
    Attributes:
        proyecto_id: ID del proyecto evaluado
        calidad_aire: Puntuación de calidad del aire (0-100, mayor es mejor)
        calidad_agua: Puntuación de calidad del agua (0-100, mayor es mejor)
        biodiversidad: Puntuación de impacto en biodiversidad (0-100, mayor es mejor)
        uso_suelo: Puntuación de uso del suelo (0-100, mayor es mejor)
        riesgo_total: Porcentaje de riesgo total (0-100, mayor es peor)
        recomendaciones: Diccionario con recomendaciones de mitigación por categoría
    """
    proyecto_id: str
    calidad_aire: float
    calidad_agua: float
    biodiversidad: float
    uso_suelo: float
    riesgo_total: float
    recomendaciones: Dict[str, str] = field(default_factory=dict)
