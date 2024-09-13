from django.contrib import admin
from .models import Cliente, Projeto, Atividade

# Register your models here.
admin.site.register(Cliente)
admin.site.register(Projeto)
admin.site.register(Atividade)
