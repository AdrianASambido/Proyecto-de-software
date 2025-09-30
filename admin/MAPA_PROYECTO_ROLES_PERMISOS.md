# 📁 MAPA DE ESTRUCTURA DEL PROYECTO - ROLES Y PERMISOS

## Estructura General
```
admin/
├── 📁 src/
│   ├── 📁 core/                    # Lógica de negocio y modelos
│   │   ├── 📁 Entities/            # Modelos de base de datos
│   │   │   ├── __init__.py         ✅ ACTUALIZADO - Agregado Permission
│   │   │   ├── site.py             📄 EXISTENTE - Modelo de sitios históricos
│   │   │   ├── user.py             ✅ ACTUALIZADO - Campo bloqueado y validaciones
│   │   │   ├── role.py             ✅ ACTUALIZADO - Relación many-to-many con permisos
│   │   │   ├── permission.py       🆕 NUEVO - Modelo de permisos con patrón modulo_accion
│   │   │   ├── feature_flag.py     📄 EXISTENTE - Modelo de feature flags
│   │   │   ├── site_history.py     📄 EXISTENTE - Modelo de historial
│   │   │   └── tag.py              📄 EXISTENTE - Modelo de tags
│   │   ├── 📁 services/            # Lógica de negocio
│   │   │   ├── 📁 roles/           🆕 NUEVO - Servicios de roles y permisos
│   │   │   │   └── __init__.py     🆕 NUEVO - CRUD completo de roles y permisos
│   │   │   ├── 📁 users/           ✅ ACTUALIZADO - Servicios de usuarios
│   │   │   │   └── __init__.py     ✅ ACTUALIZADO - Bloqueo y asignación de roles
│   │   │   ├── 📁 sites/           📄 EXISTENTE - Servicios de sitios
│   │   │   ├── 📁 tags/            📄 EXISTENTE - Servicios de tags
│   │   │   ├── 📁 history/         📄 EXISTENTE - Servicios de historial
│   │   │   └── 📁 feature_flags/   📄 EXISTENTE - Servicios de feature flags
│   │   ├── auth.py                 🆕 NUEVO - Sistema de autorización y decoradores
│   │   ├── board_sites.py          📄 EXISTENTE - Lógica de sitios
│   │   ├── board_feature_flags.py  📄 EXISTENTE - Lógica de feature flags
│   │   ├── database.py             📄 EXISTENTE - Configuración de BD
│   │   └── seeds.py                ✅ ACTUALIZADO - Seeds con roles y permisos
│   └── 📁 web/                     # Capa web y controladores
│       ├── 📁 controllers/         # Controladores REST
│       │   ├── sites.py            📄 EXISTENTE - Controlador de sitios
│       │   ├── users.py            📄 EXISTENTE - Controlador de usuarios
│       │   ├── gestion_roles.py    ✅ ACTUALIZADO - Controlador completo de roles
│       │   ├── feature_flags.py    📄 EXISTENTE - Controlador de feature flags
│       │   ├── tags.py             📄 EXISTENTE - Controlador de tags
│       │   └── sites_history.py    📄 EXISTENTE - Controlador de historial
│       ├── 📁 templates/           # Plantillas HTML
│       │   ├── 📁 administration/  # Plantillas de administración
│       │   │   ├── roles.html      🆕 NUEVO - Lista de roles
│       │   │   ├── role_detail.html 🆕 NUEVO - Detalle de rol con permisos
│       │   │   ├── users_roles.html 🆕 NUEVO - Gestión de usuarios y roles
│       │   │   ├── permissions.html 🆕 NUEVO - Lista de permisos
│       │   │   ├── feature_flags.html 📄 EXISTENTE - Interfaz de feature flags
│       │   │   └── mangement.html  📄 EXISTENTE
│       │   ├── 📁 usuarios/        📄 EXISTENTE - Plantillas de usuarios
│       │   ├── 📁 sites/           📄 EXISTENTE - Plantillas de sitios
│       │   ├── 📁 tags/            📄 EXISTENTE - Plantillas de tags
│       │   ├── 📁 login/           📄 EXISTENTE - Plantillas de login
│       │   ├── 📁 errores/         📄 EXISTENTE - Plantillas de error
│       │   └── 📁 common/          📄 EXISTENTE - Componentes comunes
│       ├── config.py               📄 EXISTENTE - Configuración SQLite
│       └── __init__.py             ✅ ACTUALIZADO - Blueprint de gestión de roles
│   ├── main.py                     📄 EXISTENTE - Punto de entrada
│   ├── pyproject.toml              📄 EXISTENTE - Configuración Poetry
│   └── app.db                      📄 EXISTENTE - Base de datos SQLite
```

