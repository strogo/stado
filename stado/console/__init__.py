import os
import sys
import argparse

from ..errors import StadoError
from .. import log


class CommandError(StadoError):
    """Raises when command generates error."""
    pass

class Command:
    """Base class for commands."""

    name = ''
    summary = ''

    def __init__(self, console):
        self.console = console

    def install(self, parser):
        """Overwritten by inheriting class."""
        return parser

    def run(self, *args, **kwargs):
        """Overwritten by inheriting class."""
        pass


    @staticmethod
    def is_site(path):
        """Returns True if given path is pointing to site directory."""

        if os.path.isdir(path) and 'site.py' in os.listdir(path):
            return True
        return False


    def event(self, name):
        """Execute event method in Console object."""

        method = getattr(self.console, name)

        if isinstance(method, (list, tuple)):
            if len(method) == 2:
                method[0](*method[1])
            else:
                method[0](*method[1], **method[2])
        else:
            method()



# Commands modules.

from .build import Build
from .watch import Watch
from .view import View
from .edit import Edit
from .help import Help



class Console:

    def __init__(self):

        # Available commands.

        self.commands = {
            Build.name: Build(self),
            Watch.name: Watch(self),
            View.name: View(self),
            Edit.name: Edit(self),
            Help.name: Help(self),
        }

        # Create command line parser.

        self.parser = argparse.ArgumentParser()
        subparsers = self.parser.add_subparsers()

        # Add subparsers from commands.

        for i in self.commands.values():
            parser = subparsers.add_parser(i.name, add_help=False)
            i.install(parser)


    # Shortcuts to commands.

    def build(self, *args, **kwargs):
        self.commands['build'].run(*args, **kwargs)

    def watch(self, *args, **kwargs):
        self.commands['watch'].run(*args, **kwargs)

    def view(self, *args, **kwargs):
        self.commands['view'].run(*args, **kwargs)


    # Execute command.

    def __call__(self, arguments=None):
        """Run stado with given arguments"""

        # Show help message if no arguments.

        print('')

        print('call', arguments)

        if len(sys.argv) == 1:
            return self.build()

        # Arguments from sys.args or from method arguments.
        if not arguments:
            args = self.parser.parse_args()
        else:
            args = self.parser.parse_args(arguments.split())

        print('parsed call', args)

        # Execute command.
        args = vars(args)

        if 'function' in args:
            cmd = args.pop('function')

            try:
                return cmd(**args)
            except KeyboardInterrupt:
                return True
            except StadoError as error:
                log.error(error)
                return False


    # Other methods.

    def set_interval(self, value):
        """Sets watcher interval."""
        self.commands['watch'].file_monitor.interval = value


    # Events:

    def before_waiting(self):
        """Runs before waiting loop in command run() method."""
        pass

    def stop_waiting(self):
        """Stops waiting loop in commands. For example stops development server."""
        self.commands['watch'].stop()
        self.commands['view'].stop()
        self.commands['edit'].stop()

    def after_rebuild(self):
        """Runs after site rebuild, usually by watcher."""
        pass
