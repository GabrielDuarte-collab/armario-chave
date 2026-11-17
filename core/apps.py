from django.apps import AppConfig
from django.contrib import admin
from .models import Unidade, Usuario, Espaco, Chave


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"


admin.site.register(Unidade)
admin.site.register(Usuario)
admin.site.register(Espaco)
admin.site.register(Chave)
