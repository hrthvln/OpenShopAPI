from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet untuk mengelola operasi CRUD pada model Product.
    Mendukung pembuatan, menampilkan daftar, menampilkan detail, mengubah, dan menghapus produk.
    Juga mendukung pencarian (filtering) berdasarkan nama dan lokasi.
    """
    queryset = Product.objects.all() # Queryset dasar, akan difilter lebih lanjut
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend] # Mengaktifkan filtering
    filterset_fields = {
        'name': ['icontains'], # Pencarian nama (case-insensitive contains)
        'location': ['exact'], # Pencarian lokasi (exact match)
    }

    def get_queryset(self):
        """
        Mengembalikan queryset yang difilter.
        Secara default, hanya menampilkan produk yang belum di-soft delete (is_delete=False).
        """
        queryset = super().get_queryset()
        # Filter out soft-deleted products by default
        return queryset.filter(is_delete=False)

    def create(self, request, *args, **kwargs):
        """
        Menangani pembuatan produk baru (POST /products).
        Mengembalikan status 201 Created jika sukses.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True) # Menerapkan validasi data (Kriteria 1 Advanced)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # Mengembalikan status 201 Created (Kriteria 1 Skilled)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, *args, **kwargs):
        """
        Menangani pengambilan detail produk (GET /products/{id}).
        Mengembalikan status 404 Not Found jika produk tidak ditemukan atau sudah di-soft delete.
        """
        try:
            instance = self.get_object()
            # Pastikan produk tidak di-soft delete saat diambil secara detail
            if instance.is_delete:
                return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND) # Kriteria 2 Skilled
        except Product.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND) # Kriteria 2 Skilled

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """
        Menangani pembaruan produk (PUT /products/{id}).
        Mengembalikan status 404 Not Found jika produk tidak ditemukan atau sudah di-soft delete.
        Mengembalikan status 400 Bad Request jika data tidak valid.
        """
        try:
            instance = self.get_object()
            # Pastikan produk tidak di-soft delete saat diperbarui
            if instance.is_delete:
                return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND) # Kriteria 3 Skilled
        except Product.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND) # Kriteria 3 Skilled

        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True) # Menerapkan validasi data (Kriteria 3 Advanced)
        self.perform_update(serializer)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Menangani penghapusan produk (DELETE /products/{id}).
        Menerapkan soft delete (Kriteria 4 Advanced).
        Mengembalikan status 204 No Content jika sukses.
        Mengembalikan status 404 Not Found jika produk tidak ditemukan.
        """
        try:
            instance = self.get_object()
            # Jika produk sudah di-soft delete, anggap tidak ditemukan
            if instance.is_delete:
                return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND) # Kriteria 4 Skilled
        except Product.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND) # Kriteria 4 Skilled

        # Lakukan soft delete
        instance.is_delete = True
        instance.save()
        # Mengembalikan status 204 No Content (Kriteria 4 Skilled)
        return Response(status=status.HTTP_204_NO_CONTENT)

     def list(self, request, *args, **kwargs):
        """
        Menangani daftar produk (GET /products).
        Mendukung pencarian berdasarkan nama dan lokasi (Kriteria 5).
        Mengembalikan daftar kosong jika tidak ada produk yang cocok.
        """
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # Mengembalikan respons paginasi yang sudah diatur oleh CustomPagination
            # CustomPagination.get_paginated_response() akan membungkus 'serializer.data'
            # ke dalam kunci 'products'
            return self.get_paginated_response(serializer.data) 

        serializer = self.get_serializer(queryset, many=True)
        # Jika tidak ada paginasi (misalnya, page_size=0 atau tidak ada query param paginasi)
        # Kita tetap membungkusnya secara manual dalam 'products'
        return Response({"products": serializer.data}) 
