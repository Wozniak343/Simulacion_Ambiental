# Simulador de Impacto Ambiental con IA

Sistema avanzado de gestión y simulación de proyectos para evaluar su impacto ambiental usando **Inteligencia Artificial** con Google Gemini.

## Descripción

Sistema profesional que permite crear, gestionar y simular el impacto ambiental de proyectos de construcción, minería y agricultura. Utiliza **Google Gemini AI** para calcular métricas ambientales contextualizadas y generar recomendaciones técnicas detalladas.

## Características Principales

- **Cálculo con IA**: Métricas ambientales generadas por Google Gemini
- **Recomendaciones Inteligentes**: Sugerencias técnicas detalladas con normativas
- **Sistema de Fallback**: Garantiza funcionamiento sin conexión a internet
- **Gestión CRUD Completa**: Crear, leer, actualizar y eliminar proyectos
- **Doble Interfaz**: GUI moderna (Tkinter) y CLI para usuarios avanzados
- **Persistencia**: Almacenamiento en CSV con manejo robusto de errores
- **Logging Completo**: Trazabilidad de todas las operaciones
- **Validaciones Exhaustivas**: Datos consistentes y confiables

## Tipos de Proyectos

1. **Construcción** - Obras civiles, edificaciones, infraestructura
2. **Minería** - Explotación de recursos minerales, canteras
3. **Agricultura** - Proyectos agrícolas, cultivos, ganadería

## Estructura del Proyecto

```
Ambiental/
├── src/                          # Código fuente principal
│   ├── __init__.py              # Inicialización del paquete
│   ├── models.py                # Modelos de datos (Project, Impacto)
│   ├── constants.py             # Constantes y configuración
│   ├── logger_base.py           # Sistema de logging
│   ├── store.py                 # Capa de persistencia (CSV)
│   ├── crud_service.py          # Lógica de negocio y CRUD
│   ├── simulation.py            # Motor de simulación ambiental
│   └── gemini_service.py        # Integración con Google Gemini AI
│
├── tests/                        # Pruebas y scripts de validación
│   ├── __init__.py
│   ├── test_basico.py           # Pruebas básicas del sistema
│   ├── test_gemini.py           # Prueba de integración con Gemini
│   ├── test_calculo_ia.py       # Prueba de cálculo con IA
│   └── test_recomendaciones_largas.py  # Prueba de recomendaciones detalladas
│
├── docs/                         # Documentación
│   ├── README_OLD.md            # Documentación original
│   ├── INTEGRACION_GEMINI.md    # Guía de integración con IA
│   ├── EJEMPLOS.md              # Ejemplos de uso
│   ├── MEJORAS.md               # Registro de mejoras
│   └── RESUMEN_FINAL.md         # Resumen del proyecto
│
├── data/                         # Datos y logs
│   ├── proyectos.csv            # Base de datos de proyectos
│   └── capa_datos.log           # Archivo de logs
│
├── app.py                        # Aplicación GUI con Tkinter
├── cli.py                        # Interfaz de línea de comandos
├── .gitignore                   # Archivos ignorados por Git
├── README.md                    # Este archivo
└── venv/                        # Entorno virtual (no incluido en Git)
```

## Instalación

### Requisitos Previos

- Python 3.7 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone <url-del-repositorio>
cd Ambiental
```

2. **Crear entorno virtual (recomendado)**
```bash
python -m venv venv
```

3. **Activar el entorno virtual**
- Windows:
  ```bash
  venv\Scripts\activate
  ```
- Linux/Mac:
  ```bash
  source venv/bin/activate
  ```

4. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

O manualmente:
```bash
pip install google-generativeai
```

5. **Configurar API Key de Gemini**
- Editar `src/constants.py` y agregar tu API Key:
```python
GEMINI_API_KEY = "tu-api-key-aqui"
```

## Uso

### Interfaz Gráfica (GUI)

```bash
python app.py
```

La aplicación GUI ofrece:
- Formulario intuitivo para crear proyectos
- Tabla con lista de proyectos existentes
- Botones para ver detalles, simular, editar y eliminar
- Ventanas emergentes con resultados de simulación
- Diseño moderno y profesional

### Interfaz de Línea de Comandos (CLI)

```bash
python cli.py
```

Opciones del menú CLI:
1. Crear proyecto
2. Listar proyectos
3. Ver detalles de proyecto
4. Actualizar proyecto
5. Eliminar proyecto
6. Simular impacto ambiental
0. Salir

### Ejecutar Pruebas

```bash
# Prueba básica del sistema
python -m tests.test_basico

