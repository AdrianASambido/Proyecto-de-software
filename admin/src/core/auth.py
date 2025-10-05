"""
Módulo de autenticación y autorización
"""

from functools import wraps
from flask import session, redirect, url_for, flash, request
from src.core.services.users import get_user_by_id
from werkzeug.exceptions import abort

def login_required(f):
    """
    Decorador que requiere que el usuario esté autenticado
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
         
            return redirect(url_for('login.login'))
        
        # Verificar que el usuario existe y puede iniciar sesión
    

        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """
    Decorador que requiere que el usuario sea administrador
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debe iniciar sesión para acceder a esta página', 'error')
            return redirect(url_for('login.login'))
        
        user = get_user_by_id(session['user_id'])
        if not user or not user.can_login():
            session.clear()
            flash('Su cuenta está bloqueada o inactiva', 'error')
            return redirect(url_for('login.login'))
        
        if not user.is_admin:
            flash('No tiene permisos para acceder a esta página', 'error')
            return redirect(url_for('home'))
        
        return f(*args, **kwargs)
    return decorated_function


def permission_required(permission_name):
    """
    Decorador que requiere un permiso específico
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Debe iniciar sesión para acceder a esta página', 'error')
                return redirect(url_for('login.login'))
            
            user = get_user_by_id(session['user_id'])
           
            
            if not user.has_permission(permission_name):
                flash(f'No tiene permisos para realizar esta acción: {permission_name}', 'error')
                return redirect(url_for('home'))
          
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def get_current_user():
    """
    Obtiene el usuario actual de la sesión
    """
    if 'user_id' in session:
        return get_user_by_id(session['user_id'])
    return None


def is_admin():
    """
    Verifica si el usuario actual es administrador
    """
    user = get_current_user()
    return user and user.is_admin


def has_permission(permission_name):
    """
    Verifica si el usuario actual tiene un permiso específico
    """
    user = get_current_user()
    return user and user.has_permission(permission_name)
