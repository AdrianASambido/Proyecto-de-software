from src.core.sites import add_site

def seeds_db():
    print("\n\n==== SEEDING BASE DE DATOS ====")
    site_data1 = {
        "nombre":"Chichen Itza",
        "descripcion_breve":"Ciudad maya antigua",
        "descripcion_completa":"Chichen Itza fue una gran ciudad precolombina...",
        "ciudad":"Yucatan",
        "provincia":"Yucatan",
        "inauguracion":2022,
        "latitud":18.9712,
        "longitud":-88.9856,
        "categoria":"Arqueológico",
        "estado_conservacion":"Bueno",
        "visible":True
    }
    site_data2 = {
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
    }
    site_data3 = {
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
    }
    site_data4={
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
    
    result = add_site(site_data4)
    
    
    print(result)
    print(f"\n==== SEEDING LISTO ====\n\n")