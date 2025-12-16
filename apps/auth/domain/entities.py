from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class User:
    id: Optional[int] | None
    username: str
    email: Optional[str] | None 
    password: Optional[str] | None 
    is_active: bool
    avatar: Optional[str] | None 
    is_2fa_enabled: bool 
    is_verify: bool
    is_superuser: bool
    is_staff: bool
    created: str
    modified: Optional[str] | None 
    is_removed: Optional[str] | None 
    groups: List[str]
    user_permissions: List[str]
