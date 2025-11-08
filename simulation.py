from typing import Dict
from models import Project, Impacto
import math
import logger_base as _log
from constants import TIPOS_PROYECTO, UMBRAL_RECOMENDACION

log = _log.log

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
    """Simula el impacto ambiental de un proyecto."""
    log.info(f'Iniciando simulación para proyecto: {p.id} ({p.tipo})')
    log.debug(f'Parámetros del proyecto: área={p.area_ha}ha, duración={p.duracion_meses}meses, intensidad={p.intensidad}')
    
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

    log.debug(f'Puntuaciones calculadas - Aire: {aire:.1f}, Agua: {agua:.1f}, Biodiversidad: {biod:.1f}, Suelo: {suelo:.1f}')
    log.debug(f'Riesgo total calculado: {riesgo:.1f}%')

    recs: Dict[str,str] = {}
    if aire < UMBRAL_RECOMENDACION: 
        recs["aire"] = "Control de polvo/PM y riego de vías."
        log.debug('Recomendación agregada para calidad del aire')
    if agua < UMBRAL_RECOMENDACION: 
        recs["agua"] = "Sedimentadores y manejo de vertimientos (ISO 14001)."
        log.debug('Recomendación agregada para calidad del agua')
    if biod < UMBRAL_RECOMENDACION: 
        recs["biodiversidad"] = "Plan de manejo de fauna/flora y reubicación de especies."
        log.debug('Recomendación agregada para biodiversidad')
    if suelo < UMBRAL_RECOMENDACION: 
        recs["suelo"] = "Estabilización de taludes y revegetalización."
        log.debug('Recomendación agregada para uso del suelo')

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