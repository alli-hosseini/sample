from typing import Union, Callable, List, Tuple, Type

from shared.domain import DomainEvent, Repository

from .types import CommandConfig, EventConfig, QueryConfig

from .interfaces import Command, Query, Bus, QueryBus

from .conf import Commands, Queries, Events


class TransactionBoundary:
    def start(self):
        pass

    def commit(self):
        pass

    def rollback(self):
        pass

    def __enter__(self) -> "TransactionBoundary":
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb is not None:
            self.rollback()
        else:
            self.commit()


def atomic(operation: Callable):
    def wrap(*args, **kwargs):
        with TransactionBoundary():
            result = operation(*args, **kwargs)
        return result

    return wrap


class InMemoryBus(Bus):
    def handle(self, message: Union[Command | DomainEvent]) -> Union[str, None]:
        raise NotImplementedError


class InMemoryQueryBus(QueryBus):
    def __init__(self, queries: QueryConfig):
        self.queries = queries

    def ask(self, query: Query):
        if query.__class__ not in self.queries:
            raise

        return self.queries[query.__class__]().handle(query)


bus = InMemoryBus()

query_bus = InMemoryQueryBus(Queries)
