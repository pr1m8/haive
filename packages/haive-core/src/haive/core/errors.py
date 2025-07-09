import sys
import traceback

def short_traceback(exc_type, exc_value, exc_tb):
    """
    A custom exception hook to provide short, clean tracebacks.
    It prints only the error type and message, avoiding the full stack trace.
    """
    print("\n❌ Error:")
    print("".join(traceback.format_exception_only(exc_type, exc_value)).strip())

def install_short_tracebacks():
    """
    Installs the short_traceback function as the global exception hook.
    """
    sys.excepthook = short_traceback 