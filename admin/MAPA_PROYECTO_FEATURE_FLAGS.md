# 📁 MAPA DE ESTRUCTURA DEL PROYECTO - FEATURE FLAGS

## Estructura General
```
admin/
├── 📁 src/
│   ├── 📁 core/                    # Lógica de negocio y modelos
│   │   ├── 📁 Entities/            # Modelos de base de datos
│   │   │   ├── __init__.py         ✅ ACTUALIZADO - Importaciones agregadas
│   │   │   ├── site.py             📄 EXISTENTE - Modelo de sitios históricos
│   │   │   ├── user.py             ✅ CREADO - Modelo básico de usuario
│   │   │   ├── role.py             ✅ CREADO - Modelo básico de roles
│   │   │   └── feature_flag.py     🆕 NUEVO - Modelo de feature flags
│   │   ├── board_sites.py          📄 EXISTENTE - Lógica de sitios
│   │   ├── board_feature_flags.py  🆕 NUEVO - Lógica de feature flags
│   │   ├── database.py             📄 EXISTENTE - Configuración de BD
│   │   └── seeds.py                ✅ ACTUALIZADO - Seeds con feature flags
│   └── 📁 web/                     # Capa web y controladores
│       ├── 📁 controllers/          # Controladores REST
│       │   ├── sites.py            📄 EXISTENTE - Controlador de sitios
│       │   ├── gestion_roles.py    📄 EXISTENTE - Controlador de roles
│       │   └── feature_flags.py    🆕 NUEVO - Controlador de feature flags
│       ├── 📁 templates/            # Plantillas HTML
│       │   ├── 📁 administration/  # Plantillas de administración
│       │   │   ├── feature_flags.html ✅ ACTUALIZADO - Interfaz completa
│       │   │   └── mangement.html  📄 EXISTENTE
│       │   └── 📁 errores/         # Plantillas de error
│       │       └── maintenance.html 🆕 NUEVO - Página de mantenimiento
│       ├── config.py               ✅ ACTUALIZADO - Configuración SQLite
│       └── __init__.py             ✅ ACTUALIZADO - App factory y middleware
├── main.py                         📄 EXISTENTE - Punto de entrada
├── pyproject.toml                  📄 EXISTENTE - Configuración Poetry
└── app.db                          🆕 NUEVO - Base de datos SQLite
```

## 📋 Detalles de Cambios por Archivo

### 🆕 ARCHIVOS NUEVOS

#### `src/core/Entities/feature_flag.py`
- **Propósito**: Modelo de base de datos para feature flags
- **Campos**:
  - `id`: Clave primaria
  - `name`: Nombre único del flag (ej: "admin_maintenance_mode")
  - `description`: Descripción del flag
  - `is_enabled`: Estado ON/OFF
  - `maintenance_message`: Mensaje personalizado para mantenimiento
  - `last_modified_by`: Usuario que modificó por última vez
  - `last_modified_at`: Fecha/hora de última modificación
  - `created_at`: Fecha de creación
- **Métodos**: `to_dict()` para serialización

#### `src/core/board_feature_flags.py`
- **Propósito**: Lógica de negocio para feature flags
- **Funciones principales**:
  - `list_feature_flags()`: Obtener todos los flags
  - `get_feature_flag_by_name()`: Buscar por nombre
  - `update_feature_flag()`: Actualizar estado con auditoría
  - `is_admin_maintenance_mode()`: Verificar modo mantenimiento admin
  - `is_portal_maintenance_mode()`: Verificar modo mantenimiento portal
  - `are_reviews_enabled()`: Verificar si reseñas están habilitadas
  - `get_admin_maintenance_message()`: Obtener mensaje de mantenimiento admin
  - `get_portal_maintenance_message()`: Obtener mensaje de mantenimiento portal

#### `src/web/controllers/feature_flags.py`
- **Propósito**: Controlador REST para feature flags
- **Rutas**:
  - `GET /admin/feature-flags/`: Lista de flags
  - `POST /admin/feature-flags/toggle/{id}`: Cambiar estado de flag
  - `GET /admin/feature-flags/status`: API de estado (JSON)
