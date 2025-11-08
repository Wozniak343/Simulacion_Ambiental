"""
Script de pruebas básicas para el Simulador Ambiental.
Ejecutar: python test_basico.py
"""
import sys
from constants import TIPOS_PROYECTO, INTENSIDAD_MIN, INTENSIDAD_MAX
from models import Project, Impacto
from crud_service import init, crear_proyecto, obtener_proyecto, listar_proyectos, eliminar_proyecto, simular_proyecto

def test_constantes():
    """Prueba que las constantes estén definidas correctamente."""
    print("Test 1: Constantes...")
    assert len(TIPOS_PROYECTO) == 3, "Deben haber 3 tipos de proyecto"
    assert INTENSIDAD_MIN == 1, "Intensidad mínima debe ser 1"
    assert INTENSIDAD_MAX == 10, "Intensidad máxima debe ser 10"
    print("✓ Constantes OK")

def test_modelos():
    """Prueba que los modelos se puedan instanciar."""
    print("\nTest 2: Modelos...")
    p = Project(
        id="TEST-001",
        nombre="Proyecto de Prueba",
        tipo="construccion",
        area_ha=5.0,
        duracion_meses=12,
        intensidad=5
    )
    assert p.id == "TEST-001", "ID del proyecto debe coincidir"
    assert p.intensidad == 5, "Intensidad debe ser 5"
    print("✓ Modelos OK")

def test_validaciones():
    """Prueba que las validaciones funcionen."""
    print("\nTest 3: Validaciones...")
    init()
    
    # Validación: ID vacío
    try:
        crear_proyecto({"id": "", "nombre": "Test", "tipo": "construccion", 
                       "area_ha": 1, "duracion_meses": 1, "intensidad": 5})
        print("✗ FALLÓ: Debió rechazar ID vacío")
        sys.exit(1)
    except ValueError:
        print("  ✓ Rechaza ID vacío")
    
    # Validación: Tipo inválido
    try:
        crear_proyecto({"id": "T1", "nombre": "Test", "tipo": "invalido", 
                       "area_ha": 1, "duracion_meses": 1, "intensidad": 5})
        print("✗ FALLÓ: Debió rechazar tipo inválido")
        sys.exit(1)
    except ValueError:
        print("  ✓ Rechaza tipo inválido")
    
    # Validación: Intensidad fuera de rango
    try:
        crear_proyecto({"id": "T1", "nombre": "Test", "tipo": "construccion", 
                       "area_ha": 1, "duracion_meses": 1, "intensidad": 15})
        print("✗ FALLÓ: Debió rechazar intensidad fuera de rango")
        sys.exit(1)
    except ValueError:
        print("  ✓ Rechaza intensidad fuera de rango")
    
    print("✓ Validaciones OK")

def test_crud_basico():
    """Prueba operaciones CRUD básicas."""
    print("\nTest 4: CRUD básico...")
    init()
    
    # Limpiar test anterior si existe
    try:
        eliminar_proyecto("TEST-CRUD")
    except:
        pass
    
    # Crear
    proyecto = crear_proyecto({
        "id": "TEST-CRUD",
        "nombre": "Proyecto CRUD Test",
        "tipo": "agricultura",
        "area_ha": 10.0,
        "duracion_meses": 24,
        "ubicacion": "Test Location",
        "intensidad": 3
    })
    assert proyecto is not None, "Proyecto debe crearse"
    print("  ✓ Crear proyecto")
    
    # Leer
    p = obtener_proyecto("TEST-CRUD")
    assert p is not None, "Proyecto debe existir"
    assert p.nombre == "Proyecto CRUD Test", "Nombre debe coincidir"
    print("  ✓ Leer proyecto")
    
    # Listar
    proyectos = listar_proyectos()
    assert len(proyectos) > 0, "Debe haber al menos un proyecto"
    print("  ✓ Listar proyectos")
    
    # Simular
    impacto = simular_proyecto("TEST-CRUD")
    assert impacto is not None, "Simulación debe devolver resultado"
    assert 0 <= impacto.riesgo_total <= 100, "Riesgo debe estar entre 0 y 100"
    print("  ✓ Simular impacto")
    
    # Eliminar
    eliminado = eliminar_proyecto("TEST-CRUD")
    assert eliminado == True, "Proyecto debe eliminarse"
    print("  ✓ Eliminar proyecto")
    
    print("✓ CRUD básico OK")

def test_simulacion():
    """Prueba el motor de simulación."""
    print("\nTest 5: Motor de simulación...")
    init()
    
    # Limpiar test anterior si existe
    try:
        eliminar_proyecto("TEST-SIM")
    except:
        pass
    
    # Crear proyecto para simular
    crear_proyecto({
        "id": "TEST-SIM",
        "nombre": "Test Simulación",
        "tipo": "mineria",
        "area_ha": 50.0,
        "duracion_meses": 36,
        "intensidad": 8
    })
    
    impacto = simular_proyecto("TEST-SIM")
    
    # Verificar estructura
    assert hasattr(impacto, 'calidad_aire'), "Debe tener calidad_aire"
    assert hasattr(impacto, 'calidad_agua'), "Debe tener calidad_agua"
    assert hasattr(impacto, 'biodiversidad'), "Debe tener biodiversidad"
    assert hasattr(impacto, 'uso_suelo'), "Debe tener uso_suelo"
    assert hasattr(impacto, 'riesgo_total'), "Debe tener riesgo_total"
    
    # Verificar rangos
    assert 0 <= impacto.calidad_aire <= 100, "Calidad aire en rango"
    assert 0 <= impacto.calidad_agua <= 100, "Calidad agua en rango"
    assert 0 <= impacto.biodiversidad <= 100, "Biodiversidad en rango"
    assert 0 <= impacto.uso_suelo <= 100, "Uso suelo en rango"
    
    print("  ✓ Estructura correcta")
    print("  ✓ Rangos válidos")
    print(f"  → Riesgo calculado: {impacto.riesgo_total:.1f}%")
    
    # Limpiar
    eliminar_proyecto("TEST-SIM")
    
    print("✓ Motor de simulación OK")

def main():
    """Ejecuta todos los tests."""
    print("=" * 60)
    print("PRUEBAS BÁSICAS - SIMULADOR AMBIENTAL")
    print("=" * 60)
    
    try:
        test_constantes()
        test_modelos()
        test_validaciones()
        test_crud_basico()
        test_simulacion()
        
        print("\n" + "=" * 60)
        print("✓ TODOS LOS TESTS PASARON EXITOSAMENTE")
        print("=" * 60)
        return 0
        
    except AssertionError as e:
        print(f"\n✗ TEST FALLÓ: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ ERROR INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
