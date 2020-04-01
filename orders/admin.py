from django.contrib import admin
from django.contrib.auth.models import Group

from django.contrib.postgres import fields
from django_json_widget.widgets import JSONEditorWidget

from .forms import ExtraAdminForm
from .models import Size, Type, Extra, Item, Basket, Order


class ItemAdmin(admin.ModelAdmin):
    filter_horizontal = ('extras_available', )


class ExtraAdmin(admin.ModelAdmin):
    form = ExtraAdminForm


class BasketAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'user')
    list_filter = ('user',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'status')
    list_filter = ('status', )

    formfield_overrides = {
        fields.JSONField: {'widget': JSONEditorWidget}
    }

    readonly_fields = ["value", "user"]

    ordering = ('status', '-pk')



admin.site.site_header = "Pinocchio's Pizza & Subs administration site"
admin.site.register(Order, OrderAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Extra, ExtraAdmin)
admin.site.register(Size)
admin.site.register(Type)
admin.site.register(Basket, BasketAdmin)
admin.site.unregister(Group)
