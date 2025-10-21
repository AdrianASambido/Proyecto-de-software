from datetime import datetime, timezone, date
from time import sleep


from src.core.services.sites import add_site

from datetime import datetime, timezone, date
from time import sleep

from src.core.Entities.role import user_roles

from src.core.services.sites import add_site

from datetime import datetime, timezone, date
from time import sleep

from geoalchemy2 import WKTElement
# db
from src.core.database import db
# servicios
from src.core.services.sites import add_site, modify_site
from src.core.services.history import add_site_history
from src.core.services import roles
from src.core.services.users import add_user
# entidades
from src.core.Entities import FeatureFlag
from src.core.Entities.site_history import HistoryAction
from src.core.Entities.role import Role
from src.core.Entities.permission import Permission
from src.core.Entities.user import User
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
        {"name": "site_export", "description": "Exportar sitios", "module": "site", "action": "export"},
        {"name": "site_history", "description": "Ver historial de sitios", "module": "site", "action": "history"},
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

    # permisos para las reseñas
    review_permissions = [
        {"name": "review_index", "description": "Listar reseñas", "module": "review", "action": "index"},
        {"name": "review_show", "description": "Ver detalle de reseña", "module": "review", "action": "show"},
        {"name": "review_approve", "description": "Aprobar reseña", "module": "review", "action": "approve"},
        {"name": "review_reject", "description": "Rechazar reseña", "module": "review", "action": "reject"},
        {"name": "review_destroy", "description": "Eliminar reseña", "module": "review", "action": "destroy"},
    ]

    all_permissions = user_permissions + site_permissions + tag_permissions + feature_flag_permissions + review_permissions
    
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
        },
        {
            "name": "Usuario Público",
            "description": "Usuario con permisos muy limitados"
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
        # Editor: permisos limitados (solo sitios y tags) sin eliminacion de sitios, moderacion de resenias
        editor_permissions = site_permissions + tag_permissions + review_permissions
        for perm_data in editor_permissions:
            perm = Permission.query.filter_by(name=perm_data["name"]).first()
            if perm and perm not in editor_role.permissions and (perm.name != "site_destroy") and (perm.name != "site_export"):
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
            "last_modified_at": datetime.now(timezone.utc),
        },
        {
            "name": "portal_maintenance_mode",
            "description": "Modo mantenimiento del portal web. Cuando está activo, pone el portal público en modo mantenimiento.",
            "is_enabled": False,
            "maintenance_message": "",
            "last_modified_by": "System",
            "last_modified_at": datetime.now(timezone.utc),
        },
        {
            "name": "reviews_enabled",
            "description": "Permitir nuevas reseñas. Cuando está desactivado, oculta/deshabilita la creación de reseñas en el portal.",
            "is_enabled": True,
            "maintenance_message": "",
            "last_modified_by": "System",
            "last_modified_at": datetime.now(timezone.utc),
        },
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

    # crear usuarios (sin commit)
    u1 = add_user({
        "email": "user1@gmail.com",
        "nombre": "Jose",
        "username": "joseuser",
        "apellido": "Perez",
        "contraseña": "jose123",
       
    })
    u2 = add_user({
        "email": "user2@gmail.com",
        "nombre": "Pedrito",
        "username": "pedrouser",
        "apellido": "Martinez",
        "contraseña": "pedro123"
    })
    u3 = add_user({
        "email": "user3@gmail.com",
        "nombre": "Juan",
        "username": "juanuser",
        "apellido": "Soria",
        "contraseña": "juan324"
    })

    # obtener roles
    admin_role = Role.query.filter_by(name="Administrador").first()
    editor_role = Role.query.filter_by(name="Editor").first()

    # asignar roles (antes del commit)
    u1.roles.append(admin_role)
    u2.roles.append(editor_role)
    u3.roles.append(editor_role)
    system_admin = add_user({
    "email": "admin@system.com",
    "nombre": "System",
    "username": "sysadmin",
    "apellido": "Administrator",
    "contraseña": "admin123"
    })

    # marcarlo como system admin
    system_admin.is_system_admin = True

    # opcional: asignarle también el rol "Administrador"
    admin_role = Role.query.filter_by(name="Administrador").first()
    if admin_role:
        system_admin.roles.append(admin_role)

    # agregar a la sesión
    db.session.add(system_admin)
    # un solo commit al final
    db.session.commit()

    print("\n==== CREANDO SITES ====")

    sites_data = [
        {
            "nombre": "Machu Picchu",
            "descripcion_breve": "Ciudad inca antigua",
            "descripcion_completa": "Machu Picchu es una ciudadela inca situada en las montañas...",
            "ciudad": "Cusco",
            "provincia": "Cusco",
            "inauguracion": 2022,
            "latitud": -13.163068,
            "longitud": -72.545128,
           
            "categoria": "Arqueológico",
            "estado_conservacion": "Bueno",
            "visible": True,
        },
        {
            "nombre": "Gran Muralla China",
            "descripcion_breve": "Estructura defensiva antigua",
            "descripcion_completa": "La Gran Muralla China es una serie de fortificaciones...",
            "ciudad": "Beijing",
            "provincia": "Beijing",
            "inauguracion": 2022,
            "latitud": 40.431908,
            "longitud": 116.570374,
            
            "categoria": "Histórico",
            "estado_conservacion": "Bueno",
            "visible": True,
        },
        {
            "nombre": "Taj Mahal",
            "descripcion_breve": "Mausoleo de mármol blanco",
            "descripcion_completa": "El Taj Mahal es un mausoleo ubicado en Agra, India...",
            "ciudad": "Agra",
            "provincia": "Uttar Pradesh",
            "inauguracion": 2022,
           "latitud": 27.175015,
              "longitud": 78.042155,
           
            "categoria": "Arquitectónico",
            "estado_conservacion": "Malo",
            "visible": True,
        },
    ]

    add_site(sites_data[0],1)


     # -------------------
    # 1. Crear etiquetas
    # -------------------
    print("\n==== CREANDO ETIQUETAS ====")
    # 26 etiquetas
    tags_data = [
        "Aventura",
        "Cultural",
        "Familiar",
        "Ecológico",
        "Histórico",
        "Gastronómico",
        "Playa",
        "Montaña",
        "Urbano",
        "Rural",
        "Deportes",
        "Relajación",
        "Lujo",
        "Económico",
        "Romántico",
        "Fotografía",
        "Vida Nocturna",
        "Compras",
        "Arte y Música",
        "Naturaleza",
        "Religioso",
        "Educativo",
        "Salud y Bienestar",
        "Tecnológico",
        "Voluntariado",
        "Festividades"
    ]
    tags_objs = []

    # crear etiquetas llamando a add_tag
    from src.core.services.tags import add_tag
    for tag_name in tags_data:
        tag = add_tag({"nombre": tag_name})
        tags_objs.append(tag)
        print(f"✓ Etiqueta '{tag_name}' creada")

    db.session.commit()
    print("✓ Todas las etiquetas guardadas en la base de datos")

    print(f"\n==== SEEDING LISTO ====\n\n")
