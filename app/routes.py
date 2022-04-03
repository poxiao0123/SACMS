from sanic import Blueprint

from app.controllers.count import count
from app.controllers.login import login
from app.controllers.staff.certificate import certificate
from app.controllers.staff.staff import staff

routes = Blueprint.group(certificate, staff, login, count, url_prefix="/api")
