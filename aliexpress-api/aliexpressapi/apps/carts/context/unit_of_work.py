from django.db import transaction

class UnitOfWork:
    def __enter__(self):
        self.atomic = transaction.atomic()
        self.atomic.__enter__()
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc:
            self.atomic.__exit__(exc_type, exc, tb)
        else:
            self.atomic.__exit__(None, None, None)
