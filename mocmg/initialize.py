"""Used to initialize mocmg and to set log message settings."""


import logging
import sys
import traceback

module_log = logging.getLogger(__name__)


class _LessThanFilter(logging.Filter):
    """Filters messages of level value less than exclusive_maximum.

    Args:
        exclusive_maximum (int): Numeric value of minimum message level to be logged.

    Example:
        LessThanFilter(logging.WARNING)

    Note:
        See `Python logging library <https://docs.python.org/3/library/logging.html>`_ documentation
        for logging level numeric values, or simply use 'logging.INFO', 'logging.WARNING', etc.

    """

    def __init__(self, exclusive_maximum):
        super().__init__()
        self.max_level = exclusive_maximum

    def filter(self, record):
        # non-zero return means we log this message
        return 1 if record.levelno < self.max_level else 0


class _CustomFormatter(logging.Formatter):
    """Specifies the format of log messages, including date, time, and colors using ANSI color codes.

    Args:
        debug (bool, optional): Enable printing of line numbers within the code where the message
            was written.

    Attributes:
        debug (bool): Enable printing of line numbers within the code where the message
            was written.

    """

    # Omitted from coverage due to no way to retrieve contents on screen.
    def __init__(self, debug=False):  # pragma no cover
        self.debug = debug

        purple = "\x1b[35;10m"
        green = "\x1b[32;10m"
        default = "\x1b[39;10m"
        bold_red = "\x1b[31;1m"
        reset = "\x1b[0m"

        default_fmt = "%(asctime)s %(levelname)-10s: %(name)s - %(message)s"
        debug_fmt = "%(asctime)s %(levelname)-10s: %(name)s - (line: %(lineno)d) %(message)s"

        if debug:
            the_format = debug_fmt
        else:
            the_format = default_fmt

        self.FORMATS = {
            logging.DEBUG: green + the_format + reset,
            logging.INFO: default + the_format + reset,
            logging.WARNING: purple + the_format + reset,
            logging.ERROR: bold_red + the_format + reset,
            logging.CRITICAL: bold_red + the_format + reset,
        }

    # Omitted from coverage due to no way to retrieve contents on screen.
    def format(self, record):  # pragma no cover
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%H:%M:%S")
        return formatter.format(record)


class _ErrorHandler(logging.StreamHandler):
    """Handles messages to sys.stderr.

    Args:
        exit_on_error (bool, optional): In the event of an error, call sys.exit() and stop the program.

    """

    def __init__(self, exit_on_error=True):
        super().__init__(stream=sys.stderr)
        self.exit_on_error = exit_on_error

    def emit(self, record):
        super().emit(record)
        if (record.levelno >= logging.ERROR) and self.exit_on_error:
            traceback.print_stack()
            sys.exit(1)


def _add_require_log_level():
    """Add the "require" log level to the logger.

    The "require" log level takes an additional boolean argument to determine if an error should
    be logged. This is used in error checking to avoid numerous "if" statements, adding unnecessary
    cyclomatic complexity.

    Example:
        module_log.require(1 == 1, "Message if condition == False") # No message logged
        module_log.require(1 == 2, "Message if condition == False") # Message logged at error level

    """
    # Add 'requre' logger level
    def require(self, condition, message, *args, **kws):
        if isinstance(condition, bool):
            if not condition:
                # Yes, logger takes its '*args' as 'args'.
                self.log(logging.ERROR, message, *args, **kws)
        else:
            module_log.error("In requre(condition, message), 'condition' argument must be bool.")

    logging.addLevelName(logging.ERROR + 1, "REQUIRE")
    logging.Logger.require = require


def _get_verbosity_number(verbosity):
    """Get the numerical level associated with the verbosity.

    Args:
        verbosity (str): Verbosity level for mocmg. The levels are as follows:

            +-----------+----------------------------------------------------+
            |   Level   |   Description                                      |
            +===========+====================================================+
            |   silent  |   Don't output anything                            |
            +-----------+----------------------------------------------------+
            |   error   |   Display error messages only                      |
            +-----------+----------------------------------------------------+
            |   warning |   Display error and warning messages               |
            +-----------+----------------------------------------------------+
            |   info    |   Display error, warning, and info messages        |
            +-----------+----------------------------------------------------+
            |   debug   |   Display error, warning, info, and debug messages |
            +-----------+----------------------------------------------------+

    Returns:
        int: Integer verbosity level for mocmg

    """
    if verbosity == "info":
        num = logging.INFO
    elif verbosity == "debug":
        num = logging.DEBUG
    elif verbosity == "warning":
        num = logging.WARNING
    elif verbosity == "error":
        num = logging.ERROR
    elif verbosity == "silent":
        num = 99
    else:
        # If bad value, set to info. Throw error in initialize once logger is setup, so
        # the error is captured in the log file
        num = logging.INFO

    return num


