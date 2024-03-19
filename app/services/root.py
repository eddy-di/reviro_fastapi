from sqlalchemy.orm import Session


class ServiceSessionContext:
    def __init__(self, db: Session) -> None:
        self.db = db


class AppService(ServiceSessionContext):
    pass


class DBSessionContext:
    """Context for database session."""

    def __init__(self, db: Session) -> None:
        """Initialization for session of connection to database."""

        self.db = db


class DatabaseCRUD(DBSessionContext):
    pass
