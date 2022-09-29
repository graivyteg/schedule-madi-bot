from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    id: int
    name: str
    group: str

    def has_name(self):
        return len(self.name) > 0

    def has_group(self):
        return len(self.group) > 0

    def is_authorized(self):
        return self.has_name() and self.has_group()

    def __str__(self):
        return f'{self.id}: {self.name} - {self.group}'
