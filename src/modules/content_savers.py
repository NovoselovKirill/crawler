import os
from abc import ABC, abstractmethod
from typing import Union, List

PathLike = Union[str, os.PathLike]


class ContentSaver(ABC):
    @abstractmethod
    def save(self, content, url: PathLike):
        pass


class FolderSaver(ContentSaver):
    def __init__(self, folder):
        pass

    def save(self, content, url: PathLike):
        pass


class ZipSaver(ContentSaver):
    def __init__(self, some_args):
        pass

    def save(self, content, url: PathLike):
        pass


class JoinedSavers(ContentSaver):
    def __init__(self, savers: List[ContentSaver]):
        self.savers = savers

    def save(self, content, url: PathLike):
        [saver.save(content, url) for saver in self.savers]
