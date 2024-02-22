class FirestoreBaseError(Exception):
    pass


class DocumentReadError(FirestoreBaseError):
    pass


class DocumentWriteError(FirestoreBaseError):
    pass


class DocumentDeleteError(FirestoreBaseError):
    pass


class DocumentNotFoundError(DocumentReadError):
    pass


class DocumentAlreadyExistsError(DocumentWriteError):
    pass
