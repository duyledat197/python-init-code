from enum import Enum


class ApacEnum(Enum):
    @classmethod
    def list(cls):
        return [t.value for t in cls]
