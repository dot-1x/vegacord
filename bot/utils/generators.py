from typing import Any, Generator, TypeVar

T = TypeVar("T")


def chunk_list(lst: list[T], size=3) -> Generator[list[T], Any, Any]:
    for i in range(0, len(lst), size):
        yield lst[i : i + size]
