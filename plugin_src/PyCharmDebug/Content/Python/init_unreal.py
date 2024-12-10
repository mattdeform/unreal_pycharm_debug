""" Plugin initialization script """

try:
    from pycharmremotedebug.menu import install  # type: ignore

    install()
except ImportError:
    pass
