from django.db import IntegrityError

class InsufficientBalance(IntegrityError):
    """Raised when a wallets has insufficient balance to
    run an operation.

    We're subclassing from :mod:`django.db.IntegrityError`
    so that it is automatically rolled-back during django's
    transaction lifecycle.
    """
class TransactionDoesNotExist(IntegrityError):
    """Raised when a Transaction record query does not exist.

    We're subclassing from :mod:`django.db.IntegrityError`
    so that it is automatically rolled-back during django's
    transaction lifecycle.
    """
