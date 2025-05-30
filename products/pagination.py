from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    """
    Kelas paginasi kustom untuk mengubah kunci 'results' menjadi 'products'
    dalam respons paginasi, sesuai dengan kriteria submission.
    """
    page_size = 10 # Ukuran halaman default, bisa diatur di settings.py juga
    page_size_query_param = 'page_size' # Memungkinkan klien menentukan page_size
    max_page_size = 100 # Batas maksimal page_size yang bisa diminta klien

    def get_paginated_response(self, data):
        """
        Mengembalikan objek respons paginasi kustom.
        Mengubah kunci 'results' menjadi 'products'.
        """
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'products': data # Mengubah 'results' menjadi 'products'
        })
