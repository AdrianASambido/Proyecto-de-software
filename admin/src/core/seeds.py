from datetime import datetime, timezone, date
from time import sleep
from src.core.services.sites import add_site
from src.core.Entities.role import user_roles

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
from src.core.Entities.review import Review, ReviewStatus
from src.core.Entities.site import Site
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
            "nombre": "Teatro Colón",
            "descripcion_breve": "Teatro de ópera histórico de Buenos Aires",
            "descripcion_completa": "El Teatro Colón es uno de los teatros de ópera más importantes del mundo. Inaugurado en 1908, es considerado una joya arquitectónica de estilo ecléctico. Su acústica es reconocida internacionalmente y ha recibido a los más grandes artistas de la ópera, el ballet y la música clásica. El edificio cuenta con una impresionante cúpula, salones de lujo y una capacidad para más de 2.400 espectadores.",
            "ciudad": "Buenos Aires",
            "provincia": "Buenos Aires",
            "inauguracion": 1908,
            "latitud": -34.601389,
            "longitud": -58.383611,
            "categoria": "Arquitectónico",
            "estado_conservacion": "Excelente",
            "visible": True,
        },
        {
            "nombre": "Manzana Jesuítica",
            "descripcion_breve": "Complejo histórico jesuítico de Córdoba",
            "descripcion_completa": "La Manzana Jesuítica es un conjunto arquitectónico histórico ubicado en el centro de Córdoba, declarado Patrimonio de la Humanidad por la UNESCO en 2000. Incluye la Universidad Nacional de Córdoba (una de las más antiguas de América), la Iglesia de la Compañía de Jesús, el Colegio Nacional de Monserrat y la Residencia de los jesuitas. Fue construido entre los siglos XVII y XVIII y representa un ejemplo excepcional de la arquitectura colonial española en América.",
            "ciudad": "Córdoba",
            "provincia": "Córdoba",
            "inauguracion": 1613,
            "latitud": -31.420278,
            "longitud": -64.188611,
            "categoria": "Histórico",
            "estado_conservacion": "Bueno",
            "visible": True,
        },
        {
            "nombre": "Ruinas de Quilmes",
            "descripcion_breve": "Sitio arqueológico precolombino en los Valles Calchaquíes",
            "descripcion_completa": "Las Ruinas de Quilmes son los restos de uno de los asentamientos precolombinos más importantes de Argentina. Ubicadas en la provincia de Tucumán, en los Valles Calchaquíes, fueron habitadas por la cultura Quilmes desde el siglo X hasta su destrucción en 1667. El sitio arqueológico muestra una ciudadela construida en terrazas sobre las laderas de las montañas, con más de 5.000 construcciones de piedra. Los Quilmes resistieron durante más de 130 años a los conquistadores españoles antes de ser finalmente derrotados y deportados.",
            "ciudad": "Amaicha del Valle",
            "provincia": "Tucumán",
            "inauguracion": 1000,
            "latitud": -26.466667,
            "longitud": -66.016667,
            "categoria": "Arqueológico",
            "estado_conservacion": "Regular",
            "visible": True,
        },
    ]

    add_site(sites_data[0],1)
    add_site(sites_data[1],1)
    add_site(sites_data[2],1)


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

    # -------------------
    # Crear reseñas de ejemplo
    # -------------------
    print("\n==== CREANDO RESEÑAS DE EJEMPLO ====")

    # Obtener el sitio Machu Picchu y usuarios
    machu_picchu = Site.query.filter_by(nombre="Machu Picchu").first()
    if machu_picchu and u1 and u2 and u3:
        reviews_data = [
            {
                "site_id": machu_picchu.id,
                "user_id": u1.id,
                "calificacion": 5,
                "contenido": "Excelente sitio histórico, muy bien conservado y con vistas impresionantes.",
                "estado": ReviewStatus.APROBADA,
                "motivo_rechazo": None,
            },
            {
                "site_id": machu_picchu.id,
                "user_id": u2.id,
                "calificacion": 4,
                "contenido": "Muy buena experiencia, aunque hay que mejorar la señalización en algunos sectores.",
                "estado": ReviewStatus.APROBADA,
                "motivo_rechazo": None,
            },
            {
                "site_id": machu_picchu.id,
                "user_id": u3.id,
                "calificacion": 3,
                "contenido": "Interesante pero esperaba más información histórica en el lugar.",
                "estado": ReviewStatus.PENDIENTE,
                "motivo_rechazo": None,
            },
            {
                "site_id": machu_picchu.id,
                "user_id": u1.id,
                "calificacion": 1,
                "contenido": "Esto es spam y contenido inapropiado.",
                "estado": ReviewStatus.RECHAZADA,
                "motivo_rechazo": "Contenido inapropiado y no relacionado con el sitio histórico",
            },
            {
                "site_id": machu_picchu.id,
                "user_id": u2.id,
                "calificacion": 5,
                "contenido": "¡Increíble! Una maravilla del mundo que todos deberían visitar.",
                "estado": ReviewStatus.APROBADA,
                "motivo_rechazo": None,
            },
            {
                "site_id": machu_picchu.id,
                "user_id": u3.id,
                "calificacion": 4,
                "contenido": "Muy recomendable, especialmente si se visita temprano en la mañana.",
                "estado": ReviewStatus.PENDIENTE,
                "motivo_rechazo": None,
            },
        ]

        for review_data in reviews_data:
            existing_review = Review.query.filter_by(
                site_id=review_data["site_id"],
                user_id=review_data["user_id"],
                contenido=review_data["contenido"]
            ).first()

            if not existing_review:
                review = Review(**review_data)
                db.session.add(review)
                print(f"✓ Reseña creada: {review_data['calificacion']} estrellas - Estado: {review_data['estado'].value}")
            else:
                print(f"⚠ Reseña ya existe para usuario {review_data['user_id']}")

        db.session.commit()
        print("✓ Todas las reseñas guardadas en la base de datos")
    else:
        print("⚠ No se pudieron crear reseñas: falta el sitio Machu Picchu o usuarios")

    print(f"\n==== SEEDING LISTO ====\n\n")
