# 🔄 FLUJO DE SOLICITUDES - SISTEMA DE ROLES Y PERMISOS

## 📋 Diagrama de Flujo de una Solicitud

```
🌐 CLIENTE (Navegador)
    ↓
📡 RUTA (/gestion-roles/usuarios)
    ↓
🔒 MIDDLEWARE DE AUTORIZACIÓN
    ├── @admin_required
    ├── Verificar sesión activa
    ├── Verificar usuario no bloqueado
    └── Verificar rol administrador
    ↓
🎯 CONTROLADOR (gestion_roles.py)
    ├── list_users()
    ├── Obtener usuarios del servicio
    └── Obtener roles del servicio
    ↓
⚙️ SERVICIOS (users/__init__.py, roles/__init__.py)
    ├── list_users() → User.query.all()
    ├── list_roles() → Role.query.all()
    └── Retornar datos procesados
    ↓
🗄️ BASE DE DATOS (SQLite)
    ├── Tabla: users
    ├── Tabla: roles
    ├── Tabla: permissions
    └── Tabla: role_permissions
    ↓
📊 TEMPLATE (users_roles.html)
    ├── Renderizar lista de usuarios
    ├── Mostrar roles disponibles
    ├── Formularios de acción
    └── JavaScript para interactividad
    ↓
🌐 RESPUESTA HTML al Cliente
```

## 🔍 Ejemplo Detallado: Bloquear un Usuario

### 1. **Solicitud del Cliente**
```
POST /gestion-roles/usuarios/5/bloquear
Content-Type: application/x-www-form-urlencoded
```

### 2. **Middleware de Autorización**
```python
@permission_required("user_update")
def block_user(user_id):
    # Verificaciones automáticas:
    # ✅ Usuario logueado
    # ✅ Usuario activo y no bloqueado
    # ✅ Tiene permiso "user_update"
```

### 3. **Controlador**
```python
def block_user(user_id):
    success = users.block_user(user_id)
    if success:
        flash("Usuario bloqueado correctamente", "success")
    else:
        flash("No se puede bloquear este usuario (es administrador)", "error")
    return redirect(url_for("gestion_roles.list_users"))
```

### 4. **Servicio de Usuarios**
```python
def block_user(user_id):
    usuario = get_user_by_id(user_id)
    if usuario and usuario.can_be_blocked():  # Verifica que no sea admin
        usuario.block()  # Cambia bloqueado = True
        db.session.commit()
        return True
    return False
```

### 5. **Modelo de Usuario**
```python
def block(self):
    if self.can_be_blocked():  # Verifica que no sea administrador
        self.bloqueado = True
        return True
    return False

def can_be_blocked(self):
    return not self.is_admin  # Administradores no pueden ser bloqueados
```

### 6. **Base de Datos**
```sql
UPDATE users 
SET bloqueado = 1 
WHERE id = 5 AND rol_id != (SELECT id FROM roles WHERE name = 'Administrador')
```

### 7. **Respuesta**
```html
<!-- Redirección a lista de usuarios con mensaje flash -->
<div class="alert alert-success">
    Usuario bloqueado correctamente
</div>
```

## 🎯 Flujo de Autorización por Permisos

### Ejemplo: Acceder a Gestión de Roles

```
1. 🌐 Usuario accede a /gestion-roles/
   ↓
2. 🔒 @admin_required verifica:
   ├── ¿Está logueado? → Si no: redirect a login
   ├── ¿Usuario activo? → Si no: redirect a login
   ├── ¿Es administrador? → Si no: redirect a home
   └── ✅ Acceso permitido
   ↓
3. 🎯 Controlador ejecuta función
   ↓
4. 📊 Template se renderiza
   ↓
5. 🌐 Usuario ve la página
```

### Ejemplo: Asignar Permiso a Rol

```
1. 🌐 Usuario hace POST a /gestion-roles/roles/2/permisos/5/asignar
   ↓
2. 🔒 @admin_required verifica permisos
   ↓
3. 🎯 assign_permission_to_role() ejecuta:
   ├── Obtiene rol por ID
   ├── Obtiene permiso por ID
   ├── Llama a servicio para asignar
   └── Redirecciona con mensaje
   ↓
4. ⚙️ Servicio roles.assign_permission_to_role():
   ├── role.add_permission(permission)
   ├── db.session.commit()
   └── Retorna True/False
   ↓
5. 🗄️ Base de datos actualiza tabla role_permissions
   ↓
6. 🌐 Usuario ve confirmación
```

## 🔐 Sistema de Validaciones

### En el Modelo de Usuario
```python
def can_login(self):
    return self.activo and not self.bloqueado

def can_be_blocked(self):
    return not self.is_admin

def has_permission(self, permission_name):
    if not self.role:
        return False
    return self.role.has_permission(permission_name)
```

### En el Modelo de Rol
```python
def has_permission(self, permission_name):
    return any(perm.name == permission_name for perm in self.permissions)
```

### En el Middleware de Autorización
```python
@permission_required("user_update")
def block_user(user_id):
    # Automáticamente verifica:
    # 1. Usuario logueado
    # 2. Usuario activo
    # 3. Usuario no bloqueado
    # 4. Usuario tiene permiso "user_update"
```

## 📊 Flujo de Datos en Templates

### Template: users_roles.html
```
1. 📊 Recibe datos del controlador:
   ├── users: Lista de usuarios
   └── roles: Lista de roles disponibles
   ↓
2. 🎨 Renderiza tabla de usuarios:
   ├── Muestra información básica
   ├── Muestra rol actual con colores
   ├── Muestra estado (activo/bloqueado)
   └── Crea formularios de acción
   ↓
3. 🔧 JavaScript para interactividad:
   ├── Confirmaciones de acción
   ├── Validaciones del lado cliente
   └── Actualizaciones dinámicas
   ↓
4. 🌐 HTML final enviado al navegador
```

## 🚀 Ventajas del Sistema Implementado

### 1. **Separación de Responsabilidades**
- **Modelos**: Lógica de negocio y validaciones
- **Servicios**: Operaciones de base de datos
- **Controladores**: Lógica de presentación y rutas
- **Templates**: Interfaz de usuario

### 2. **Seguridad en Múltiples Capas**
- **Decoradores**: Validación automática de permisos
- **Modelos**: Validaciones de negocio
- **Servicios**: Validaciones de datos
- **Templates**: Validaciones del lado cliente

### 3. **Flexibilidad**
- **Permisos granulares**: Control específico por acción
- **Roles dinámicos**: Fácil agregar nuevos roles
- **Módulos extensibles**: Fácil agregar nuevos módulos

### 4. **Mantenibilidad**
- **Código organizado**: Estructura clara y consistente
- **Reutilización**: Servicios y decoradores reutilizables
- **Documentación**: Código autodocumentado

---

**Este flujo garantiza que cada solicitud pase por todas las validaciones necesarias antes de ejecutar cualquier acción, manteniendo la seguridad y la integridad del sistema.**
