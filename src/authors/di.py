from injector import Binder, Module

from src.authors import interfaces
from src.authors.services.author_repository import AuthorRepository


class AuthorModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(interfaces.AuthorRepository, AuthorRepository)  # type: ignore[type-abstract]
