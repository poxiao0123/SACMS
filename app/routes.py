from sanic import Blueprint

from app.controllers.login import login
from app.controllers.staff.certificate import certificate
from app.controllers.staff.staff import staff

routes = Blueprint.group(certificate, staff, login, url_prefix="/api")