## 📋 Detalles de Cambios por Archivo

### 🆕 ARCHIVOS NUEVOS

#### `src/core/Entities/permission.py`
- **Propósito**: Modelo de permisos con patrón `modulo_accion`
- **Campos**:
  - `id`: Clave primaria
  - `name`: Nombre único del permiso (ej: "user_index")
  - `description`: Descripción del permiso
  - `module`: Módulo (user, site, tag, feature_flag)
  - `action`: Acción (index, new, update, destroy, show)
  - `created_at`: Fecha de creación
- **Relaciones**: Many-to-many con roles
- **Métodos**: `full_name` (retorna modulo_accion)

#### `src/core/services/roles/__init__.py`
- **Propósito**: Servicios completos para roles y permisos
- **Funciones principales**:
  - `list_roles()`, `get_role_by_id()`, `create_role()`, `update_role()`, `delete_role()`
  - `list_permissions()`, `get_permission_by_id()`, `create_permission()`
  - `assign_permission_to_role()`, `remove_permission_from_role()`
  - `get_permissions_by_module()`, `get_role_permissions()`

#### `src/core/auth.py`
- **Propósito**: Sistema de autorización y decoradores
- **Decoradores**:
  - `@login_required`: Requiere usuario autenticado
  - `@admin_required`: Requiere rol administrador
  - `@permission_required(permission_name)`: Requiere permiso específico
- **Funciones auxiliares**:
  - `get_current_user()`, `is_admin()`, `has_permission()`

#### `src/web/templates/administration/roles.html`
- **Propósito**: Lista de roles con información básica
- **Características**: Tabla responsive, contador de usuarios, enlaces a detalles

#### `src/web/templates/administration/role_detail.html`
- **Propósito**: Detalle de rol con gestión de permisos
- **Características**: 
  - Información del rol
  - Permisos asignados (con opción de remover)
  - Permisos disponibles (con opción de asignar)
  - Formularios para asignar/remover permisos

#### `src/web/templates/administration/users_roles.html`
- **Propósito**: Gestión de usuarios y asignación de roles
- **Características**:
  - Lista de usuarios con estado (activo/bloqueado)
  - Selector de roles por usuario
  - Botones de bloquear/desbloquear
  - Resumen de usuarios por rol

#### `src/web/templates/administration/permissions.html`
- **Propósito**: Lista completa de permisos
- **Características**:
  - Tabla con colores por módulo y acción
  - Resumen por módulo
  - Leyenda de acciones
  - Información detallada de cada permiso

### ✅ ARCHIVOS MODIFICADOS

#### `src/core/Entities/role.py`
- **Cambios**:
  - Agregada tabla de asociación `role_permissions`
  - Relación many-to-many con `Permission`
  - Métodos: `has_permission()`, `add_permission()`, `remove_permission()`

#### `src/core/Entities/user.py`
- **Cambios**:
  - Agregado campo `bloqueado` (Boolean)
  - Propiedades: `is_admin`, `is_editor`
  - Métodos: `can_login()`, `can_be_blocked()`, `has_permission()`, `block()`, `unblock()`

#### `src/core/services/users/__init__.py`
- **Cambios**:
  - Funciones para bloqueo: `block_user()`, `unblock_user()`
  - Función para asignación de roles: `assign_role_to_user()`
  - Funciones de consulta: `get_users_by_role()`, `get_active_users()`, `get_blocked_users()`

#### `src/web/controllers/gestion_roles.py`
- **Cambios completos**:
  - Agregados decoradores de autorización
  - Rutas para gestión de roles y permisos
  - Rutas para gestión de usuarios
  - Endpoints API para AJAX
  - Validaciones de seguridad

