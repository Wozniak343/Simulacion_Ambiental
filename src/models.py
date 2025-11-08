"""
Modelos de datos para el Simulador de Impacto Ambiental.
Aquí definimos las clases principales que usamos en todo el proyecto.
"""
from dataclasses import dataclass, field
from typing import Dict

@dataclass
class Project:
    """
    Clase que representa un proyecto ambiental.
    Uso dataclass porque hace el código más limpio y fácil de leer.
    """
    # Campos obligatorios del proyecto
    id: str                    # Identificador único
    nombre: str               # Nombre del proyecto
    tipo: str                 # Tipo: construccion, mineria o agricultura
    area_ha: float            # Área en hectáreas
    duracion_meses: int       # Duración en meses
    
    # Campos opcionales con valores por defecto
    ubicacion: str = ""       # Dónde está el proyecto
    intensidad: int = 5       # Escala del 1 al 10
    
@dataclass
class Impacto:
    """
    Clase que guarda los resultados de la simulación.
    Almacena todas las métricas calculadas y las recomendaciones.
    """
    proyecto_id: str          # A qué proyecto pertenece
    
    # Métricas ambientales (0-100, más alto = mejor)
    calidad_aire: float       # Qué tan limpio queda el aire
    calidad_agua: float       # Calidad del agua después del proyecto
    biodiversidad: float      # Impacto en plantas y animales
    uso_suelo: float          # Cómo afecta al suelo
    
    # Riesgo total (0-100, más alto = peor)
    riesgo_total: float       # Porcentaje de riesgo general
    
    # Diccionario con las recomendaciones por categoría
    recomendaciones: Dict[str, str] = field(default_factory=dict)
