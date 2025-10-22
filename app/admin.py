from django.contrib import admin
from app.models import Vacina

@admin.register(Vacina)
class VacinaAdmin(admin.ModelAdmin):
    ...