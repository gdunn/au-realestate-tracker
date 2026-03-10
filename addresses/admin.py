from django.contrib import admin

from .models import Address, AddressConfig


class AddressAdmin(admin.ModelAdmin):
    list_display = ("street_address", "suburb", "state", "created_at")
    list_filter = ("state", "suburb")
    ordering = ("-created_at",)


class AddressConfigAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # only allow a single configuration object
        return not AddressConfig.objects.exists()


admin.site.register(Address, AddressAdmin)
admin.site.register(AddressConfig, AddressConfigAdmin)
