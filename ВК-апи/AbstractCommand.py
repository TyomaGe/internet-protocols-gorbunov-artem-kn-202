from abc import ABC, abstractmethod


class AbstractCommand(ABC):
    @abstractmethod
    def run(self, args):
        pass

    def get_args(self, parser):
        parser.add_argument(
            "id",
            type=str,
        )
