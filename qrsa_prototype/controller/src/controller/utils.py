from typing import Callable, Generic, TypeVar


T = TypeVar("T")


class PubSub(Generic[T]):
    def __init__(self) -> None:
        self.subscription = []

    def subscribe(self, fn: Callable[[T], None]):
        self.subscription.append(fn)

    def publish(self, value: T):
        for s in self.subscription:
            s(value)

    def unsubscribe(self, fn: Callable[[T], None]):
        self.subscription = [s for s in self.subscription if s is not fn]
