from rest_framework.pagination import PageNumberPagination


class PageNumberPaginationWithCount(PageNumberPagination):
    def get_paginated_response(self, data):
        # Чтобы подстроиться под тесты
        response = super(PageNumberPaginationWithCount, self).get_paginated_response(data)
        response.data['total_pages'] = self.page.paginator.num_pages
        response.data['prev'] = self.page.previous_page_number() if self.page.has_previous() else None
        response.data['next'] = self.page.next_page_number() if self.page.has_next() else None
        del response.data['previous']
        return response
