from time import sleep
from src.core.board_sites import add_site, update_site
from src.core.Entities.site_history import HistoryAction
from src.core.sites_history import add_site_history

def seeds_db():
    print("\n\n==== SEEDING BASE DE DATOS ====")
    site_data = {
        "nombre":"Chicho Itsa",
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

    sleep(5)
    update_site(result.id, {
        "nombre":"Chichen Itza",
        "estado_conservacion":"Malo",
        "visible":False
    })

    sleep(5)
    update_site(result.id, {
        "estado_conservacion":"Bueno",
        "visible":True
    })

    sleep(5)
    update_site(result.id, {
        "latitud":19.8712,
        "longitud":-87.2856,
    })

    sleep(5)
    update_site(result.id, {
        "ciudad":"Tuxtla Gutiérrez",
        "provincia":"Chiapas",
    })


    add_site_history(result.id, HistoryAction.ELIMINAR, 1, None, result, None)

    print(f"\n==== SEEDING LISTO ====\n\n")