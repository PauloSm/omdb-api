from abc import ABC, abstractmethod


class IDocumentDB(ABC):
    @abstractmethod
    async def get_document(self, path: str):
        pass

    @abstractmethod
    async def get_document_by_title(self, path: str):
        pass

    @abstractmethod
    async def create_document(self, path: str, document: dict):
        pass

    @abstractmethod
    async def delete_document(self, path: str):
        pass

    @abstractmethod
    async def get_all_documents(self):
        pass

    @abstractmethod
    async def is_collection_empty(self):
        pass

    @abstractmethod
    async def get_paginated_documents(self, page_size: int = 10, start_after: str = None):
        pass
