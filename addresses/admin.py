from django.contrib import admin

from .models import Address, AddressConfig, PropertyInfo


class PropertyInfoInline(admin.TabularInline):
    model = PropertyInfo
    fk_name = "address"
    readonly_fields = ("scraped_at",)
    can_delete = False
    extra = 0


class AddressAdmin(admin.ModelAdmin):
    list_display = ("street_address", "suburb", "state", "created_at")
    list_filter = ("state", "suburb")
    ordering = ("-created_at",)
    inlines = [PropertyInfoInline]


class AddressConfigAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # only allow a single configuration object
        return not AddressConfig.objects.exists()


class PropertyInfoAdmin(admin.ModelAdmin):
    list_display = (
        "address",
        "source_domain",
        "is_for_sale",
        "sale_type",
        "scraped_at",
    )
    list_filter = ("source_domain", "is_for_sale", "sale_type")
    readonly_fields = ("scraped_at",)


admin.site.register(Address, AddressAdmin)
admin.site.register(AddressConfig, AddressConfigAdmin)
admin.site.register(PropertyInfo, PropertyInfoAdmin)