- **Características**: Manejo de JSON, validaciones, respuestas REST

#### `src/web/templates/errores/maintenance.html`
- **Propósito**: Página de mantenimiento
- **Características**:
  - Diseño responsive con Bootstrap
  - Animación de icono de herramientas
  - Botones de reintentar y volver
  - Mensaje personalizable
  - Estilos CSS integrados

### ✅ ARCHIVOS MODIFICADOS

#### `src/core/Entities/__init__.py`
- **Cambio**: Agregadas importaciones de User, Role y FeatureFlag
- **Antes**: Solo importaba Site
- **Después**: Importa todas las entidades

#### `src/core/seeds.py`
- **Cambios**:
  - Agregada importación de FeatureFlag y date
  - Corregido formato de fecha para SQLite
  - Agregados seeds para 3 feature flags iniciales:
    - `admin_maintenance_mode`: Modo mantenimiento administración
    - `portal_maintenance_mode`: Modo mantenimiento portal
    - `reviews_enabled`: Control de reseñas

#### `src/web/__init__.py`
- **Cambios**:
  - Agregada importación de `board_feature_flags`
  - Registrado blueprint de feature flags
  - Implementado middleware `check_maintenance_mode()`:
    - Verifica flags antes de cada request
    - Bloquea rutas según configuración
    - Permite excepciones para System Admins
    - Retorna página de mantenimiento con código 503

#### `src/web/config.py`
- **Cambios**:
  - Cambiado de PostgreSQL a SQLite para desarrollo
  - Configuración más simple para desarrollo local
  - Comentada configuración PostgreSQL original

#### `src/web/templates/administration/feature_flags.html`
- **Cambios completos**:
  - Interfaz moderna con Bootstrap
  - Toggles interactivos con JavaScript
  - Modal para mensajes de mantenimiento
  - Actualización en tiempo real via AJAX
  - Validaciones del lado cliente
  - Alertas de éxito/error
  - Tabla responsive con información completa

### ✅ ARCHIVOS CREADOS/COMPLETADOS

#### `src/core/Entities/user.py`
- **Propósito**: Modelo básico de usuario
- **Campos**: id, username, email, created_at
- **Estado**: Creado para evitar errores de importación

#### `src/core/Entities/role.py`
- **Propósito**: Modelo básico de roles
- **Campos**: id, name, description, created_at
- **Estado**: Creado para evitar errores de importación

## 🎯 Funcionalidades Implementadas

### Feature Flags Disponibles
1. **admin_maintenance_mode**: Bloquea administración excepto login y feature flags
2. **portal_maintenance_mode**: Pone el portal en modo mantenimiento
3. **reviews_enabled**: Controla la creación/visualización de reseñas

### Características del Sistema
- ✅ **Solo System Admins** pueden gestionar flags
- ✅ **Cambios en tiempo real** sin reiniciar aplicación
- ✅ **Mensajes personalizables** para mantenimiento
- ✅ **Auditoría completa** (quién y cuándo modificó)
- ✅ **Middleware automático** que bloquea rutas
- ✅ **Interfaz intuitiva** con validaciones
- ✅ **API REST** para integración externa

## 🌐 URLs Disponibles

- **Panel Feature Flags**: `http://localhost:5000/admin/feature-flags/`
- **API Estado**: `http://localhost:5000/admin/feature-flags/status`
- **Toggle Flag**: `POST /admin/feature-flags/toggle/{id}`

## 🗄️ Base de Datos

- **Motor**: SQLite (desarrollo local)
- **Archivo**: `app.db`
- **Tablas**: sites, users, roles, feature_flags
- **Seeds**: Ejecutados con datos iniciales

## 🚀 Estado del Proyecto

- ✅ **Dependencias**: Instaladas con Poetry
- ✅ **Base de datos**: Creada y poblada
- ✅ **Aplicación**: Lista para ejecutar
- ✅ **Feature Flags**: Completamente funcionales

---

**Fecha de creación**: $(date)
**Desarrollado por**: Asistente AI
**Versión**: 1.0
