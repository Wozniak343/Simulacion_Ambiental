"""
Constantes globales del proyecto Simulador Ambiental
"""

# Tipos de proyectos válidos
TIPOS_PROYECTO = ["construccion", "agricultura", "mineria"]

# API Keys
GEMINI_API_KEY = "AIzaSyCBIesdP9H99p_YsuO7HO9ZaAyGVYeauEA"

# Validaciones de datos
INTENSIDAD_MIN = 1
INTENSIDAD_MAX = 10
INTENSIDAD_DEFAULT = 5

AREA_MIN = 0.01  # hectáreas mínimas
DURACION_MIN = 1  # meses mínimos

# Umbrales de calidad para recomendaciones
UMBRAL_RECOMENDACION = 70.0

# Mensajes de error comunes
MSG_ERROR_TIPO_INVALIDO = f"Tipo de proyecto inválido. Debe ser uno de: {', '.join(TIPOS_PROYECTO)}"
MSG_ERROR_INTENSIDAD = f"La intensidad debe estar entre {INTENSIDAD_MIN} y {INTENSIDAD_MAX}"
MSG_ERROR_AREA = f"El área debe ser mayor a {AREA_MIN} hectáreas"
MSG_ERROR_DURACION = f"La duración debe ser de al menos {DURACION_MIN} mes(es)"
MSG_ERROR_ID_VACIO = "El ID no puede estar vacío"
MSG_ERROR_NOMBRE_VACIO = "El nombre no puede estar vacío"
