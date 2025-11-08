# Simulador de Impacto Ambiental

Sistema de gestión y simulación de proyectos para evaluar su impacto ambiental en construcción, minería y agricultura.

## Descripción

Este proyecto permite crear, gestionar y simular el impacto ambiental de diferentes tipos de proyectos. El simulador calcula métricas como calidad del aire, agua, biodiversidad y uso del suelo, proporcionando un análisis de riesgo y recomendaciones de mitigación.

## Características

- **Gestión completa de proyectos** (CRUD)
- **Simulación de impacto ambiental** con métricas detalladas
- **Interfaz gráfica (GUI)** moderna con Tkinter
- **Interfaz de línea de comandos (CLI)** para usuarios avanzados
- **Persistencia de datos** en formato CSV
- **Visualización de resultados** con gráficos de barras
- **Sistema de logging** para trazabilidad
- **Diseño oscuro/claro** adaptable

## Tipos de Proyectos Soportados

1. **Construcción** - Obras civiles y edificaciones
2. **Minería** - Explotación de recursos minerales
3. **Agricultura** - Proyectos agrícolas y cultivos

## Estructura del Proyecto

```
Ambiental/
├── app.py              # Aplicación GUI principal con Tkinter
├── cli.py              # Interfaz de línea de comandos
├── models.py           # Modelos de datos (Project, Impacto)
├── crud_service.py     # Lógica de negocio y operaciones CRUD
├── simulation.py       # Motor de simulación de impacto ambiental
├── store.py            # Capa de persistencia (CSV)
├── logger_base.py      # Configuración del sistema de logging
├── constants.py        # Constantes y configuración global
├── proyectos.csv       # Base de datos de proyectos
├── README.md           # Documentación principal
├── MEJORAS.md          # Registro de mejoras realizadas
├── EJEMPLOS.md         # Ejemplos de uso y casos reales
├── .gitignore          # Archivos ignorados por Git
└── __pycache__/        # Archivos Python compilados
```

## Instalación

### Requisitos

- Python 3.7 o superior
- Tkinter (incluido en la mayoría de distribuciones de Python)

### Dependencias

No se requieren dependencias externas adicionales. El proyecto utiliza solo bibliotecas estándar de Python:
- `tkinter` - Interfaz gráfica
- `csv` - Manejo de datos
- `dataclasses` - Modelos de datos
- `logging` - Sistema de registro

### Instalación

```bash
# Clonar o descargar el proyecto
cd Ambiental
```

## Uso

### Interfaz Gráfica (GUI)

```bash
python app.py
```

La aplicación GUI ofrece:
- **Panel lateral** con listado de proyectos
- **Formularios** para crear y editar proyectos
- **Visualización de simulaciones** con gráficos
- **Pestañas** para separar formularios y resultados

#### Funcionalidades GUI:
- Crear nuevo proyecto
- Editar proyecto existente
- Eliminar proyecto
- Actualizar listado
- Simular impacto ambiental
- Visualizar resultados con gráficos

### Interfaz de Línea de Comandos (CLI)

```bash
python cli.py
```

Menú disponible:
```
1) Crear proyecto
2) Listar proyectos
3) Ver proyecto
4) Actualizar proyecto
5) Eliminar proyecto
6) Simular impacto
0) Salir
```

## Simulación de Impacto

El simulador evalúa cuatro dimensiones ambientales:

### Métricas Evaluadas

| Métrica | Descripción | Rango |
|---------|-------------|-------|
| **Calidad del Aire** | Emisiones y material particulado | 0-100 |
| **Calidad del Agua** | Contaminación hídrica y vertimientos | 0-100 |
| **Biodiversidad** | Impacto en flora y fauna local | 0-100 |
| **Uso del Suelo** | Degradación y erosión del terreno | 0-100 |

*Nota: 100 es el valor óptimo (menor impacto), 0 es el peor (mayor impacto)*

### Factores de Cálculo

El algoritmo de simulación considera:

- **Tipo de proyecto** - Factores base según construcción/minería/agricultura
- **Área del proyecto** - Hectáreas afectadas (escala logarítmica)
- **Duración** - Meses de ejecución
- **Intensidad** - Nivel de impacto del 1 al 10

### Recomendaciones Automáticas

Si alguna métrica cae por debajo de 70, el sistema genera recomendaciones:

- **Aire**: Control de polvo/PM y riego de vías
- **Agua**: Sedimentadores y manejo de vertimientos (ISO 14001)
- **Biodiversidad**: Plan de manejo de fauna/flora y reubicación
- **Suelo**: Estabilización de taludes y revegetalización

## Estructura de Datos

### Proyecto (Project)

```python
{
    "id": "P001",
    "nombre": "Edificio Corporativo",
    "tipo": "construccion",  # construccion|mineria|agricultura
    "area_ha": 2.5,
    "duracion_meses": 18,
    "ubicacion": "Zona Industrial Norte",
    "intensidad": 6  # 1-10
}
```

### Impacto

```python
{
    "proyecto_id": "P001",
    "calidad_aire": 75.3,
    "calidad_agua": 82.1,
    "biodiversidad": 68.9,
    "uso_suelo": 71.2,
    "riesgo_total": 31.2,  # Porcentaje de riesgo (0-100)
    "recomendaciones": {
        "biodiversidad": "Plan de manejo de fauna/flora..."
    }
}
```

## Capturas de Pantalla

### GUI Principal
- Panel lateral oscuro con listado de proyectos
- Formulario de creación con validaciones
- Visualización de métricas con gráficos de barras
- Recomendaciones de mitigación

### CLI
- Menú interactivo en consola
- Operaciones CRUD simplificadas
- Visualización de datos en formato texto

## Sistema de Logging

El proyecto incluye un sistema de logging completo que registra:

- Operaciones exitosas
- Advertencias (IDs duplicados, proyectos no encontrados)
- Errores (validación de datos, simulaciones fallidas)
- Debug (detalles de cálculos y operaciones)

Los logs facilitan la trazabilidad y depuración del sistema.

## Configuración

### Archivo de Datos

Los proyectos se almacenan en `proyectos.csv` con el siguiente formato:

```csv
id,nombre,tipo,area_ha,duracion_meses,ubicacion,intensidad
P001,Edificio Corporativo,construccion,2.5,18,Zona Industrial,6
```

El archivo se crea automáticamente en el primer uso.

## Pruebas

El proyecto incluye un script de pruebas básicas:

```bash
python test_basico.py
```

Las pruebas verifican:
- Importación correcta de módulos
- Validaciones de datos
- Operaciones CRUD
- Motor de simulación
- Rangos de valores

## Contribuciones

Este es un proyecto Work In Progress (WIP). Áreas de mejora futuras:

- [ ] Validación avanzada de datos de entrada
- [ ] Exportación de reportes en PDF
- [ ] Gráficos más avanzados (líneas de tendencia, comparativas)
- [ ] Base de datos SQLite en lugar de CSV
- [ ] API REST para integración con otros sistemas
- [ ] Tests unitarios
- [ ] Soporte para múltiples idiomas
- [ ] Dashboard con estadísticas generales

## Licencia

Este proyecto es de código abierto y está disponible para uso educativo y de investigación.

## Autor

Desarrollado como herramienta de análisis de impacto ambiental para proyectos de construcción, minería y agricultura.

---

**Estado del Proyecto**: Work In Progress (WIP)

**Versión**: 1.0.0

**Última Actualización**: Noviembre 2025
