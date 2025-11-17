from flask import Blueprint


api_bp=Blueprint('api', __name__, url_prefix='/api')

from . import sites
from . import reviews
from . import tags
from . import users
from . import loginGoogle
from . import maintenance