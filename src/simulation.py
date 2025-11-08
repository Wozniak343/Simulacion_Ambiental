from typing import Dict
from src.models import Project, Impacto
import math
import src.logger_base as _log
from src.constants import TIPOS_PROYECTO, UMBRAL_RECOMENDACION, GEMINI_API_KEY

log = _log.log

# Instancia global del servicio de Gemini (se inicializa al primer uso)
_gemini_service = None

def _get_gemini_service():
    """Obtiene o crea la instancia del servicio de Gemini."""
    global _gemini_service
    if _gemini_service is None:
        try:
            from src.gemini_service import GeminiService
            _gemini_service = GeminiService(GEMINI_API_KEY)
            log.info('Servicio de Gemini inicializado para recomendaciones con IA')
        except ImportError as e:
            log.warning(f'No se pudo importar gemini_service: {e}. Instala google-generativeai')
            _gemini_service = False  # Marcar como no disponible
        except Exception as e:
            log.error(f'Error al inicializar Gemini: {e}')
            _gemini_service = False
    return _gemini_service if _gemini_service is not False else None

# Factores base por tipo (0 peor, 1 mejor)
FACTORES_TIPO = {
    "construccion": {"aire": 0.85, "agua": 0.9, "biodiv": 0.8, "suelo": 0.75},
    "mineria": {"aire": 0.7, "agua": 0.6, "biodiv": 0.55, "suelo": 0.5},
    "agricultura": {"aire": 0.9, "agua": 0.7, "biodiv": 0.65, "suelo": 0.7},
}

def _clip(x: float, lo=0.0, hi=100.0) -> float:
    """Limita un valor entre un mínimo y un máximo."""
    return max(lo, min(hi, x))

def simular(p: Project) -> Impacto:
    """Simula el impacto ambiental de un proyecto usando IA o fórmulas matemáticas."""
    log.info(f'Iniciando simulación para proyecto: {p.id} ({p.tipo})')
    log.debug(f'Parámetros del proyecto: área={p.area_ha}ha, duración={p.duracion_meses}meses, intensidad={p.intensidad}')
    
    # Intentar usar Gemini AI para calcular las métricas
    gemini = _get_gemini_service()
    metricas = None
    
    if gemini:
        log.info('Calculando métricas de impacto con IA (Gemini)')
        try:
            metricas = gemini.calcular_impacto_ambiental(
                proyecto_tipo=p.tipo,
                proyecto_nombre=p.nombre,
                area_ha=p.area_ha,
                duracion_meses=p.duracion_meses,
                intensidad=p.intensidad,
                ubicacion=p.ubicacion
            )
        except Exception as e:
            log.error(f'Error al calcular con IA: {e}')
            metricas = None
    
    # Si Gemini no está disponible o falló, usar cálculo por fórmulas
    if metricas is None:
        log.info('Calculando métricas con fórmulas matemáticas (fallback)')
        metricas = _calcular_con_formulas(p)
    
    # Extraer métricas
    aire = metricas['calidad_aire']
    agua = metricas['calidad_agua']
    biod = metricas['biodiversidad']
    suelo = metricas['uso_suelo']
    riesgo = metricas['riesgo_total']
    
    log.debug(f'Puntuaciones calculadas - Aire: {aire:.1f}, Agua: {agua:.1f}, Biodiversidad: {biod:.1f}, Suelo: {suelo:.1f}')
    log.debug(f'Riesgo total calculado: {riesgo:.1f}%')

    # Generar recomendaciones con IA
    recs: Dict[str,str] = {}
    
    if gemini:
        # Usar Gemini AI para generar recomendaciones personalizadas
        log.info('Generando recomendaciones con IA (Gemini)')
        try:
            recs = gemini.generar_recomendaciones(
                proyecto_tipo=p.tipo,
                proyecto_nombre=p.nombre,
                area_ha=p.area_ha,
                duracion_meses=p.duracion_meses,
                intensidad=p.intensidad,
                calidad_aire=aire,
                calidad_agua=agua,
                biodiversidad=biod,
                uso_suelo=suelo,
                riesgo_total=riesgo
            )
        except Exception as e:
            log.error(f'Error al generar recomendaciones con IA: {e}')
            # Fallback a recomendaciones básicas
            recs = _generar_recomendaciones_basicas(aire, agua, biod, suelo)
    else:
        # Sin IA disponible, usar recomendaciones básicas
        log.info('Generando recomendaciones básicas (sin IA)')
        recs = _generar_recomendaciones_basicas(aire, agua, biod, suelo)

    log.info(f'Simulación completada - Riesgo total: {riesgo:.1f}%, Recomendaciones generadas: {len(recs)}')
    
    return Impacto(
        proyecto_id=p.id,
        calidad_aire=aire,
        calidad_agua=agua,
        biodiversidad=biod,
        uso_suelo=suelo,
        riesgo_total=riesgo,
        recomendaciones=recs
    )

