from enum import Enum

class GetType(Enum):
    ALL = 'all'
    PAGE = 'page'

class SortType(Enum):
    ASC = 'ASC'
    DESC = 'DESC'

class Status(Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
