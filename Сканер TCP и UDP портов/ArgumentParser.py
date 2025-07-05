import argparse


class ArgumentParser:
    def __init__(self):
        self.__parser = argparse.ArgumentParser(
            description="",
            epilog="",
            formatter_class=argparse.RawDescriptionHelpFormatter
        )

    def get_arguments(self):
        self.__parser.add_argument(
            "mode",
            choices=["opened", "protocols"],
            type=str,
        )
        self.__parser.add_argument(
            "ip",
            type=str,
        )
        self.__parser.add_argument(
            "protocol",
            type=str,
        )
        self.__parser.add_argument(
            "lower_bound",
            type=int,
        )
        self.__parser.add_argument(
            "upper_bound",
            type=int,
        )
        args = self.__parser.parse_args()
        return args
