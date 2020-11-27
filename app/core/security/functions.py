import socket

from crum import get_current_request

from core.erp.crm.models import Vehicle
from core.security.forms import Company
from datetime import datetime


def system_information(request):
    data = {
        'comp': get_company(),
        'hostname': socket.gethostname(),
        'menu': get_layout(),
        'localhost': socket.gethostbyname(socket.gethostname()),
        'date_joined': datetime.now(),
        'vehicles_client': get_vehs()
    }
    return data


def get_company():
    try:
        items = Company.objects.all()
        if items.exists():
            return items[0]
    except:
        pass
    return None


def get_layout():
    objs = Company.objects.filter()
    if objs.exists():
        objs = objs[0]
        if objs.layout == 1:
            return 'vtc_body.html'
        return 'hzt_body.html'
    return 'hzt_body.html'


def get_vehs():
    try:
        request = get_current_request()
        return Vehicle.objects.filter(cli__user_id=request.user.id)
    except:
        pass
    return []
