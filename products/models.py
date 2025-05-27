from django.db import models
import uuid # Import modul uuid untuk UUIDField

class Product(models.Model):
    """
    Model Django untuk merepresentasikan produk dalam aplikasi OpenShop.
    Menggunakan UUID sebagai primary key untuk ID unik.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, unique=True) # SKU harus unik
    description = models.TextField(blank=True, null=True)
    shop = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    price = models.IntegerField()
    discount = models.IntegerField(default=0)
    category = models.CharField(max_length=100)
    stock = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    picture = models.URLField(blank=True, null=True)
    # Field untuk soft delete (Kriteria 4 Advanced)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Meta class untuk mendefinisikan opsi model.
        Mengatur nama tabel di database dan urutan default.
        """
        ordering = ['name'] # Urutkan produk berdasarkan nama secara default

    def __str__(self):
        """
        Representasi string dari objek Product.
        """
        return self.name