from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, ClassVar, Dict, Optional
from uuid import UUID, uuid4


class Message(ABC):
    uuid: UUID
    message_type: ClassVar[str]
    command: ClassVar[str]

    def __init__(self, data: Optional[dict[str, Any]]) -> None:
        self.uuid = uuid4()

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def from_dict(self, data: Dict[str, Any]) -> None:
        pass