#### `src/core/seeds.py`
- **Cambios**:
  - Agregadas importaciones de Role y Permission
  - Seeds para permisos de todos los módulos
  - Seeds para roles (Editor, Administrador)
  - Asignación automática de permisos a roles

#### `src/web/__init__.py`
- **Cambios**:
  - Agregada importación de `gestion_roles_bp`
  - Registrado blueprint de gestión de roles

#### `src/core/Entities/__init__.py`
- **Cambios**:
  - Agregada importación de `Permission`
  - Actualizado `__all__` con nueva entidad

## 🎯 Funcionalidades Implementadas

### Sistema de Roles
- ✅ **Editor**: Permisos limitados (solo sitios y tags)
- ✅ **Administrador**: Todos los permisos del sistema
- ✅ **Gestión completa**: Crear, editar, eliminar roles
- ✅ **Asignación de permisos**: Agregar/remover permisos a roles

### Sistema de Permisos
- ✅ **Patrón modulo_accion**: user_index, site_new, tag_update, etc.
- ✅ **Módulos**: user, site, tag, feature_flag
- ✅ **Acciones**: index, new, update, destroy, show, toggle
- ✅ **Gestión completa**: CRUD de permisos

### Sistema de Usuarios
- ✅ **Asignación de roles**: Cambiar rol de usuario
- ✅ **Bloqueo/desbloqueo**: Control de acceso
- ✅ **Validaciones**: Administradores no bloqueables
- ✅ **Estado**: Activo/inactivo, bloqueado/desbloqueado

### Sistema de Autorización
- ✅ **Decoradores**: @login_required, @admin_required, @permission_required
- ✅ **Validaciones automáticas**: Verificación de permisos
- ✅ **Control de acceso**: Bloqueo de rutas no autorizadas
- ✅ **Mensajes de error**: Feedback al usuario

## 🌐 URLs Disponibles

### Gestión de Roles
- **Panel Principal**: `http://localhost:5000/gestion-roles/`
- **Lista de Roles**: `http://localhost:5000/gestion-roles/roles`
- **Detalle de Rol**: `http://localhost:5000/gestion-roles/roles/<id>`
- **Gestión de Usuarios**: `http://localhost:5000/gestion-roles/usuarios`
- **Lista de Permisos**: `http://localhost:5000/gestion-roles/permisos`

### API Endpoints
- **Roles JSON**: `GET /gestion-roles/api/roles`
- **Rol de Usuario**: `GET /gestion-roles/api/usuarios/<id>/rol`

### Acciones
- **Asignar Rol**: `POST /gestion-roles/usuarios/<id>/asignar-rol`
- **Bloquear Usuario**: `POST /gestion-roles/usuarios/<id>/bloquear`
- **Desbloquear Usuario**: `POST /gestion-roles/usuarios/<id>/desbloquear`
- **Asignar Permiso**: `POST /gestion-roles/roles/<id>/permisos/<perm_id>/asignar`
- **Remover Permiso**: `POST /gestion-roles/roles/<id>/permisos/<perm_id>/remover`

## 🗄️ Base de Datos

### Tablas Nuevas
- **`permissions`**: Permisos del sistema
- **`role_permissions`**: Tabla de asociación roles-permisos

### Tablas Modificadas
- **`users`**: Agregado campo `bloqueado`
- **`roles`**: Relación con permisos

### Datos Iniciales
- **Roles**: Editor, Administrador
- **Permisos**: 17 permisos totales
  - 5 permisos de usuarios (user_*)
  - 5 permisos de sitios (site_*)
  - 5 permisos de tags (tag_*)
  - 2 permisos de feature flags (feature_flag_*)

## 🚀 Estado del Proyecto

- ✅ **Dependencias**: Instaladas con Poetry
- ✅ **Base de datos**: Creada y poblada
- ✅ **Aplicación**: Lista para ejecutar
- ✅ **Sistema de Roles**: Completamente funcional
- ✅ **Sistema de Permisos**: Completamente funcional
- ✅ **Sistema de Autorización**: Completamente funcional
- ✅ **Interfaz Web**: Completamente funcional

---

