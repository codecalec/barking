import logging
import abc
from typing import Iterable, Optional, List


class Event:
    pass


class Cut(abc.ABC):
    description: str
    required_branches: List[str]

    def __init__(
        self,
        description: Optional[str] = None,
        required_branches: Optional[List[str]] = None,
    ):
        if description:
            self.description = description
        if required_branches:
            self.required_branches = required_branches

    def check_requirements(self, event) -> bool:
        branch_statuses = [hasattr(event, branch) for branch in self.required_branches]
        if all(branch_statuses):
            return True
        else:
            msg = f"Following branches not in event for {self.__class__.__name__}: [ "
            for i, branch in enumerate(self.required_branches):
                if not branch_statuses[i]:
                    msg += f"{branch} "
            msg += "]"
            raise ValueError(msg)

    @abc.abstractmethod
    def cut(self, event: Event) -> Optional[Event]:
        pass

    def apply(self, event: Event) -> Optional[Event]:
        self.check_requirements(event)
        return self.cut(event)


class CutFlow:
    cuts: Iterable[Cut] = []

    def __init__(self, cuts: Iterable[Cut]):
        self.cuts = cuts

    def apply(self, event: Event):

        if event is None:
            return None

        if not self.cuts:
            raise Exception(f"No cuts supplied to {self}")

        # Apply the cuts and raise a exception if any Cut object cannot be applied
        for cut in self.cuts:
            try:
                if not cut.apply(event):
                    return None
            except ValueError as s:
                logging.exception(s)
                exit(1)

        return event
