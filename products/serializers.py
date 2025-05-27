from rest_framework import serializers
from .models import Product
from django.urls import reverse # Untuk menghasilkan URL

class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer untuk model Product.
    Mengonversi instance model Product ke format JSON dan sebaliknya.
    Juga menambahkan HATEOAS (_links) ke respons.
    """
    # Field 'id' akan otomatis ditangani oleh ModelSerializer karena itu primary_key
    # Field 'is_delete' akan disertakan karena default=False

    # Menambahkan HATEOAS (_links)
    _links = serializers.SerializerMethodField()

    class Meta:
        """
        Meta class untuk Serializer.
        Mendefinisikan model dan field yang akan diserialisasi.
        """
        model = Product
        fields = [
            'id', 'name', 'sku', 'description', 'shop', 'location',
            'price', 'discount', 'category', 'stock', 'is_available',
            'picture', 'is_delete', '_links' # Sertakan _links di fields
        ]
        read_only_fields = ['id', 'created_at', 'updated_at'] # ID dan timestamp tidak bisa diubah via API

    def get__links(self, obj):
        """
        Metode untuk menghasilkan HATEOAS links.
        Mengembalikan daftar dictionary yang merepresentasikan link terkait.
        """
        request = self.context.get('request')
        if request is None:
            return [] # Kembalikan list kosong jika request tidak tersedia (misalnya, di shell)

        # Base URL untuk produk
        product_list_url = request.build_absolute_uri(reverse('product-list'))
        product_detail_url = request.build_absolute_uri(reverse('product-detail', kwargs={'pk': obj.id}))

        links = [
            {
                "rel": "self",
                "href": product_list_url,
                "action": "POST",
                "types": ["application/json"]
            },
            {
                "rel": "self",
                "href": product_detail_url,
                "action": "GET",
                "types": ["application/json"]
            },
            {
                "rel": "self",
                "href": product_detail_url,
                "action": "PUT",
                "types": ["application/json"]
            },
            {
                "rel": "self",
                "href": product_detail_url,
                "action": "DELETE",
                "types": ["application/json"]
            }
        ]
        return links
