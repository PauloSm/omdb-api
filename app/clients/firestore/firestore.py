from typing import Optional, AsyncIterator, List, Tuple
from functools import lru_cache
from pathlib import Path

from google.cloud.exceptions import Conflict
from google.cloud.firestore_v1 import (
    AsyncClient,
    DocumentSnapshot,
)

from app.clients.base_db import IDocumentDB
from app.tools.tools import get_project_id
from app.tools.base_logger import ILogger, LogLevel

from .errors import (
    DocumentAlreadyExistsError,
    DocumentDeleteError,
    DocumentNotFoundError,
    DocumentReadError,
    DocumentWriteError,
)


class FirestoreClient(IDocumentDB):
    def __init__(self, collection_name: str, logger: ILogger, project_id: str | None = None) -> None:
        """
        Initializes a new FirestoreClient instance.

        Args:
            collection_name (str): Name of the Firestore collection.
            project_id (str | None): GCP ID where the Firestore database is located.
        """
        self._collection_name = collection_name
        self.logger = logger
        self._db = AsyncClient(project=project_id or get_project_id())

    async def get_document(self, path: str) -> DocumentSnapshot:
        """
        Get a single document from Firestore by its path.

        Args:
            path (str): The document path relative to the collection.

        Returns:
            DocumentSnapshot: The Firestore document snapshot.

        Raises:
            DocumentReadError: If an error occurs while fetching the document.
            DocumentNotFoundError: If the document does not exist.
        """
        document_path = str(Path(self._collection_name) / Path(path))
        try:
            document = await self._db.document(document_path).get()
        except Exception as e:
            self.logger.log(LogLevel.ERROR, f"Failed to get document on path: {path}")
            raise DocumentReadError from e
        if not document.exists:
            raise DocumentNotFoundError
        return document

    async def get_document_by_title(self, title: str) -> Optional[DocumentSnapshot]:
        """
        Get a single document by its Title attribute.

        Args:
            title (str): The title of the document to find.

        Returns:
            Optional[DocumentSnapshot]: The first document matching the title or None.
        """
        try:
            query = self._db.collection(self._collection_name).where("Title", "==", value=title).limit(1)
            async for document in query.stream():
                return document
        except Exception as e:
            self.logger.log(LogLevel.ERROR, f"Failed to get document by title: {title}")
            raise e
        return None

    async def create_document(self, path: str, document: dict) -> DocumentSnapshot:
        """
        Creates a new document in Firestore.

        Args:
            path (str): The path where the document will be created, relative to the collection.
            document (dict): The document data to store.

        Returns:
            DocumentSnapshot: A snapshot of the created document.

        Raises:
            DocumentAlreadyExistsError: If a document already exists at the specified path.
            DocumentWriteError: If an error occurs while creating the document.
        """
        document_path = str(Path(self._collection_name) / Path(path))
        try:
            await self._db.document(document_path).create(document)
            return await self._db.document(document_path).get()
        except Conflict:
            self.logger.log(LogLevel.ERROR, f"The document already exists at the path {path}")
            raise DocumentAlreadyExistsError
        except Exception:
            self.logger.log(LogLevel.ERROR, f"Failed to create the document {document}")
            raise DocumentWriteError

    async def delete_document(self, path: str) -> None:
        """
        Deletes a document from Firestore.

        Args:
            path (str): The path of the document to delete, relative to the collection.

        Raises:
            DocumentDeleteError: If an error occurs while deleting document.
        """
        await self.get_document(path)

        document_path = str(Path(self._collection_name) / Path(path))
        try:
            await self._db.document(document_path).delete()
        except Exception as e:
            self.logger.log(LogLevel.ERROR, f"Failed to get the document. Error: {e}")
            raise DocumentDeleteError

    async def get_all_documents(self, page_size: int = 10) -> AsyncIterator[DocumentSnapshot]:
        """
        Get all documents from the collection.

        Args:
            page_size (int, optional): Number of documents per page.

        Yields:
            DocumentSnapshot: Each document in the collection.
        """
        try:
            coll_ref = self._db.collection(self._collection_name)

            cursor = None
            while True:
                query = coll_ref.order_by("__name__").limit(page_size)
                if cursor:
                    query = query.start_after(cursor)

                docs = []
                async for doc in query.stream():
                    yield doc
                    docs.append(doc)

                if len(docs) < page_size:
                    break

                cursor = docs[-1]
        except Exception as e:
            self.logger.log(LogLevel.ERROR, f"Failed to get documents. Error {e}")
            raise e

    async def is_collection_empty(self) -> bool:
        """
        Checks if the Firestore collection is empty.

        Returns:
            bool: True if the collection contains is empty, False otherwise.
        """
        try:
            query = self._db.collection(self._collection_name).limit(1)
            results = query.stream()

            async for _ in results:
                return False
            return True
        except Exception as e:
            self.logger.log(LogLevel.ERROR, f"Failed to query the DB. Error: {e}")
            raise e

    async def get_paginated_documents(self, page_size: int = 10, start_after: str = None) -> Tuple[
        List[DocumentSnapshot], Optional[str]]:
        """
    Get a paginated list of documents from the Firestore collection, ordered by document ID.

    This method get a group of documents up to the specified page size, starting after
    a given document ID. It returns the documents with a token
    for the next page, which can be used to continue pagination.

    Args:
        page_size (int): The maximum number of documents to return.
        start_after (str, optional): The document ID to start the pagination after.

    Returns:
        Tuple[List[DocumentSnapshot], Optional[str]]: A tuple containing the list of DocumentSnapshots
                                                      and an optional ID of the last document. This ID
                                                      can be used as the `start_after` argument in a
                                                      next call to paginate through the next set
                                                      of documents.
    """
        query = self._db.collection(self._collection_name).order_by("__name__").limit(page_size)
        if start_after:
            last_doc = await self._db.collection(self._collection_name).document(start_after).get()
            if last_doc.exists:
                query = query.start_after(last_doc)
        docs = []
        async for doc in query.stream():
            docs.append(doc)
        next_page_token = docs[-1].id if docs else None
        return docs, next_page_token


@lru_cache
def get_firestore_client(logger: ILogger, collection_name: str = "movies") -> FirestoreClient:
    return FirestoreClient(
        collection_name=collection_name,
        logger=logger
    )
