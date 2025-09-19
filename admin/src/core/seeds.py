from src.core.board_sites import add_site

def seeds_db():
    print("\n\n==== SEEDING BASE DE DATOS ====")
    site_data = {
        "nombre":"Chichen Itza",
        "descripcion_breve":"Ciudad maya antigua",
        "descripcion_completa":"Chichen Itza fue una gran ciudad precolombina...",
        "ciudad":"Yucatan",
        "provincia":"Yucatan",
        "inauguracion":"2022-01-01",
        "latitud":18.9712,
        "longitud":-88.9856,
        "categoria":"Arqueológico",
        "estado_conservacion":"Bueno",
        "visible":True
    }
    result = add_site(site_data)
    print(result)
    print(f"\n==== SEEDING LISTO ====\n\n")