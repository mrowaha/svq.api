"""
This package contains app wide routes for the fastApi application
:author Muhammad Rowaha <ashfaqrowaha@gmail.com>
"""
from .echo import register as registerEcho
from .datasource import register as registerDataSourceHandlers
from .auth import register as registerAuth
from .annotate import register as registerAnnotate
