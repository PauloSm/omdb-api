from typing import Generic, List, Optional, TypeVar
from pydantic.generics import GenericModel

T = TypeVar('T')


class Page(GenericModel, Generic[T]):
    items: List[T]
    next_page_token: Optional[str]
    page_size: int
