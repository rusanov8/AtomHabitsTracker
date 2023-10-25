from rest_framework import pagination


class HabitPaginator(pagination.PageNumberPagination):
    """ Custom paginator for paginating Habit objects. """

    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50