# Prueba de integración con Gemini
python -m tests.test_gemini

# Prueba de cálculo con IA
python -m tests.test_calculo_ia

# Prueba de recomendaciones detalladas
python -m tests.test_recomendaciones_largas
```

## Funcionamiento del Sistema IA

### Cálculo de Métricas con IA

El sistema utiliza **Google Gemini** para:

1. **Analizar el contexto del proyecto**: tipo, área, duración, intensidad, ubicación
2. **Calcular métricas ambientales**:
   - Calidad del Aire (0-100)
   - Calidad del Agua (0-100)
   - Biodiversidad (0-100)
   - Uso del Suelo (0-100)
   - Riesgo Total (0-100%)

3. **Generar recomendaciones detalladas** con:
   - Medidas técnicas cuantificables
   - Tecnologías y equipos específicos
   - Referencias normativas (ISO, leyes locales)
   - Cronogramas de implementación
   - Indicadores de éxito medibles

### Sistema de Fallback Dual

**Nivel 1**: Gemini AI (modo ideal)
- Cálculos contextualizados
- Recomendaciones técnicas exhaustivas

**Nivel 2**: Fórmulas matemáticas (fallback de cálculo)
- Algoritmos basados en factores tipo de proyecto
- Ajustes por escala, área y duración

**Nivel 3**: Recomendaciones básicas (fallback total)
- Recomendaciones predefinidas detalladas
- Aplican cuando API no está disponible

## Métricas Ambientales

### Calidad del Aire
- Material particulado (PM10/PM2.5)
- Emisiones de gases
- Polvo en suspensión

### Calidad del Agua
- DBO/DQO
- Sólidos suspendidos
- pH y contaminantes

### Biodiversidad
- Impacto en flora nativa
- Afectación de fauna
- Corredores biológicos

### Uso del Suelo
- Erosión y estabilidad
- Compactación
- Pérdida de suelo orgánico

## Niveles de Riesgo

- **0-30%**: 🟢 Riesgo Bajo
- **30-60%**: 🟡 Riesgo Moderado
- **60-100%**: 🔴 Riesgo Alto

## Validaciones

El sistema valida automáticamente:
- ID único del proyecto (no vacío)
- Nombre del proyecto (no vacío)
- Tipo válido (construccion, mineria, agricultura)
- Área: ≥ 0.1 hectáreas
- Duración: ≥ 1 mes
- Intensidad: 1-10 (escala numérica)

## Configuración Avanzada

### constants.py

Archivo de configuración central:
- `GEMINI_API_KEY`: API key de Google Gemini
- `TIPOS_PROYECTO`: Tipos de proyectos permitidos
- `INTENSIDAD_MIN/MAX`: Rango de intensidad
- `AREA_MIN`: Área mínima en hectáreas
- `DURACION_MIN`: Duración mínima en meses
- `UMBRAL_RECOMENDACION`: Umbral para generar recomendaciones

### Archivos de Log

Los logs se guardan en `data/capa_datos.log` con:
- Timestamp de cada operación
- Nivel de log (DEBUG, INFO, WARNING, ERROR)
- Nombre de archivo y línea de código
- Mensaje descriptivo

## Tecnologías Utilizadas

- **Python 3.7+**: Lenguaje principal
- **Tkinter**: Interfaz gráfica
- **Google Gemini AI**: Inteligencia artificial
- **google-generativeai**: SDK oficial de Google
- **CSV**: Persistencia de datos
- **Logging**: Trazabilidad del sistema
- **Dataclasses**: Modelos de datos

## Contribución

Este proyecto está en desarrollo activo. Para contribuir:

1. Fork del repositorio
2. Crear rama feature (`git checkout -b feature/NuevaCaracteristica`)
3. Commit de cambios (`git commit -m 'Agrega nueva característica'`)
4. Push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Crear Pull Request

## Documentación Adicional

- **[INTEGRACION_GEMINI.md](docs/INTEGRACION_GEMINI.md)**: Guía completa de integración con IA
- **[EJEMPLOS.md](docs/EJEMPLOS.md)**: Casos de uso y ejemplos prácticos
- **[MEJORAS.md](docs/MEJORAS.md)**: Historial de mejoras implementadas
- **[RESUMEN_FINAL.md](docs/RESUMEN_FINAL.md)**: Resumen técnico del proyecto

## Licencia

Proyecto educativo - Libre uso con atribución

## Contacto

Para preguntas, sugerencias o reportes de errores, crear un issue en el repositorio.

---

**Versión**: 2.0.0 con IA  
**Última actualización**: Noviembre 2025  
**Estado**: Producción ✓
