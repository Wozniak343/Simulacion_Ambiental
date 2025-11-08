"""
Servicio de integración con Google Gemini AI para generar recomendaciones.
"""
import google.generativeai as genai
import src.logger_base as _log
from typing import Dict, Optional

log = _log.log

class GeminiService:
    """Servicio para interactuar con la API de Gemini."""
    
    def __init__(self, api_key: str):
        """
        Inicializa el servicio de Gemini.
        
        Args:
            api_key: Clave de API de Google Gemini
        """
        self.api_key = api_key
        genai.configure(api_key=api_key)
        # Usar gemini-2.0-flash que es rápido y está disponible
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        log.info('Servicio de Gemini AI inicializado')
    
    def generar_recomendaciones(
        self,
        proyecto_tipo: str,
        proyecto_nombre: str,
        area_ha: float,
        duracion_meses: int,
        intensidad: int,
        calidad_aire: float,
        calidad_agua: float,
        biodiversidad: float,
        uso_suelo: float,
        riesgo_total: float
    ) -> Dict[str, str]:
        """
        Genera recomendaciones personalizadas usando Gemini AI.
        
        Args:
            proyecto_tipo: Tipo de proyecto (construccion, mineria, agricultura)
            proyecto_nombre: Nombre del proyecto
            area_ha: Área en hectáreas
            duracion_meses: Duración en meses
            intensidad: Nivel de intensidad (1-10)
            calidad_aire: Puntuación calidad del aire (0-100)
            calidad_agua: Puntuación calidad del agua (0-100)
            biodiversidad: Puntuación biodiversidad (0-100)
            uso_suelo: Puntuación uso del suelo (0-100)
            riesgo_total: Porcentaje de riesgo total
            
        Returns:
            Diccionario con recomendaciones por categoría
        """
        log.info(f'Generando recomendaciones con IA para proyecto tipo {proyecto_tipo}')
        
        prompt = self._construir_prompt_recomendaciones(
            proyecto_tipo, proyecto_nombre, area_ha, duracion_meses, intensidad,
            calidad_aire, calidad_agua, biodiversidad, uso_suelo, riesgo_total
        )
        
        try:
            response = self.model.generate_content(prompt)
            recomendaciones = self._parsear_respuesta(response.text)
            log.info(f'Recomendaciones generadas exitosamente: {len(recomendaciones)} categorías')
            return recomendaciones
            
        except Exception as e:
            log.error(f'Error al generar recomendaciones con Gemini: {e}')
            return self._recomendaciones_fallback(
                calidad_aire, calidad_agua, biodiversidad, uso_suelo
            )
    
    def calcular_impacto_ambiental(
        self,
        proyecto_tipo: str,
        proyecto_nombre: str,
        area_ha: float,
        duracion_meses: int,
        intensidad: int,
        ubicacion: str = ""
    ) -> Dict[str, float]:
        """
        Calcula el impacto ambiental usando Gemini AI.
        
        Args:
            proyecto_tipo: Tipo de proyecto (construccion, mineria, agricultura)
            proyecto_nombre: Nombre del proyecto
            area_ha: Área en hectáreas
            duracion_meses: Duración en meses
            intensidad: Nivel de intensidad (1-10)
            ubicacion: Ubicación del proyecto
            
        Returns:
            Diccionario con las métricas calculadas:
            {
                'calidad_aire': float (0-100),
                'calidad_agua': float (0-100),
                'biodiversidad': float (0-100),
                'uso_suelo': float (0-100),
                'riesgo_total': float (0-100)
            }
        """
        log.info(f'Calculando impacto ambiental con IA para proyecto: {proyecto_nombre}')
        
        prompt = self._construir_prompt_impacto(
            proyecto_tipo, proyecto_nombre, area_ha, duracion_meses, 
            intensidad, ubicacion
        )
        
        try:
            response = self.model.generate_content(prompt)
            metricas = self._parsear_metricas(response.text)
            log.info(f'Métricas calculadas por IA - Riesgo: {metricas.get("riesgo_total", 0):.1f}%')
            return metricas
            
        except Exception as e:
            log.error(f'Error al calcular impacto con Gemini: {e}')
            # Retornar None para indicar que se debe usar el cálculo por fórmulas
            return None
    
    def _construir_prompt_impacto(
        self,
        tipo: str,
        nombre: str,
        area: float,
        duracion: int,
        intensidad: int,
        ubicacion: str
    ) -> str:
        """Construye el prompt para calcular el impacto ambiental."""
        ubicacion_texto = f"\n- Ubicación: {ubicacion}" if ubicacion else ""
        
        return f"""Eres un experto analista ambiental con conocimiento profundo en evaluación de impactos para proyectos de construcción, minería y agricultura.

PROYECTO A EVALUAR:
- Nombre: {nombre}
- Tipo: {tipo}
- Área: {area} hectáreas
- Duración: {duracion} meses
- Intensidad del impacto: {intensidad}/10{ubicacion_texto}

TAREA:
Calcula las siguientes métricas de impacto ambiental en una escala de 0 a 100, donde:
- **100 = ÓPTIMO** (mínimo impacto, máxima calidad ambiental)
- **0 = PÉSIMO** (máximo impacto, destrucción ambiental)

Considera factores como:
- Tipo de proyecto y sus características inherentes
- Área afectada (mayor área = mayor impacto)
- Duración (más tiempo = más impacto acumulado)
- Intensidad de las operaciones (1=muy bajo, 10=muy alto)
- Estándares ambientales típicos para este tipo de proyecto

FORMATO DE RESPUESTA OBLIGATORIO (números decimales):
CALIDAD_AIRE: [0-100]
CALIDAD_AGUA: [0-100]
BIODIVERSIDAD: [0-100]
USO_SUELO: [0-100]
RIESGO_TOTAL: [0-100]

EJEMPLOS DE REFERENCIA:
- Construcción pequeña (1ha, 6 meses, int:3): Aire=85, Agua=88, Biodiv=82, Suelo=80, Riesgo=17
- Minería grande (100ha, 48 meses, int:9): Aire=35, Agua=28, Biodiv=25, Suelo=22, Riesgo=72
- Agricultura media (20ha, 36 meses, int:4): Aire=80, Agua=70, Biodiv=68, Suelo=72, Riesgo=25

Responde SOLO con los números en el formato indicado. NO agregues explicaciones."""

    def _parsear_metricas(self, texto: str) -> Dict[str, float]:
        """
        Parsea las métricas de impacto de la respuesta de Gemini.
        
        Args:
            texto: Respuesta de Gemini con las métricas
            
        Returns:
            Diccionario con las métricas parseadas
        """
        metricas = {}
        lineas = texto.strip().split('\n')
        
        mapeo = {
            'CALIDAD_AIRE': 'calidad_aire',
            'CALIDAD_AGUA': 'calidad_agua',
            'BIODIVERSIDAD': 'biodiversidad',
            'USO_SUELO': 'uso_suelo',
            'RIESGO_TOTAL': 'riesgo_total'
        }
        
        for linea in lineas:
            linea = linea.strip()
            if not linea:
                continue
            
            for clave_upper, clave_lower in mapeo.items():
                if linea.upper().startswith(clave_upper):
                    # Extraer el número después de los dos puntos
                    try:
                        valor_str = linea.split(':')[1].strip()
                        # Limpiar cualquier carácter no numérico excepto punto decimal
                        valor_str = ''.join(c for c in valor_str if c.isdigit() or c == '.')
                        valor = float(valor_str)
                        # Asegurar que esté en rango 0-100
                        valor = max(0.0, min(100.0, valor))
                        metricas[clave_lower] = valor
                        log.debug(f'Métrica parseada: {clave_lower} = {valor}')
                    except (ValueError, IndexError) as e:
                        log.warning(f'Error al parsear {clave_upper}: {e}')
                    break
        
        # Validar que tengamos todas las métricas
        requeridas = ['calidad_aire', 'calidad_agua', 'biodiversidad', 'uso_suelo', 'riesgo_total']
        if not all(k in metricas for k in requeridas):
            faltantes = [k for k in requeridas if k not in metricas]
            log.error(f'Métricas faltantes en respuesta de Gemini: {faltantes}')
            return None
        
        log.debug(f'Métricas parseadas exitosamente: {metricas}')
        return metricas
    
    def _construir_prompt_recomendaciones(
        self,
        tipo: str,
        nombre: str,
        area: float,
        duracion: int,
        intensidad: int,
        aire: float,
        agua: float,
        biodiv: float,
        suelo: float,
        riesgo: float
    ) -> str:
        """Construye el prompt para generar recomendaciones."""
        return f"""Eres un experto consultor ambiental certificado con 15 años de experiencia. Analiza el siguiente proyecto y proporciona recomendaciones detalladas, técnicas y específicas para mitigar su impacto ambiental.

DATOS DEL PROYECTO:
- Nombre: {nombre}
- Tipo: {tipo}
- Área: {area} hectáreas
- Duración: {duracion} meses
- Intensidad del impacto: {intensidad}/10

MÉTRICAS CALCULADAS (0-100, donde 100 es óptimo):
- Calidad del Aire: {aire:.1f}
- Calidad del Agua: {agua:.1f}
- Biodiversidad: {biodiv:.1f}
- Uso del Suelo: {suelo:.1f}
- Riesgo Total: {riesgo:.1f}%

INSTRUCCIONES:
Genera recomendaciones SOLO para las métricas que tengan puntuación menor a 70. Para cada métrica problemática, proporciona UNA recomendación detallada que incluya:

1. Medidas técnicas específicas con parámetros cuantificables
2. Tecnologías, equipos o metodologías concretas
3. Referencias a normativas ambientales aplicables (ISO, leyes nacionales, etc.)
4. Cronogramas o frecuencias de implementación
5. Indicadores de éxito medibles

Cada recomendación debe tener entre 4-6 líneas de texto detallado y técnico, orientado a profesionales ambientales.

Usa EXACTAMENTE este formato:
AIRE: [recomendación detallada de 4-6 líneas si aire < 70]
AGUA: [recomendación detallada de 4-6 líneas si agua < 70]
BIODIVERSIDAD: [recomendación detallada de 4-6 líneas si biodiversidad < 70]
SUELO: [recomendación detallada de 4-6 líneas si suelo < 70]

Si una métrica está por encima de 70, NO incluyas esa categoría.
Las recomendaciones deben ser exhaustivas y profesionales, aplicables específicamente a proyectos de tipo {tipo} en contexto latinoamericano."""

    def _parsear_respuesta(self, texto: str) -> Dict[str, str]:
        """
        Parsea la respuesta de Gemini en un diccionario.
        
        Args:
            texto: Respuesta de Gemini
            
        Returns:
            Diccionario con recomendaciones por categoría
        """
        recomendaciones = {}
        lineas = texto.strip().split('\n')
        
        categorias_map = {
            'AIRE': 'aire',
            'AGUA': 'agua',
            'BIODIVERSIDAD': 'biodiversidad',
            'SUELO': 'suelo'
        }
        
        for linea in lineas:
            linea = linea.strip()
            if not linea:
                continue
                
            for cat_upper, cat_lower in categorias_map.items():
                if linea.upper().startswith(cat_upper + ':'):
                    # Extraer el texto después de "CATEGORIA:"
                    recomendacion = linea[len(cat_upper)+1:].strip()
                    if recomendacion:
                        recomendaciones[cat_lower] = recomendacion
                    break
        
        log.debug(f'Recomendaciones parseadas: {list(recomendaciones.keys())}')
        return recomendaciones
    
    def _recomendaciones_fallback(
        self,
        aire: float,
        agua: float,
        biodiv: float,
        suelo: float
    ) -> Dict[str, str]:
        """
        Genera recomendaciones básicas si falla la API de Gemini.
        
        Args:
            aire, agua, biodiv, suelo: Puntuaciones de cada métrica
            
        Returns:
            Diccionario con recomendaciones básicas
        """
        log.warning('Usando recomendaciones fallback (sin IA)')
        recs = {}
        
        if aire < 70:
            recs["aire"] = "Control de polvo mediante riego periódico, uso de barreras vegetales y monitoreo de material particulado (PM10/PM2.5)."
        if agua < 70:
            recs["agua"] = "Implementar sistemas de sedimentación, tratamiento de aguas residuales y manejo de vertimientos según ISO 14001."
        if biodiv < 70:
            recs["biodiversidad"] = "Desarrollar plan de manejo de fauna y flora, rescate y reubicación de especies, y creación de corredores biológicos."
        if suelo < 70:
            recs["suelo"] = "Estabilización de taludes, control de erosión mediante revegetalización y terrazas, y manejo adecuado de material orgánico."
        
        return recs
