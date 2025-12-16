
from math import ceil
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from shared.enums.pagination_enum import Status
from shared.enums import pagination_enum
def fetch_with_pagination(
    queryset,
    *,
    page: int = 1,
    limit: int = 10,
    search: dict | None = None,
    is_active: str | None = 'active',
    type_: str = 'page',
    sort: str | None = None,
    to_domain=lambda x: x,
    to_response=lambda x: x,
    request: Request | None = None,
) -> dict:
    """
    Generic pagination helper for DRF + DDD.

    Args:
        queryset: Django queryset
        page: current page number
        limit: page size
        search: dict with keys 'kw' and 'field'
        is_active: filter active users (True/False)
        type_: 'page' = paginate, 'all' = return all
        sort: ordering string (ex: '-created')
        to_domain: callable to convert ORM obj to domain obj
        request: optional DRF request (for pagination)

    Returns:
        dict with keys:
            data: list of domain objects
            pagination: dict with total, count, limit, totalPages, currentPage
    """

    if is_active is Status.ACTIVE:
        queryset = queryset.filter(is_removed=False)
    elif is_active is Status.INACTIVE:
        queryset = queryset.filter(is_removed=True)


    if search and search.get('kw') and search.get('field'):
        kw = search['kw']
        field = search['field']
        filter_expr = {f"{field}__icontains": kw}
        queryset = queryset.filter(**filter_expr)

    if sort:
        queryset = queryset.order_by(sort)
    else:
        queryset = queryset.order_by('-created')
    if type_ == pagination_enum.GetType.ALL:
        entities = list(queryset)
        domain_objs = [to_domain(obj) for obj in entities]
        serialized = [to_response(obj) for obj in entities]
        total = len(domain_objs)
        return {
            'data': serialized,
            'pagination': {
                'total': total,
                'count': total,
                'limit': 0,
                'totalPages': 1,
                'page': 1,
            }
        }

    paginator = PageNumberPagination()
    paginator.page_size = limit
    class DummyRequest:
        def __init__(self, page, page_size):
            self.query_params = {'page': str(page), 'page_size': str(page_size)}

    use_request = request or DummyRequest(page, limit)

    paginated_qs = paginator.paginate_queryset(queryset, use_request)
    
    domain_objs = [to_domain(obj) for obj in paginated_qs]
    serialized = [to_response(obj) for obj in domain_objs]

    return {
        'data': serialized,
        'pagination': {
            'total': paginator.page.paginator.count,
            'count': len(domain_objs),
            'limit': paginator.page_size,
            'totalPages': paginator.page.paginator.num_pages,
            'page': paginator.page.number,
        }
    }
