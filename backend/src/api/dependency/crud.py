from typing import Callable, Type

from src.repository.crud.base import BaseCRUDRepository


def get_crud(
    repo_type: Type[BaseCRUDRepository],
    collection_name: str,
) -> Callable:
    def _get_repo() -> BaseCRUDRepository:
        return repo_type(collection_name=collection_name)

    return _get_repo
