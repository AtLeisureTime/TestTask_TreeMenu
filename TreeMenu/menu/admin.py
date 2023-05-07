from django.contrib import admin
from . import models


@admin.register(models.Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(models.Element)
class ElementAdmin(admin.ModelAdmin):
    list_display = ['id', 'menu_name', 'parent', 'value', 'url', 'namedUrl']
    list_filter = ['parent', 'menu__name']

    @admin.display(ordering='menu__name', description='menu name')
    def menu_name(self, obj):
        return obj.menu.name
