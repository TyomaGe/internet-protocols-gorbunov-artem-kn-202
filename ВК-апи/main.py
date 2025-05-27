from FacadeFactory import FacadeFactory
from Exceptions import ExceptionsFactory
from ArgumentParser import ArgumentParser


def main():
    exceptions = ExceptionsFactory().get_exceptions()
    parser = ArgumentParser()
    facade_factory = FacadeFactory(parser)
    try:
        facade_factory.register_commands()
        args = parser.get_arguments()
        args.command_instance.run(args)
    except exceptions as e:
        print(f"\033[91m{e}\033[0m")

if __name__ == "__main__":
    main()