def _calcular_con_formulas(p: Project) -> Dict[str, float]:
    """
    Calcula las métricas usando fórmulas matemáticas (fallback sin IA).
    
    Args:
        p: Proyecto a evaluar
        
    Returns:
        Diccionario con las métricas calculadas
    """
    if p.tipo not in FACTORES_TIPO:
        log.warning(f"Tipo de proyecto desconocido: {p.tipo}. Se asumirá 'construccion'.")
    
    f = FACTORES_TIPO.get(p.tipo, FACTORES_TIPO["construccion"])
    escala = 1 + (p.intensidad - 5) * 0.08  # +/- 40% máx
    area_factor = 1 + math.log10(max(p.area_ha, 1)) * 0.1
    tiempo_factor = 1 + (p.duracion_meses/12) * 0.05
    
    log.debug(f'Factores calculados - escala: {escala:.2f}, área: {area_factor:.2f}, tiempo: {tiempo_factor:.2f}')

    # Puntuaciones (100 es óptimo/menor impacto)
    aire = _clip(100 * f["aire"] / (escala * area_factor * tiempo_factor))
    agua = _clip(100 * f["agua"] / (escala * area_factor * tiempo_factor))
    biod = _clip(100 * f["biodiv"] / (escala * area_factor * tiempo_factor))
    suelo = _clip(100 * f["suelo"] / (escala * area_factor * tiempo_factor))

    # Riesgo total (0-100, mayor es peor)
    riesgo = _clip(100 - (0.25*aire + 0.25*agua + 0.25*biod + 0.25*suelo))
    
    return {
        'calidad_aire': aire,
        'calidad_agua': agua,
        'biodiversidad': biod,
        'uso_suelo': suelo,
        'riesgo_total': riesgo
    }

def _generar_recomendaciones_basicas(aire: float, agua: float, biod: float, suelo: float) -> Dict[str, str]:
    """
    Genera recomendaciones básicas sin IA.
    
    Args:
        aire, agua, biod, suelo: Puntuaciones de cada métrica
        
    Returns:
        Diccionario con recomendaciones básicas detalladas
    """
    recs: Dict[str,str] = {}
    
    if aire < UMBRAL_RECOMENDACION: 
        recs["aire"] = """Implementar sistema de control de material particulado mediante aspersión con agua nebulizada cada 4 horas en áreas de movimiento de tierras y vías no pavimentadas. Instalar barreras vegetales perimetrales con especies de follaje denso (altura mínima 3m) y realizar monitoreo trimestral de PM10/PM2.5 según DS 074-2001-PCM. Mantener velocidad máxima de 20 km/h en rutas internas y cubrir materiales en transporte con lonas impermeables."""
        log.debug('Recomendación agregada para calidad del aire')
    if agua < UMBRAL_RECOMENDACION: 
        recs["agua"] = """Construir sistema de sedimentación primaria con tres etapas (desarenador, sedimentador y filtro de grava) con capacidad de retención de 48 horas. Implementar planta de tratamiento modular para aguas residuales domésticas e industriales según ISO 14001:2015, con análisis fisicoquímicos mensuales (DBO, DQO, SST, pH, metales pesados). Establecer programa de manejo de vertimientos con reutilización de 60% del agua tratada en riego de vías y áreas verdes."""
        log.debug('Recomendación agregada para calidad del agua')
    if biod < UMBRAL_RECOMENDACION: 
        recs["biodiversidad"] = """Desarrollar Plan de Manejo de Biodiversidad (PMB) con inventario completo de flora y fauna en área de influencia directa e indirecta. Ejecutar programa de rescate y reubicación de especies con protocolo aprobado por autoridad ambiental, priorizando especies endémicas o en peligro según lista roja UICN. Crear tres corredores biológicos de mínimo 50m de ancho con especies nativas, instalando 20 cajas nido para aves y refugios para pequeños mamíferos. Monitoreo semestral con fototrampeo y transectos."""
        log.debug('Recomendación agregada para biodiversidad')
    if suelo < UMBRAL_RECOMENDACION: 
        recs["suelo"] = """Implementar estabilización geotécnica de taludes con pendiente máxima 2:1 (H:V), utilizando geomallas biaxiales de alta resistencia y sistemas de drenaje subsuperficial. Aplicar revegetalización inmediata con hidrosiembra de mezcla de gramíneas nativas (70%) y leguminosas fijadoras de nitrógeno (30%) a razón de 35g/m². Construir terrazas de infiltración cada 5m de desnivel y zanjas de coronación. Realizar análisis de estabilidad de suelos cada 6 meses durante fase operativa."""
        log.debug('Recomendación agregada para uso del suelo')
    
    return recs