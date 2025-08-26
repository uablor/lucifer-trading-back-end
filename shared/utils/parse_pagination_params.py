from typing import Dict
from rest_framework.request import Request
from shared.enums import pagination_enum
def parse_pagination_params(request: Request) -> Dict:

    page = request.query_params.get('page', 1)
    limit = request.query_params.get('limit', 10)
    search_kw = request.query_params.get('search')
    search_field = request.query_params.get('search_field')

    try:
        is_active_param = request.query_params.get('is_active')
        is_active = pagination_enum.Status(is_active_param.lower()) if is_active_param else None
    except ValueError:
        is_active = None
    try:
        type_ = pagination_enum.GetType(request.query_params.get('type', 'page'))
    except ValueError:
        type_ = pagination_enum.GetType('page')
        
    sort = request.query_params.get('sort')
    
    try:
        sort = pagination_enum.SortType(sort)
        if sort == pagination_enum.SortType.ASC:
            sort = 'created'
        elif sort == pagination_enum.SortType.DESC:
            sort = '-created'
        else:
            sort = None
    except ValueError:
        sort = None

    try:
        page = int(page)
    except Exception:
        page = 1
    try:
        limit = int(limit)
    except Exception:
        limit = 10

    search = {'kw': search_kw, 'field': search_field} if search_kw else None

    return {
        'page': page,
        'limit': limit,
        'search': search,
        'is_active': is_active,
        'type_': type_,
        'sort': sort,
    }
