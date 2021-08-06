from django.core.validators import MinValueValidator
from django.db.models.fields import DecimalField
from root.core.utils.files import store_cover_images
from django.db import models
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.deletion import CASCADE
from django.contrib.postgres.fields import JSONField
from root.suppliers.models import Supplier
from django.utils.text import slugify
from decimal import Decimal


def opening_hours_default_value():
    return {
        "sunday": {"open": True, "from": "00:00:00", "to": "00:00:00"},
        "monday": {"open": True, "from": "00:00:00", "to": "00:00:00"},
        "tuesday": {"open": True, "from": "00:00:00", "to": "00:00:00"},
        "wednesday": {"open": True, "from": "00:00:00", "to": "00:00:00"},
        "thursday": {"open": True, "from": "00:00:00", "to": "00:00:00"},
        "friday": {"open": True, "from": "00:00:00", "to": "00:00:00"},
        "saturday": {"open": True, "from": "00:00:00", "to": "00:00:00"},
    }


class DeliveryArea(models.Model):
    addon_price = models.DecimalField(
        _("Addon Price"), null=False, blank=False, max_digits=5, decimal_places=2
    )
    basket_value = models.DecimalField(
        _("Basket Value"), null=True, blank=True, max_digits=5, decimal_places=2
    )
    city_name = models.CharField(
        _("City Name"), null=False, blank=False, max_length=100
    )
    area_name = models.CharField(
        _("Area Name"), null=False, blank=False, max_length=100
    )
    store = models.ForeignKey(
        "Store", CASCADE, null=True, blank=True, related_name="delivery_areas"
    )

    def __str__(self):
        return str(self.area_name)

    class Meta:
        verbose_name = _("Delivery Area")
        verbose_name_plural = _("Delivery Areas")


class Store(models.Model):
    TAX_RATE_CHOICES = (
        ("INCLUSIVE", "Inclusive"),
        ("EXCLUSIVE", "Exclusive"),
    )
    ORDER_SCHEDULE_CHOICES = (
        ("NEXT DAY", "Next Day"),
        ("SAME DAY", "Same Day"),
    )
    phone = PhoneNumberField(
        help_text=_("Required. Phone number with country code."),
        error_messages={"unique": _("A Store with that phone number already exists.")},
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(_("Active"), default=True)
    email = models.EmailField(_("Store Email"), blank=True, null=True)
    name = models.CharField(_("Store Name"), null=False, blank=False, max_length=100)
    slug = models.SlugField(_("Store Slug"), null=False, blank=True, max_length=100)
    tax_type = models.CharField(
        _("Tax Type"), null=True, blank=True, max_length=100, choices=TAX_RATE_CHOICES
    )
    tax_rate = models.IntegerField(_("Tax Type"), null=False, blank=False)
    order_schedule = models.CharField(
        _("Order Schedule"),
        null=True,
        blank=True,
        max_length=100,
        choices=ORDER_SCHEDULE_CHOICES,
    )

    supplier = models.OneToOneField(
        Supplier, CASCADE, null=False, blank=False, related_name="store"
    )
    cover_image = models.ImageField(
        _("Cover Image"), upload_to=store_cover_images, null=True, blank=True
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = _("Store")
        verbose_name_plural = _("Stores")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Store, self).save(*args, **kwargs)


class AddressSettings(models.Model):
    address = models.CharField(_("Address"), null=True, blank=True, max_length=500)
    area = models.CharField(_("Area"), null=False, blank=False, max_length=100)
    store = models.OneToOneField(
        Store, CASCADE, null=False, blank=False, related_name="address_settings"
    )

    def __str__(self):
        return f"Address: {self.area} - {self.address}"

    class Meta:
        verbose_name = _("AddressPreference")
        verbose_name_plural = _("AddressPreferences")


class DeliverySettings(models.Model):
    PAYMENT_CHOICES = (("CASH_ON_DELIVERY", "Cash on Delivery"),)
    OPERATION_CHOICES = (
        ("X_DAYS_OPTION", "X Days Option"),
        ("INSTANT", "instant "),
        ("SCHEDULED", "scheduled"),
    )
    payment_method = models.CharField(
        _("Payment Method"),
        null=False,
        blank=False,
        max_length=16,
        choices=PAYMENT_CHOICES,
        default="CASH_ON_DELIVERY",
    )
    opening_hours = JSONField(
        _("Opening Hours"),
        default=opening_hours_default_value,
        null=False,
        blank=False,
    )
    operation_settings = models.CharField(
        _("Operation Settings"),
        null=False,
        blank=False,
        max_length=13,
        choices=OPERATION_CHOICES,
        default="INSTANT",
    )
    operation_days = models.IntegerField(_("Operation Days"), blank=True, null=True)
    operation_scheduled_date = models.DateTimeField(
        _("Scheduled Date"), blank=True, null=True
    )
    store = models.OneToOneField(
        Store, CASCADE, null=False, blank=False, related_name="delivery_settings"
    )

    def __str__(self):
        return f"Delivery Settings"

    class Meta:
        verbose_name = _("DeliveryPreference")
        verbose_name_plural = _("DeliveryPreferences")


class Item(models.Model):
    name = models.CharField(_("Item Name"), max_length=100, null=False, blank=False,)
    description = models.CharField(
        _("Description"), max_length=500, null=True, blank=True,
    )
    store = models.ForeignKey(
        Store, CASCADE, null=True, blank=True, related_name="item"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Item")
        verbose_name_plural = _("Items")


class Variation(models.Model):
    name = models.CharField(
        _("Variation Name"), max_length=100, null=False, blank=False,
    )
    price = DecimalField(
        _("Price"),
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    item = models.ForeignKey(
        Item, CASCADE, null=True, blank=True, related_name="variations"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Variation")
        verbose_name_plural = _("Variations")


class Extra(models.Model):
    name = models.CharField(_("Extras Name"), max_length=100, null=False, blank=False,)
    price = DecimalField(
        _("Price"),
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    item = models.ForeignKey(
        Item, CASCADE, null=True, blank=True, related_name="extras"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Extra")
        verbose_name_plural = _("Extras")


class Category(models.Model):
    name = models.CharField(_("Category Name"), null=False, blank=False, max_length=100)
    items = models.ManyToManyField(Item, blank=True, related_name="Categories")
    store = models.ForeignKey(
        Store, CASCADE, null=True, blank=True, related_name="category"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
