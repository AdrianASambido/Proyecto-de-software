
from datetime import datetime, timezone, date
from time import sleep
# db
from src.core.database import db
# servicios
from src.core.services.sites import add_site, modify_site
from src.core.services.history import add_site_history
from src.core.services import roles
# entidades
from src.core.Entities import FeatureFlag
from src.core.Entities.site_history import HistoryAction
from src.core.Entities.role import Role
from src.core.Entities.permission import Permission
# para agregar datos de prueba a la base de datos se usa "flask seeddb"
def seeds_db():
    print("\n\n==== SEEDING BASE DE DATOS ====")

    # Seed para Roles y Permisos
    print("\n==== CREANDO ROLES Y PERMISOS ====")
    
    # Crear permisos del módulo de usuarios
    user_permissions = [
        {"name": "user_index", "description": "Listar usuarios", "module": "user", "action": "index"},
        {"name": "user_new", "description": "Crear usuario", "module": "user", "action": "new"},
        {"name": "user_update", "description": "Actualizar usuario", "module": "user", "action": "update"},
        {"name": "user_destroy", "description": "Eliminar usuario", "module": "user", "action": "destroy"},
        {"name": "user_show", "description": "Ver detalle de usuario", "module": "user", "action": "show"},
    ]
    
    # Crear permisos del módulo de sitios
    site_permissions = [
        {"name": "site_index", "description": "Listar sitios", "module": "site", "action": "index"},
        {"name": "site_new", "description": "Crear sitio", "module": "site", "action": "new"},
        {"name": "site_update", "description": "Actualizar sitio", "module": "site", "action": "update"},
        {"name": "site_destroy", "description": "Eliminar sitio", "module": "site", "action": "destroy"},
        {"name": "site_show", "description": "Ver detalle de sitio", "module": "site", "action": "show"},
    ]
    
    # Crear permisos del módulo de tags
    tag_permissions = [
        {"name": "tag_index", "description": "Listar tags", "module": "tag", "action": "index"},
        {"name": "tag_new", "description": "Crear tag", "module": "tag", "action": "new"},
        {"name": "tag_update", "description": "Actualizar tag", "module": "tag", "action": "update"},
        {"name": "tag_destroy", "description": "Eliminar tag", "module": "tag", "action": "destroy"},
        {"name": "tag_show", "description": "Ver detalle de tag", "module": "tag", "action": "show"},
    ]
    
    # Crear permisos del módulo de feature flags
    feature_flag_permissions = [
        {"name": "feature_flag_index", "description": "Listar feature flags", "module": "feature_flag", "action": "index"},
        {"name": "feature_flag_toggle", "description": "Activar/desactivar feature flags", "module": "feature_flag", "action": "toggle"},
    ]
    
    all_permissions = user_permissions + site_permissions + tag_permissions + feature_flag_permissions
    
    for perm_data in all_permissions:
        existing_perm = Permission.query.filter_by(name=perm_data["name"]).first()
        if not existing_perm:
            perm = Permission(**perm_data)
            db.session.add(perm)
            print(f"✓ Permiso '{perm_data['name']}' creado")
        else:
            print(f"⚠ Permiso '{perm_data['name']}' ya existe")
    
    # Crear roles
    roles_data = [
        {
            "name": "Editor",
            "description": "Usuario con permisos de edición limitados"
        },
        {
            "name": "Administrador", 
            "description": "Usuario con todos los permisos del sistema"
        }
    ]
    
    for role_data in roles_data:
        existing_role = Role.query.filter_by(name=role_data["name"]).first()
        if not existing_role:
            role = Role(**role_data)
            db.session.add(role)
            print(f"✓ Rol '{role_data['name']}' creado")
        else:
            print(f"⚠ Rol '{role_data['name']}' ya existe")
    
    try:
        db.session.commit()
        print("✓ Roles y permisos guardados en la base de datos")
    except Exception as e:
        db.session.rollback()
        print(f"✗ Error al guardar roles y permisos: {e}")
    
    # Asignar permisos a roles
    print("\n==== ASIGNANDO PERMISOS A ROLES ====")
    
    # Obtener roles
    editor_role = Role.query.filter_by(name="Editor").first()
    admin_role = Role.query.filter_by(name="Administrador").first()
    
    if editor_role and admin_role:
        # Editor: permisos limitados (solo sitios y tags)
        editor_permissions = site_permissions + tag_permissions
        for perm_data in editor_permissions:
            perm = Permission.query.filter_by(name=perm_data["name"]).first()
            if perm and perm not in editor_role.permissions:
                editor_role.add_permission(perm)
                print(f"✓ Permiso '{perm_data['name']}' asignado a Editor")
        
        # Administrador: todos los permisos
        for perm_data in all_permissions:
            perm = Permission.query.filter_by(name=perm_data["name"]).first()
            if perm and perm not in admin_role.permissions:
                admin_role.add_permission(perm)
                print(f"✓ Permiso '{perm_data['name']}' asignado a Administrador")
        
        try:
            db.session.commit()
            print("✓ Permisos asignados a roles correctamente")
        except Exception as e:
            db.session.rollback()
            print(f"✗ Error al asignar permisos: {e}")

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


    # Seed para sitios
   
   
    print("\n==== CREANDO SITES ====")


    sites_data = [{
        "nombre":"Machu Picchu",
        "descripcion_breve":"Ciudad inca antigua",
        "descripcion_completa":"Machu Picchu es una ciudadela inca situada en las montañas...",
        "ciudad":"Cusco",
        "provincia":"Cusco",
        "inauguracion":2022,
        "latitud":-13.1631,
        "longitud":-72.5450,
        "categoria":"Arqueológico",
        "estado_conservacion":"Bueno",
        "visible":True
    },
   {
        "nombre":"Gran Muralla China",
        "descripcion_breve":"Estructura defensiva antigua",
        "descripcion_completa":"La Gran Muralla China es una serie de fortificaciones...",
        "ciudad":"Beijing",
        "provincia":"Beijing",
        "inauguracion":2022,
        "latitud":40.4319,
        "longitud":116.5704,
        "categoria":"Histórico",
        "estado_conservacion":"Bueno",
        "visible":True
    },
   {
        "nombre":"Taj Mahal",
        "descripcion_breve":"Mausoleo de mármol blanco",
        "descripcion_completa":"El Taj Mahal es un mausoleo ubicado en Agra, India...",
        "ciudad":"Agra",
        "provincia":"Uttar Pradesh",
        "inauguracion":2022,
        "latitud":27.1751,
        "longitud":78.0421,
        "categoria":"Arquitectónico",
        "estado_conservacion":"Malo",
        "visible":True
    }
    ]

    add_site(sites_data[0])
    result = add_site(sites_data[1])

    add_site(sites_data[2])

   


    # sleep(5)
    modify_site(result.id, {
        "nombre":"Chichen Itza",
        "estado_conservacion":"Malo",
        "visible":False
    })

    # sleep(5)
    modify_site(result.id, {
        "estado_conservacion":"Bueno",
        "visible":True
    })

    # sleep(5)
    modify_site(result.id, {
        "latitud":19.8712,
        "longitud":-87.2856,
    })

    # sleep(5)
    modify_site(result.id, {
        "ciudad":"Tuxtla Gutiérrez",
        "provincia":"Chiapas",
    })

    # eliminar efectivamente el site con la funcion que lo maneje al eliminado 
    add_site_history(result.id, HistoryAction.ELIMINAR, 1, None, result, None)


    # sleep(5)
    modify_site(result.id, {
        "nombre":"Chichen Itza",
        "estado_conservacion":"Malo",
        "visible":False
    })

    # sleep(5)
    modify_site(result.id, {
        "estado_conservacion":"Bueno",
        "visible":True
    })

    # sleep(5)
    modify_site(result.id, {
        "latitud":19.8712,
        "longitud":-87.2856,
    })

    # sleep(5)
    modify_site(result.id, {
        "ciudad":"Tuxtla Gutiérrez",
        "provincia":"Chiapas",
    })

    # eliminar efectivamente el site con la funcion que lo maneje al eliminado 
    add_site_history(result.id, HistoryAction.ELIMINAR, 1, None, result, None)




    print(f"\n==== SEEDING LISTO ====\n\n")
