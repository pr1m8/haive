import sys


def short_traceback(exc_type, exc_value, exc_tb):
    """A custom exception hook to provide short, clean tracebacks.
    It prints only the error type and message, avoiding the full stack trace.
    """


def install_short_tracebacks():
    """Installs the short_traceback function as the global exception hook."""
    sys.excepthook = short_traceback
