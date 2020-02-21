from django.contrib import admin
from django.contrib.auth.models import Group

from .forms import ExtraAdminForm
from .models import Size, Type, Extra, Item


class ItemAdmin(admin.ModelAdmin):
    filter_horizontal = ('extras_available', )


class ExtraAdmin(admin.ModelAdmin):
    form = ExtraAdminForm


admin.site.site_header = "Pinocchio's Pizza & Subs administration site"
admin.site.register(Item, ItemAdmin)
admin.site.register(Extra, ExtraAdmin)
admin.site.register(Size)
admin.site.register(Type)
admin.site.unregister(Group)
