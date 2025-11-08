# Ejemplos de Uso - Simulador Ambiental

## Ejemplos CLI

### Crear un Proyecto de Construcción

```
$ python cli.py

Opción: 1
id (obligatorio): CONST-001
nombre (obligatorio): Edificio Corporativo Centro
tipo [construccion|agricultura|mineria] (obligatorio): construccion
area_ha (obligatorio): 2.5
duracion_meses (obligatorio): 18
ubicacion (Enter=): Zona Urbana Centro
intensidad (1-10) (Enter=5): 6

✓ Proyecto CONST-001 creado exitosamente
```

### Simular Impacto

```
Opción: 6
id (obligatorio): CONST-001

{
  "proyecto_id": "CONST-001",
  "scores": {
    "aire": 78.5,
    "agua": 82.3,
    "biodiversidad": 74.1,
    "uso_suelo": 71.2
  },
  "riesgo_total": 23.5,
  "recomendaciones": {
    "uso_suelo": "Estabilización de taludes y revegetalización."
  }
}
```

## Ejemplos GUI

### Crear Proyecto desde la Interfaz

1. Abrir la aplicación: `python app.py`
2. Llenar el formulario en la pestaña "Proyectos":
   - ID: `MIN-001`
   - Nombre: `Extracción Oro Norte`
   - Tipo: `mineria`
   - Área: `50.0` ha
   - Duración: `36` meses
   - Ubicación: `Región Norte, Zona 5`
   - Intensidad: `8`
3. Click en "Crear"

### Simular desde GUI

1. Seleccionar proyecto en el panel lateral
2. Click en "Simular Impacto"
3. Ver resultados en la pestaña "Simulación"

## Ejemplos Programáticos

### Uso de la API Interna

```python
from crud_service import init, crear_proyecto, simular_proyecto

# Inicializar
init()

# Crear proyecto
proyecto_data = {
    "id": "AGR-001",
    "nombre": "Cultivo de Café Orgánico",
    "tipo": "agricultura",
    "area_ha": 15.0,
    "duracion_meses": 60,
    "ubicacion": "Montañas del Sur",
    "intensidad": 4
}

proyecto = crear_proyecto(proyecto_data)
print(f"Proyecto creado: {proyecto.id}")

# Simular impacto
impacto = simular_proyecto("AGR-001")
print(f"Riesgo total: {impacto.riesgo_total:.1f}%")
print(f"Calidad del aire: {impacto.calidad_aire:.1f}")
```

## Casos de Uso Reales

### Caso 1: Evaluación de Proyecto de Construcción

**Contexto**: Una empresa constructora necesita evaluar el impacto ambiental de un nuevo complejo residencial.

**Datos del Proyecto**:
- Tipo: Construcción
- Área: 5 hectáreas
- Duración: 24 meses
- Intensidad: 7 (alta densidad)

**Resultado Esperado**:
- Riesgo total: ~30-35%
- Recomendaciones en: aire, suelo
- Acciones: Control de polvo, estabilización de suelo

### Caso 2: Evaluación de Proyecto Minero

**Contexto**: Evaluación de impacto de extracción minera en zona protegida.

**Datos del Proyecto**:
- Tipo: Minería
- Área: 100 hectáreas
- Duración: 48 meses
- Intensidad: 9 (muy alta)

**Resultado Esperado**:
- Riesgo total: ~55-65%
- Recomendaciones en: todas las categorías
- Acciones: Plan integral de mitigación requerido

### Caso 3: Evaluación de Proyecto Agrícola

**Contexto**: Cultivo extensivo con prácticas sostenibles.

**Datos del Proyecto**:
- Tipo: Agricultura
- Área: 20 hectáreas
- Duración: 36 meses
- Intensidad: 3 (bajo impacto)

**Resultado Esperado**:
- Riesgo total: ~15-20%
- Pocas o ninguna recomendación
- Proyecto ambientalmente viable

## Validaciones y Errores Comunes

### Error: ID Duplicado

```
$ python cli.py
Opción: 1
id: CONST-001
...
Error de validación: Ya existe un proyecto con ID: CONST-001
```

**Solución**: Usar un ID único para cada proyecto.

### Error: Tipo Inválido

```
id: TEST-001
tipo [construccion|agricultura|mineria]: industrial
...
Error de validación: Tipo de proyecto inválido. Debe ser uno de: construccion, agricultura, mineria
```

**Solución**: Usar uno de los tipos válidos.

### Error: Intensidad Fuera de Rango

```
intensidad (1-10): 15
...
Error de validación: La intensidad debe estar entre 1 y 10
```

**Solución**: Proporcionar un valor entre 1 y 10.

### Error: Área Inválida

```
area_ha: -5
...
Error de validación: El área debe ser mayor a 0.01 hectáreas
```

**Solución**: Proporcionar un valor positivo.

## Tips y Mejores Prácticas

1. **IDs Descriptivos**: Use prefijos como CONST-, MIN-, AGR- para mejor organización
2. **Intensidad Realista**: Base la intensidad en estudios preliminares reales
3. **Ubicación Detallada**: Incluya coordenadas o referencias claras
4. **Simulaciones Múltiples**: Compare diferentes escenarios ajustando la intensidad
5. **Documentar Recomendaciones**: Exporte y guarde los resultados de simulación

## Integración con Flujos de Trabajo

### Flujo de Evaluación Ambiental Típico

1. **Recopilación de Datos** → Llenar formulario con datos del proyecto
2. **Simulación Inicial** → Ejecutar primera simulación
3. **Análisis de Resultados** → Revisar métricas y recomendaciones
4. **Ajustes** → Modificar parámetros (reducir intensidad, área, etc.)
5. **Re-simulación** → Comparar resultados
6. **Decisión** → Aprobar o solicitar más mitigaciones

## Mantenimiento de Datos

### Backup del CSV

```powershell
# Windows PowerShell
Copy-Item proyectos.csv proyectos_backup_$(Get-Date -Format 'yyyyMMdd').csv
```

### Limpieza de Proyectos Antiguos

Use la opción "5) Eliminar proyecto" en CLI o el botón "Eliminar" en GUI para proyectos que ya no necesita.
