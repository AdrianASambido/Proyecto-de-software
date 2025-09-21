from src.core.board_sites import add_site
from src.core.database import db
from src.core.Entities import FeatureFlag
from datetime import datetime, timezone, date

# para agregar datos de prueba a la base de datos se usa "flask seeddb"
def seeds_db():
    print("\n\n==== SEEDING BASE DE DATOS ====")
    
    # Seed para sitios
    site_data = {
        "nombre":"Chichen Itza",
        "descripcion_breve":"Ciudad maya antigua",
        "descripcion_completa":"Chichen Itza fue una gran ciudad precolombina...",
        "ciudad":"Yucatan",
        "provincia":"Yucatan",
        "inauguracion": date(2022, 1, 1),
        "latitud":18.9712,
        "longitud":-88.9856,
        "categoria":"Arqueológico",
        "estado_conservacion":"Bueno",
        "visible":True
    }
    result = add_site(site_data)
    print(result)
    
    # Seed para Feature Flags
    print("\n==== CREANDO FEATURE FLAGS ====")
    
    feature_flags_data = [
        {
            "name": "admin_maintenance_mode",
            "description": "Modo mantenimiento de administración. Cuando está activo, bloquea todas las rutas de administración excepto login y feature flags.",
            "is_enabled": False,
            "maintenance_message": "",
            "last_modified_by": "System",
            "last_modified_at": datetime.now(timezone.utc)
        },
        {
            "name": "portal_maintenance_mode", 
            "description": "Modo mantenimiento del portal web. Cuando está activo, pone el portal público en modo mantenimiento.",
            "is_enabled": False,
            "maintenance_message": "",
            "last_modified_by": "System",
            "last_modified_at": datetime.now(timezone.utc)
        },
        {
            "name": "reviews_enabled",
            "description": "Permitir nuevas reseñas. Cuando está desactivado, oculta/deshabilita la creación de reseñas en el portal.",
            "is_enabled": True,
            "maintenance_message": "",
            "last_modified_by": "System", 
            "last_modified_at": datetime.now(timezone.utc)
        }
    ]
    
    for flag_data in feature_flags_data:
        # Verificar si el flag ya existe
        existing_flag = FeatureFlag.query.filter_by(name=flag_data["name"]).first()
        if not existing_flag:
            flag = FeatureFlag(**flag_data)
            db.session.add(flag)
            print(f"✓ Feature flag '{flag_data['name']}' creado")
        else:
            print(f"⚠ Feature flag '{flag_data['name']}' ya existe")
    
    try:
        db.session.commit()
        print("✓ Feature flags guardados en la base de datos")
    except Exception as e:
        db.session.rollback()
        print(f"✗ Error al guardar feature flags: {e}")
    
    print(f"\n==== SEEDING LISTO ====\n\n")