from django.db import models


class AddressConfig(models.Model):
    """Site-wide configuration for the addresses app.

    Currently the only setting is the default state that should be applied when
    new addresses are created without an explicit state. This model is editable
    via the admin; the first record found is used and additional entries are
    discouraged (the admin prohibits creating more than one).
    """

    default_state = models.CharField(max_length=50, default="")

    class Meta:
        verbose_name = "Address configuration"
        verbose_name_plural = "Address configuration"

    def __str__(self):
        return "Address configuration"

    @classmethod
    def get_default_state(cls):
        cfg = cls.objects.first()
        return cfg.default_state if cfg else ""


class Address(models.Model):
    street_address = models.CharField(max_length=200)
    suburb = models.CharField(max_length=100)
    state = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.state:
            self.state = AddressConfig.get_default_state()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.street_address}, {self.suburb} {self.state}"


class PropertyInfo(models.Model):
    """Information scraped from real estate websites about a property."""

    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, related_name="property_info"
    )
    is_for_sale = models.BooleanField(default=False)
    sale_type = models.CharField(
        max_length=50, blank=True, help_text="auction, sale, etc."
    )
    price_info = models.CharField(
        max_length=200, blank=True, help_text="Price, guide, or 'contact agent'"
    )
    next_inspection = models.DateTimeField(null=True, blank=True)
    auction_date = models.DateTimeField(null=True, blank=True)
    last_sale_price = models.CharField(max_length=100, blank=True)
    scraped_at = models.DateTimeField(auto_now=True)
    source_domain = models.CharField(
        max_length=100, help_text="domain.com.au or realestate.com.au"
    )

    class Meta:
        verbose_name = "Property Information"
        verbose_name_plural = "Property Information"

    def __str__(self):
        return f"Property info for {self.address} from {self.source_domain}"
