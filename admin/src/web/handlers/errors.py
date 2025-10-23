from flask import render_template
from dataclasses import dataclass

@dataclass
class HttpError:
    code: int
    message: str
    description: str

def not_found(e):
    error = HttpError(
        code=404,
        message="Página No Encontrada",
        description="Lo sentimos, la página que estás buscando no existe."
    )
    return render_template("errors.html", error=error), 404

def internal_error(e):
    error = HttpError(
        code=500,
        message="Error Interno del Servidor",
        description="Lo sentimos, ha ocurrido un error en el servidor. Por favor, intenta nuevamente más tarde."
    )
    return render_template("errors.html", error=error), 500

