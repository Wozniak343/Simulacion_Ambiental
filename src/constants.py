"""
Aquí guardo todas las constantes del proyecto.
Es más fácil cambiar valores si están todos en un solo lugar.
"""

# Los tipos de proyecto que acepta el sistema
TIPOS_PROYECTO = ["construccion", "agricultura", "mineria"]

# Mi API key de Google Gemini para usar la IA
GEMINI_API_KEY = "AIzaSyCBIesdP9H99p_YsuO7HO9ZaAyGVYeauEA"

# Valores mínimos y máximos para validar datos
INTENSIDAD_MIN = 1          # Mínima intensidad de impacto
INTENSIDAD_MAX = 10         # Máxima intensidad de impacto
INTENSIDAD_DEFAULT = 5      # Valor por defecto

AREA_MIN = 0.01            # Hectáreas mínimas (0.01 = 100 m²)
DURACION_MIN = 1           # Al menos 1 mes de duración

# Si una métrica está por debajo de esto, generamos recomendaciones
UMBRAL_RECOMENDACION = 70.0

# Mensajes de error que se muestran al usuario
MSG_ERROR_TIPO_INVALIDO = f"Tipo de proyecto inválido. Debe ser uno de: {', '.join(TIPOS_PROYECTO)}"
MSG_ERROR_INTENSIDAD = f"La intensidad debe estar entre {INTENSIDAD_MIN} y {INTENSIDAD_MAX}"
MSG_ERROR_AREA = f"El área debe ser mayor a {AREA_MIN} hectáreas"
MSG_ERROR_DURACION = f"La duración debe ser de al menos {DURACION_MIN} mes(es)"
MSG_ERROR_ID_VACIO = "El ID no puede estar vacío"
MSG_ERROR_NOMBRE_VACIO = "El nombre no puede estar vacío"
