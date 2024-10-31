""" Plugin initialization script """
try:
    from pycharmremotedebug.menu import install
    install()
except ImportError:
    pass
