from datetime import datetime, timezone, date
from time import sleep


from src.core.services.sites import add_site

from datetime import datetime, timezone, date
from time import sleep


# db
from src.core.database import db

# servicios
from src.core.services.sites import add_site, modify_site
from src.core.services.history import add_site_history
from src.core.services.users import add_user

# entidades
from src.core.Entities import FeatureFlag
from src.core.Entities.site_history import HistoryAction


# para agregar datos de prueba a la base de datos se usa "flask seeddb"
def seeds_db():
    print("\n\n==== SEEDING BASE DE DATOS ====")

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

    # Seed para sitios

    print("\n==== CREANDO SITES ====")

    sites_data = [
        {
            "nombre": "Machu Picchu",
            "descripcion_breve": "Ciudad inca antigua",
            "descripcion_completa": "Machu Picchu es una ciudadela inca situada en las montañas...",
            "ciudad": "Cusco",
            "provincia": "Cusco",
            "inauguracion": 2022,
            "latitud": -13.1631,
            "longitud": -72.5450,
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
            "latitud": 40.4319,
            "longitud": 116.5704,
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
            "latitud": 27.1751,
            "longitud": 78.0421,
            "categoria": "Arquitectónico",
            "estado_conservacion": "Malo",
            "visible": True,
        },
    ]

    user_data={
        "email": "lapampa2003@gmail.com",
        "nombre": "Juan Ignacio",
        "username": "jics",
        "apellido": "Coelho Soria",
        "contraseña_cifrada": "lapampa",
        "rol_id": "1",
    }

    add_user(user_data)

    add_site(sites_data[0])
    result = add_site(sites_data[1])

    add_site(sites_data[2])

    # sleep(5)
    modify_site(
        result.id,
        {"nombre": "Chichen Itza", "estado_conservacion": "Malo", "visible": False},
    )

    # sleep(5)
    modify_site(result.id, {"estado_conservacion": "Bueno", "visible": True})

    # sleep(5)
    modify_site(
        result.id,
        {
            "latitud": 19.8712,
            "longitud": -87.2856,
        },
    )

    # sleep(5)
    modify_site(
        result.id,
        {
            "ciudad": "Tuxtla Gutiérrez",
            "provincia": "Chiapas",
        },
    )

    # eliminar efectivamente el site con la funcion que lo maneje al eliminado
    add_site_history(result.id, HistoryAction.ELIMINAR, 1, None, result, None)

    # sleep(5)
    modify_site(
        result.id,
        {"nombre": "Chichen Itza", "estado_conservacion": "Malo", "visible": False},
    )

    # sleep(5)
    modify_site(result.id, {"estado_conservacion": "Bueno", "visible": True})

    # sleep(5)
    modify_site(
        result.id,
        {
            "latitud": 19.8712,
            "longitud": -87.2856,
        },
    )

    # sleep(5)
    modify_site(
        result.id,
        {
            "ciudad": "Tuxtla Gutiérrez",
            "provincia": "Chiapas",
        },
    )

    # eliminar efectivamente el site con la funcion que lo maneje al eliminado
    add_site_history(result.id, HistoryAction.ELIMINAR, 1, None, result, None)

    print(f"\n==== SEEDING LISTO ====\n\n")