def initialize(verbosity="info", color=True, exit_on_error=True):
    """Initialize the mocmg logger with the desired output options.

    Args:
        verbosity (str, optional): Verbosity level for mocmg. All messages below this level will not be
            displayed. The levels are as follows:

            +-----------+----------------------------------------------------+
            |   Level   |   Description                                      |
            +===========+====================================================+
            |   silent  |   Don't output anything                            |
            +-----------+----------------------------------------------------+
            |   error   |   Display error messages only                      |
            +-----------+----------------------------------------------------+
            |   warning |   Display error and warning messages               |
            +-----------+----------------------------------------------------+
            |   info    |   Display error, warning, and info messages        |
            +-----------+----------------------------------------------------+
            |   debug   |   Display error, warning, info, and debug messages |
            +-----------+----------------------------------------------------+

        color (bool, optional): Display log messages with color coded levels.
        exit_on_error (bool, optional): In the event of an error, call sys.exit()

    """
    # Add the additional log level "require".
    _add_require_log_level()
    # Get the numerical level for the verbosity
    verbosity_number = _get_verbosity_number(verbosity)
    # Get the root logger
    logger = logging.getLogger()
    # Clear any handlers if it already has them. Used primarily in test suite.
    logger.handlers.clear()
    # Have to set the root logger level, it defaults to logging.WARNING
    logger.setLevel(logging.NOTSET)
    # Format stdout and stderr based upon color and debug mode
    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)-10s: %(name)s - %(message)s", datefmt="%H:%M:%S"
    )
    debug_formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)-10s: %(name)s" + " - (line: %(lineno)d) %(message)s",
        datefmt="%H:%M:%S",
    )

    # Format log file ##############################################
    logging_handler_file = logging.FileHandler("mocmg.log", mode="w")
    if verbosity_number == logging.DEBUG:
        logging_handler_file.setFormatter(debug_formatter)
    else:
        logging_handler_file.setFormatter(formatter)
    logging_handler_file.setLevel(verbosity_number)

    logger.addHandler(logging_handler_file)

    # Format stdout #################################################
    logging_handler_out = logging.StreamHandler(sys.stdout)
    logging_handler_out.setLevel(verbosity_number)
    logging_handler_out.addFilter(_LessThanFilter(logging.WARNING))

    # If stdout is terminal, color if desired. Otherwise, don't color.
    # Omitted from coverage due to no way to retrieve contents on screen.
    if color and sys.stdout.isatty():  # pragma no cover
        if verbosity_number == logging.DEBUG:
            logging_handler_out.setFormatter(_CustomFormatter(debug=True))
        else:
            logging_handler_out.setFormatter(_CustomFormatter())
    else:
        if verbosity_number == logging.DEBUG:
            logging_handler_out.setFormatter(debug_formatter)
        else:
            logging_handler_out.setFormatter(formatter)
    logger.addHandler(logging_handler_out)

    # Format stderr #################################################
    logging_handler_err = _ErrorHandler(exit_on_error=exit_on_error)
    lvl = max(logging.WARNING, verbosity_number)
    logging_handler_err.setLevel(lvl)

    # If stderr is terminal, color if desired. Otherwise, don't color.
    # Omitted from coverage due to no way to retrieve contents on screen.
    if color and sys.stderr.isatty():  # pragma no cover
        if verbosity_number == logging.DEBUG:
            logging_handler_err.setFormatter(_CustomFormatter(debug=True))
        else:
            logging_handler_err.setFormatter(_CustomFormatter())
    else:
        if verbosity_number == logging.DEBUG:
            logging_handler_err.setFormatter(debug_formatter)
        else:
            logging_handler_err.setFormatter(formatter)
    logger.addHandler(logging_handler_err)

    # print warning about bad verbosity value now that logger is setup
    if verbosity not in ["info", "debug", "warning", "error", "silent"]:
        module_log.warning(
            f"Invalid verbosity option '{verbosity}'."
            + " Defaulting to 'info'.\n"
            + "    Next time please choose from one of: "
            + "'silent', 'error', 'warning', 'info', or 'debug'"
        )
